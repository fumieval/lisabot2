# coding: utf-8
"""
Lisabot 2.3.0 chatter
"""
from __future__ import unicode_literals
import random
import string
import itertools

from lisabot2.core.chatter.util import *

def get_keywords(x):
    """Get keyword in sentence."""
    keywords = []
    for word, data in parse(x):
        if data[0] == "感動詞" or data[0] == "名詞" and data[1] != "非自立" and data[1] != "代名詞":
            keywords.append(word)
    return keywords

def get_elements(x):
    keywords = []
    for word, data in parse(x):
        if data[0] not in ["助詞", "助動詞", "記号"] and data[6] != "する":
            keywords.append(word if data[6] == "*" else data[6])
    return keywords

def extend_markovtable(table, words):
    word0 = word1 = word2 = ""
    for word in itertools.ifilter(None, words):
        if word0 and word1 and word2:
            if not word0 in table:
                table[word0] = {}
            if not word1 in table[word0]:
                table[word0][word1] = {}
            if not word2 in table[word0][word1]:
                table[word0][word1][word2] = []
            table[word0][word1][word2].append(word)
        word0, word1, word2 = word1, word2, word
            
def extend_table(table, text):
    """一方向にマルコフ連鎖の辞書を拡張する。"""
    extend_markovtable(table, [START_SYMBOL] * 3 + wakati(text) + [END_SYMBOL])

def extend_table_both(ltor, rtol, text):
    """双方向にマルコフ連鎖の辞書を拡張する。"""
    words = wakati(text)
    extend_markovtable(ltor, [START_SYMBOL] * 3 + words + [END_SYMBOL])
    words.reverse()
    extend_markovtable(rtol, [START_SYMBOL] * 3 + words + [END_SYMBOL])

def greedymarkov(keywords, table, word2, word1, word0, depth=64):
    """可能ならばkeywordsの単語を使用して文章を生成する。"""
    if word0 == END_SYMBOL or depth == 0:
        return [], len(keywords)

    candidate = filter(lambda w: w in keywords, table[word2][word1][word0])
    if candidate:
        result = map(lambda w: greedymarkov(filter(lambda x: x != w, keywords),
                                            table, word1, word0, w, depth - 1),
                     candidate)
        best = min(itertools.imap(lambda xs: xs[1], result))
        final = filter(lambda xs: xs[1] == best, result)
        return [word0] + random.choice(final)[0], best
    else:
        result, score = greedymarkov(keywords, table, word1, word0,
                                     random.choice(table[word2][word1][word0]),
                                     depth - 1)
        return [word0] + result, score

def format_words(wordlist):
    """単語のリストから文章を作る。"""
    flag = False
    result = ""
    for word in wordlist:
        if isterminal(word):
            continue
        if word[0] == "#":
            result += " "
        newflag = all(itertools.imap(lambda x: x in string.ascii_letters, word))
        result += " " * (flag and newflag) + word
        flag = newflag
    return result

def greedygenerate(table, keywords):
    return format_words(greedymarkov(keywords, table, START_SYMBOL,
                                     START_SYMBOL, START_SYMBOL)[0])
    
def generate(ltor, rtol, origin=None, keywords=[]):
    """Not implemented
    双方向マルコフ連鎖。originで指定したワードを可能ならば使用する。
    パフォーマンスを損なわない範囲でkeywordsを使用する。"""
    word0 = origin and random.choice(ltor.keys())
    word1 = random.choice(ltor[word0].keys())
    word2 = random.choice(ltor[word0][word1].keys())
