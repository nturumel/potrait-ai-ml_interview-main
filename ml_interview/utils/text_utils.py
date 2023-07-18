import re


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
