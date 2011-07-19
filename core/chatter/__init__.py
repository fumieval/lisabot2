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

    return map(lambda xs: xs[1][6],
               itertools.ifilter(lambda xs: xs[1][0] , parse(x)))

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
    extend_markovtable(table, [START_SYMBOL] * 3 + wakati(text) + [END_SYMBOL] * 3)

def markov(table, start,
           choice=lambda w, x, y: random.choice(w[x][y]),
           before=lambda x: False, after=lambda x: False):
    
    r = []
    
    word0, word1, word2 = start
    
    while word0 in table and word1 in table[word0] and word2 in table[word0][word1]:
        word0, word1, word2 = word1, word2, choice(table, word0, word1, word2)
        
        if before(word2) or isterminal(word2): break
        
        a = isAlphabetonly(word2)
        if r and not a and r[-1] == " ": r.pop()
        r.append(word2)
        if a: r.append(" ") #アルファベットのみの場合はスペースを追加する
        
        if after(word2): break
        
    if r and r[-1] == " ": r.pop()
    
    return r

def keywordchooser(keywords):
    def f(table, word0, word1, word2):
        candidate = filter(lambda word: word in keywords, table[word0][word1][word2])
        if candidate:
            word = random.choice(candidate)
            keywords.remove(word)
            return word
        else:
            return random.choice(table[word0][word1][word2])
    return f

def greedymarkov(keywords, table, word2, word1, word0, depth=16):
    """keywordに与えられた単語を最大限使用する"""

    if  depth == 0 or word0== END_SYMBOL:
        return [], len(keywords)
    candidate = filter(lambda w: w in keywords, table[word2][word1][word0])
    if candidate:
        result = map(lambda word: greedymarkov(filter(lambda x: x != word, keywords),
                                               table, word1, word0, word, depth - 1), candidate)
    else:
        result = map(lambda word: greedymarkov(keywords, table, word1, word0, word, depth - 1), random.sample(table[word2][word1][word0],1))
    
    best = min(itertools.imap(lambda xs: xs[1], result)) #残ったキーワードの最小値
    final = filter(lambda xs: xs[1] == best, result) #最終的な解の候補
    if all(itertools.imap(isterminal, final)):
        return [], len(keywords) #解が全て終了記号の場合
    else:
        return [word0] + random.choice(final)[0], best

def format_words(wordlist):
    flag = False
    result = ""
    for word in wordlist:
        if isterminal(word): continue
        if word[0] == "#": result += " "
        newflag = all(itertools.imap(lambda x: x in string.ascii_letters, word))
        result += " " * (flag and newflag) + word
        if word[0] == "#": result += " "
        flag = newflag
    return result


def generate(LtoR, RtoL, keywords=None):

    _ = itertools

    if keywords:    
        #起点
    
        lst = list(_.chain(*_.imap(lambda word: _.ifilter(lambda x: word == x,
                                                          LtoR.keys()), keywords)))
        
        if lst:
            word0 = random.choice(lst)
            keywords_ = list(keywords)
            chooser = keywordchooser(keywords_) #キーワードを元に次の候補を選択する関数
        else:
            word0 = random.choice(LtoR.keys())
            chooser = lambda w, x, y, z: random.choice(w[x][y][z])
    else:
        word0 = random.choice(LtoR.keys())
        chooser = lambda w, x, y, z: random.choice(w[x][y][z])

    word1 = random.choice(LtoR[word0].keys())
    word2 = random.choice(LtoR[word0][word1].keys())
    result = []
    result.extend(reversed(markov(RtoL, (word2, word1, word0), chooser))) #左方向に拡張
    result.extend([word0, word1]) #基点
    result.extend(markov(LtoR, (word0, word1, word2), chooser)) #右方向に拡張
    
    return ''.join(result)

def greedygenerate(table, keywords=None):
    return format_words(greedymarkov(keywords, table,
                                     START_SYMBOL, START_SYMBOL, START_SYMBOL)[0])
def test():
    import cPickle as pickle
    table = {}
    while True:
        text = raw_input("> ").decode("utf-8")
        extend_markovtable(table, [START_SYMBOL] * 3 + wakati(text) + [END_SYMBOL] * 3)
        print format_words(greedymarkov(get_keywords(text), table,
                                        START_SYMBOL, START_SYMBOL, START_SYMBOL)[0])

if __name__ == "__main__":
    test()
