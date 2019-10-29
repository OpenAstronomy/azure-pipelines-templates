import os
import sys


def test_32bit():
    if '32' in os.environ['ENVNAME']:
        assert sys.maxsize == 2147483647
    else:
        assert sys.maxsize == 9223372036854775807
