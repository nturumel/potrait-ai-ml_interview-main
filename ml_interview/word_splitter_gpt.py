import csv
import glob
import os
from typing import List

from ml_interview.utils.constants import DATA_DIR, GPT_CHUNK_SIZE
from ml_interview.utils.text_similarity import compare_text
from ml_interview.utils.text_utils import (
    post_clean_text,
    pre_clean_text,
)
from ml_interview.utils.text_tokenizers import (
    calculate_gpt_length,
    get_gpt_text_splitter,
)


def split_text_chunks(text: str):
    """
    Split a text chunk into smaller chunks based on a maximum token limit.
    This function will attempt to split the text evenly without breaking sentences.
    """
    text_splitter = get_gpt_text_splitter()

    chunks = text_splitter.split_text(text)

    return chunks


def process_csv_files_gpt():
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

            segmented_rows: List[str] = []
            prev_row_chunk = next(reader)[0]
            segmented_rows.append(prev_row_chunk)
            for row in reader:
                current_row_chunk = row[0]
                # If the end of the previous row is similar to the beginning of the current row
                if compare_text(prev_row_chunk, current_row_chunk) == 2:
                    # Join the two rows with a newline
                    segmented_rows[-1] = "\n".join([segmented_rows[-1], current_row_chunk])  # type: ignore

                # If the end of the previous row is similar to the beginning of the current row
                elif compare_text(prev_row_chunk, current_row_chunk) == 1:
                    # Join the two rows with two newlines, less similar
                    segmented_rows[-1] = "\n\n".join([segmented_rows[-1], current_row_chunk])  # type: ignore
                else:
                    # Add the current row to the output list
                    segmented_rows.append(current_row_chunk)  # type: ignore
                prev_row_chunk = current_row_chunk
                # If the end of the previous row is similar to the beginning of the current row

            for segment in segmented_rows:
                text_chunk = segment  # assuming only one column per row
                token_length = calculate_gpt_length(text_chunk)

                # If the text chunk is too large, split it
                if token_length > GPT_CHUNK_SIZE:
                    chunks = split_text_chunks(pre_clean_text(text_chunk))
                    new_rows.extend(
                        [
                            (
                                post_clean_text(chunk),
                                calculate_gpt_length(post_clean_text(chunk)),
                            )
                            for chunk in chunks
                        ]
                    )
                else:
                    new_rows.append(((text_chunk), token_length))

        # Write the new rows to a new CSV file
        output_file_name = os.path.basename(file_path).replace(
            ".csv", "_gpt_segmented.csv"
        )
        output_file_path = os.path.join(output_dir, output_file_name)
        with open(output_file_path, "w", newline="") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["text", "token_length"])  # write header
            writer.writerows(new_rows)


if __name__ == "__main__":
    process_csv_files_gpt()
