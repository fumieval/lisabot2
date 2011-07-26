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