import re
from typing import List

import html2text
import nltk
from bs4 import BeautifulSoup, NavigableString

nltk.download("punkt")


def split_text_into_sentences(text: str) -> List[str]:
    sentences: List[str] = nltk.sent_tokenize(text)
    return sentences


def post_clean_text(text: str):
    # Strip leading and trailing whitespace
    text = text.strip()

    # Replace tabs with a space
    text = text.replace("\t", " ")

    # Replace double spaces with a single space
    text = re.sub(r" {2,}", " ", text)

    # Convert triple newlines to a single newline
    text = re.sub(r"\n\n\n", "\n", text)

    # Now convert double newlines to a single newline
    text = re.sub(r"\n\n", "\n", text)

    # Remove newlines before or after the text
    text = re.sub(r"^\n+|\n+$", "", text)

    return text


def pre_clean_text(text: str):
    # Replace \' with '
    text = text.replace("\\'", "'")

    # Replace double new lines with triple new lines
    text = text.replace("\n\n", "\n\n\n")

    # Replace single new lines followed by a tab or extra space with double new lines
    text = re.sub(r"\n\s+", "\n\n", text)

    # Replace remaining single new lines with double new lines, but only when \n is not followed by one of these punctuation marks: .!?
    text = re.sub(r"\n(?![.!?])", "\n\n", text)

    # Add \n\n after every sentence that ends with more than one space
    text = re.sub(r"([.!?])\s{2,}", r"\1\n\n", text)

    # Add \n after every sentence except if sentence ends with ")"
    text = re.sub(r"([.!?])(?=[^)])(?=\s)", r"\1\n", text)

    return text


def extract_sections_from_html_file(file_path: str) -> List[str]:
    with open(file_path, "r") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")

    sections: List[str] = []
    current_section: List[str] = []
    current_heading = None

    for tag in soup.recursiveChildGenerator():
        if isinstance(tag, NavigableString):  # if it's a text element
            text = str(tag).strip()
            if text:  # if it's non-empty
                current_section.append(text)
        elif tag.name == "b":  # if it's a heading
            if current_heading is not None:  # if there was a previous heading
                # join all text elements in the section into one string
                section_text = "\n".join(current_section)
                # concatenate the heading and the section text and add it to the list of sections
                sections.append(current_heading + "\n" + section_text)
                # reset the current section
                current_section = []
            # set the current heading
            current_heading = tag.text.strip()

    # add the last section if it's non-empty
    if current_heading is not None and current_section:
        section_text = " ".join(current_section)
        sections.append(current_heading + " " + section_text)

    return sections
