import sys, os, pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'lab1')))
from main import compress_rle, decompress_rle

def test_compress_basic(): assert compress_rle("AAABCC") == "A3B1C2"
def test_compress_no_repeats(): assert compress_rle("ABC") == "A1B1C1"
def test_compress_empty(): assert compress_rle("") == ""
def test_compress_single(): assert compress_rle("A") == "A1"
def test_compress_all_same(): assert compress_rle("AAAAA") == "A5"

def test_decompress_basic(): assert decompress_rle("A3B1C2") == "AAABCC"
def test_round_trip(): assert decompress_rle(compress_rle("WWWWAAADEEXYYYYYZZ")) == "WWWWAAADEEXYYYYYZZ"