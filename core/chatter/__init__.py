# coding: utf-8
"""
Lisabot 2.4.0 chatter
"""
from __future__ import unicode_literals

import itertools
import random
import string

from lisabot2.core.chatter.util import *

def getkeywords(x):
    """Get keywords in the sentence."""
    return [word for word, data in parse(x) if word != "ー" and \
            data[0] in ["感動詞", "名詞"] and \
            data[1] not in ["非自立", "代名詞"]]
def getelements(x):
    """get elements in the sentence."""
    return [word for word, data in parse(x) if word == "…" or \
            data[0] not in ["助詞", "助動詞", "記号"] and \
            data[6] not in ["する", "ー"]]

def extend_markovtable(table, words):
    """マルコフ連鎖の辞書を拡張する。"""
    word0 = word1 = word2 = START_SYMBOL
    for word in itertools.ifilter(None, words + [END_SYMBOL]):
        if not word0 in table:
            table[word0] = {}
        if not word1 in table[word0]:
            table[word0][word1] = {}
        if not word2 in table[word0][word1]:
            table[word0][word1][word2] = []
        table[word0][word1][word2].append(word)
        word0, word1, word2 = word1, word2, word

def extend_table(table, text):
    """一方向にマルコフ連鎖の辞書を拡張する。
    todo: extend_markovtableと統合"""
    extend_markovtable(table, wakati(text))

def greedymarkov(keywords, table, word2, word1, word0, depth=64):
    """可能ならばkeywordsの単語を使用して文章を生成する。"""
    if word0 == END_SYMBOL or depth == 0:
        return [], len(keywords)

    candidate = [w for w in table[word2][word1][word0] if w in keywords]
    if candidate:
        result = [greedymarkov([x for x in keywords if x != w],
                               table, word1, word0, w, depth - 1) for w in candidate]
        best = min(y for x, y in result)
        final = [(x, y) for x, y in result if y == best]
        return [word0] + random.choice(final)[0], best
    else:
        result, score = greedymarkov(keywords, table, word1, word0,
                                     random.choice(table[word2][word1][word0]),
                                     depth - 1)
        return [word0] + result, score

def format_words(wordlist, conversation=False):
    """単語のリストから文章を作る。"""
    flag = False
    result = ""
    for word in wordlist:
        if isterminal(word):
            continue
        if word[0] == "#":
            result += " "
        if conversation and word == "リサ":
            result += "%(name)s"
            continue
        if word in ["俺", "僕", "私", "わし", "あたい", "あたし", "わたし"]:
            result += "自分"
            continue

        if conversation and word in ["お前", "きみ", "あなた", "貴方", "てめえ", "あんた", "貴様"]:
            result += "%(name)s氏"
        newflag = all(x in string.ascii_letters for x in word)
        result += " " * (flag and newflag) + word
        flag = newflag
    return result

def greedygenerate(table, keywords, conversation=False):
    """指定された辞書とキーワードから整形された文章を出力する。"""
    return format_words(greedymarkov(keywords, table, START_SYMBOL,
                                     START_SYMBOL, START_SYMBOL)[0], conversation)
