import csv
import glob
import os

from ml_interview.utils.text_utils import post_clean_text, pre_clean_text
from ml_interview.utils.constants import BERT_CHUNK_SIZE, DATA_DIR
from ml_interview.utils.text_tokenizers import (
    calculate_bert_length,
    get_bert_text_splitter,
)


def split_text_chunks(text: str):
    """
    Split a text chunk into smaller chunks based on a maximum token limit.
    This function will attempt to split the text evenly without breaking sentences.
    """
    text_splitter = get_bert_text_splitter()
    chunks = text_splitter.split_text(text)

    return chunks


def process_csv_files_bert():
    """
    Process all CSV files in the data directory.
    Each file will be read, its text chunks will be split if necessary,
    and a new CSV file will be written with the adjusted chunks.
    """
    output_dir = os.path.join(DATA_DIR, "output")
    os.makedirs(
        output_dir, exist_ok=True
    )  # create output directory if it doesn't exist

    for file_path in glob.glob(os.path.join(DATA_DIR, "*.csv")):
        new_rows = []

        with open(file_path, "r") as f:
            reader = csv.reader(f)

            for row in reader:
                text_chunk = row[0]  # assuming only one column per row
                token_length = calculate_bert_length(text_chunk)

                # If the text chunk is too large, split it
                if token_length > BERT_CHUNK_SIZE:
                    chunks = split_text_chunks(pre_clean_text(text_chunk))
                    new_rows.extend(
                        [
                            (
                                post_clean_text(chunk),
                                calculate_bert_length(post_clean_text(chunk)),
                            )
                            for chunk in chunks
                        ]
                    )
                else:
                    new_rows.append(((text_chunk), token_length))

        # Write the new rows to a new CSV file
        output_file_name = os.path.basename(file_path).replace(
            ".csv", "_bert_segmented.csv"
        )
        output_file_path = os.path.join(output_dir, output_file_name)
        with open(output_file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["text", "token_length"])  # write header
            writer.writerows(new_rows)


if __name__ == "__main__":
    process_csv_files_bert()
