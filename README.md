# ML engineer interview

Welcome, the point of this interview is to give you an idea of a common problems we'll be working on at portrait,  
see how you work through problems and to gauge your interest in our work. 
Code that solves the problem is most important, don't worry too much about readability.


## prerequisites

```
python 
https://python-poetry.org/docs/
https://github.com/huggingface/tokenizers
```

wordpiece tokenization can be preformed with this snippet:

```python
from tokenizers import BertWordPieceTokenizer
tokenizer: BertWordPieceTokenizer = BertWordPieceTokenizer.from_file("./bert-base-uncased-vocab.txt")
len(tokenizer.encode("some sentence").ids) # this is the number of tokens
```

## getting started

please create a new branch with your name as the name to get started.
i.e. `git branch -b john-doe`  
in the root of this project run `poetry install` to install all the python dependencies.

Please keep track of the time you spend on the problem by making a commit when you start and finish part 1. and part 2.

## part 1.


Both tasks are segmentation problems.
You'll be given a number of paragraphs in the form of a csv. They look like this:

```

"a paragraph from that section"
"The next paragraph. With a lot of text this one is probably too long. There's also a lot of sentences in it. This is probably a better example with an even number of sentences though."
etc.

```

Each line is a `text chunk`, and can contain multiple `sentences` or one.

So in the above example one `text chunk` is "a paragraph from that section"  
and another is: "The next paragraph. With a lot of text this one is probably too long. There's also a lot of `sentences` in it. This is probably a better example with an even number of `sentences` though."  

We want to keep the number of tokens in any `text chunk` section under 180.
If the number of tokens is over 180 try to evenly break up the `text chunk` <i>without breaking in the middle of a sentence</i>.  
Use the `BertWordPieceTokenizer` to count the number of tokens in each text chunk, and any other libraries that you find helpful.

Create a new csv alongside each `<year>.csv` file with the name `<year>_bert_segmented.csv` in the same format as the original except
the long `text chunk` sections should broken into multiple `text chunks`. Please keep them ordinal.

so if the above example was over 180 tokens ( but not over 360 ) it would look like this after your code ran.

```

"a paragraph from that section"
"The next paragraph. With a lot of text this one is probably too long."
"There's also a lot of sentences in it. This is probably a better example with an even number of sentences though."  
etc.

```

Don't forget to make a commit for time tracking!

## part 2.

Great, I hope that went swimmingly and you're excited to work on the second part of this little project.
The next part is another segmentation problem this one for a gpt-3 context window.  
You can start using your BERT segmented text or the original texts.

Since we'll be doing things like making summaries, asking, and answering questions that need a lot of context  
we want to fit as much of our document <i>within the bounds of a topic</i> into the context window as we can.

Our goal is to create new text chunks under 3800 gpt tokens long while splitting on changes in topics.

The definition of a topic is ambiguous and you decide based on your assumptions where a split should be made.

to count tokens you can use a gpt2 tokenizer like so:

```python
from tokenizers import Tokenizer

tokenizer = Tokenizer.from_pretrained("ComCom/gpt2-small") # this will download about 2mb
len(tokenizer.encode("some sentence").ids) # this is the number of tokens
```

To find good break points you can choose any method you want ( apart from hand labeling breakpoints 😅 ), if you'd like to use sentence similarity embeddings you can use the following endpoint.  
This is the model being used: https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2


```python
import requests

url = "https://fctcyg9tpt5zelzq.us-east-1.aws.endpoints.huggingface.cloud/"

payload = {"inputs": "This is my favorite sentence."}
headers = {
    "Authorization": "Bearer BiAncWndOfeSpTVTnppeZMDOSjIGrDixfzQsIcvBHsrLKULmCOBHZfsPISBFGtsUPIFVYwmcSDdXSTIpkLTDTUuYGaTjKwzLalqwWdlPXyqLoeCJGvvpSBlXhmipczGQ",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
```

Create a new csv alongside each `<year>.csv` file with the name `<year>_gpt_segmented.csv` in the same format as the original except with 
long text chunks under 3800 gpt tokens. Please keep the texts ordinal.

Don't forget to make a commit for time tracking!




-------------------------------------
## APPENDIX
```python
class RecursiveCharacterTextSplitter(TextSplitter):
    """Implementation of splitting text that looks at characters.

    Recursively tries to split by different characters to find one
    that works.
    """

    def __init__(
        self,
        separators: Optional[List[str]] = None,
        keep_separator: bool = True,
        **kwargs: Any,
    ) -> None:
        """Create a new TextSplitter."""
        super().__init__(keep_separator=keep_separator, **kwargs)
        self._separators = separators or ["\n\n", "\n", ';', ':', " ", ""]

    def _split_text(self, text: str, separators: List[str]) -> List[str]:
        """Split incoming text and return chunks."""
        final_chunks = []
        # Get appropriate separator to use
        separator = separators[-1]
        new_separators = []
        for i, _s in enumerate(separators):
            if _s == "":
                separator = _s
                break
            if re.search(_s, text):
                separator = _s
                new_separators = separators[i + 1 :]
                break

        splits = _split_text_with_regex(text, separator, self._keep_separator)
        # Now go merging things, recursively splitting longer texts.
        _good_splits = []
        _separator = "" if self._keep_separator else separator
        for s in splits:
            if self._length_function(s) < self._chunk_size:
                _good_splits.append(s)
            else:
                if _good_splits:
                    merged_text = self._merge_splits(_good_splits, _separator)
                    final_chunks.extend(merged_text)
                    _good_splits = []
                if not new_separators:
                    final_chunks.append(s)
                else:
                    other_info = self._split_text(s, new_separators)
                    final_chunks.extend(other_info)
        if _good_splits:
            merged_text = self._merge_splits(_good_splits, _separator)
            final_chunks.extend(merged_text)
        return final_chunks

```