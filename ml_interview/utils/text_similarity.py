import json
from typing import List

import requests

from ml_interview.utils.constants import (
    GPT_SIMILARITY_THRESHOLD_LOWER,
    GPT_SIMILARITY_THRESHOLD_UPPER,
)

API_URL = (
    "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
)
headers = {"Authorization": f"Bearer {'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'}"}


def compare_text(base_text: str, search_text: str) -> int:
    try:
        payload = {"inputs": {"source_sentence": base_text, "sentences": [search_text]}}
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raises a HTTPError if the response was unsuccessful
        similarity: float = json.loads(response.text)[0]
        if similarity > GPT_SIMILARITY_THRESHOLD_UPPER:
            return 2
        if similarity > GPT_SIMILARITY_THRESHOLD_LOWER:
            return 1
        else:
            return 0
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0  # type: ignore
