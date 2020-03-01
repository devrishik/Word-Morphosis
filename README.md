# Word Morphosis

Word Morphosis is a Python library for dealing with word ladder
It runs a bi-directional BFS

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requests.

```bash
pip3 install requests
```

## Usage

```bash
python3 word_morphosis.py <start word> <end word> [--test]
```
The data is gathered from [five-letter-words](https://www.bestwordlist.com/5letterwords.txt)  
The `test` flag uses all the words which only begin with 'A'
