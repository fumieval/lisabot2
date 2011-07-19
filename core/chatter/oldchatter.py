
def isAlphabetonly(string):
    return all(itertools.imap(lambda x: ord(x) & 0x70 and ord(x) < 128, string))

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
