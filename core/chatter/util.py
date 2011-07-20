# coding: utf-8
from __future__ import unicode_literals
import MeCab
import itertools

START_SYMBOL = "#@#START#@#"
END_SYMBOL = "#@#END#@#"

def parse(x):
    result = []
    tagger = MeCab.Tagger(str(""))
    for line in tagger.parse(x.encode("utf-8")).decode("utf-8").split("\n"):
        if line == "EOS": return result
        word, data = line.split("\t")
        result.append((word, data.split(",")))

def wakati(x):
    return MeCab.Tagger(str("-Owakati")).parse(x.encode("utf-8")).decode("utf-8").strip("\n").split(" ")


def isterminal(word):
    return word == START_SYMBOL or word == END_SYMBOL

def issymbol(word):
    return word == "." or word == "。" or \
           word == "!" or word == "！" or \
           word == "?" or word == "？" or \
           word == START_SYMBOL or \
           word == END_SYMBOL


def ibranch(functions, *args, **kwargs):
    """
    >>> f = lambda x, y: x + y
    >>> g = lambda x, y: x * y
    >>> h = lambda x, y: x ** y
    >>> A = ibranch((f, g, h), 4, 3)
    >>> next(A)
    7
    >>> next(A)
    12
    >>> next(A)
    64
    """
    return itertools.imap(lambda f: f(*args, **kwargs), functions)

def merge(f, *functions):
    """
    >>> f = lambda x: x + 2
    >>> g = lambda x: x - 3
    >>> A = lambda x, y: x * y
    >>> F = merge(A, f, g) #λx.(x + 2)(x + 3)
    >>> F(2)
    -4
    >>> F(3)
    0
    >>> F(5)
    14
    """
    return lambda *args, **kwargs: f(*ibranch(functions, *args, **kwargs))
