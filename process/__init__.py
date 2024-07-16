from pathlib import Path
from typing import Any, List
from .parser_base import BaseParser
from .pdfparser import PDFParser
from .docparser import WordParser
from .pptparser import PPTXParser
from .mdparser import MDParser
from .txtparser import TXTParser
from .imgparser import ImgParser

from config import IMAGE_TYPES

import os 
import nltk
os.environ['nltk_data'] =  '/home/cyh/nltk_data/packages/tokenizers/punkt/PY3/english.pickle'
nltk.data.path.append("/home/cyh/nltk_data")
#nltk.download("punkt")


# import nltk
# punkt_path = "/home/cyh/nltk_data/packages/tokenizers/punkt/PY3/english.pickle"
# tokenizer = nltk.data.load(punkt_path, format='raw')

#nltk.download("punkt")
#import nltk
#nltk.data.path.append("/home/cyh/nltk_data/nltk_data")


parsers: List[BaseParser] = [PDFParser, WordParser, PPTXParser, MDParser, TXTParser, ImgParser]


def _get_parser(suffix: str) -> BaseParser:
    for parser in parsers:
        if parser.type.lower() == suffix.lower():
            return parser
    return None


def process_file(file_path: str, suffix: Any, model: Any):
    fpath = Path(file_path)
    suffix = suffix if suffix is not None else fpath.suffix.strip('.')
    if suffix in IMAGE_TYPES:
        suffix = "image"
    
    parser = _get_parser(suffix)
    print(parser)
    if not parser:
        raise NotImplementedError("Suffix of file is not supported.")
    
    return parser(file_path, model, None).parse()