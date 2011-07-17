# coding:utf-8
"""
Lisabot2 response library
"""
from __future__ import unicode_literals

import itertools
import random
import datetime
import re

from pysocialbot import launcher
from pysocialbot.twitter import userstream

from lisabot2.core.vocab import PATTERN, FIBONACCI_SIGN
from lisabot2.core import chatter, action, vocab
from lisabot2.settings import TZ_ACTIVITY

IGNORE = re.compile("\.(@\w+ )+|http:\/\/(\w+|\.|\/)*|RT @\w+:?|@\w+")

RT_REGEX = re.compile(r"RT @\w:?.*")
MENTION_REGEX = re.compile(r"[@＠][Ll][Ii][Ss][Aa]_[Mm][Aa][Tt][Hh]\W")
SCREEN_NAME = "Lisa_math"
RESPONSE_THRESHOLD = 3

class LisabotStreamHandler(userstream.StreamHandler):
    
    """Userstream handler."""
    
    def __init__(self, env):
        userstream.StreamHandler.__init__(self)
        self.api = env.api
        self.env = env

    def status(self, status):
        respond(self.env, status)

    def follow(self, source):
        if source.screen_name == "Lisa_math":
            return
        print "New Follower: @%s" % source.screen_name
        self.api.follow(source.id)
        self.api.post(vocab.follow(self.env) % \
                      {"screen_name": source.screen_name,
                       "id": source.id,
                       "name": source.name})
        if not source.screen_name in self.env.conversation:
            self.env.conversation.append(source.screen_name)

def get_response(env, status):
    """Get response message to specified status."""
    
    if 'retweeted_status' in status.__dict__:
        return #リツイートには反応しない

    if not status.user.id in env.impression.__dict__: #印象が未定義の場合初期化
        env.impression.__dict__[status.user.id] = 0
    
    def increment_impression(value):
        """increment the impression."""
        env.impression.__dict__[status.user.id] += value
    
    def withimpression(value, increment=0):
        """return value with changing impression."""
        increment_impression(increment)
        return value
    
    def choice_i(data, els):
        """choice response by impression."""
        for i in data:
            if env.impression.__dict__[status.user.id] >= i[0]:
                if len(i) == 3:
                    increment_impression(i[2])
                return random.choice(i[1])
        
        if len(els) == 2:
            increment_impression(els[1])
        return random.choice(els[0])  
   
    check = lambda i: PATTERN[i].search(status.text)
    
    if status.in_reply_to_screen_name == SCREEN_NAME: #自分宛
        if check("もしゃ") or check("もふ"):
            return choice_i([(15, ["@%(id)s きゃうん！",
                                   "@%(id)s きゃうん…",
                                   "@%(id)s きゃん！",
                                   "@%(id)s ……コンティニュー//",
                                   "@%(id)s ……つづけて//",
                                   "@%(id)s やめて…",], -1),
                             (4, ["@%(id)s きゃうん！",
                                  "@%(id)s きゃうん…",
                                  "@%(id)s きゃうん…",
                                  "@%(id)s きゃん！",
                                  "@%(id)s やめて",
                                  "@%(id)s だめ",
                                  "@%(id)s やめて、%(name)s氏"])
                             ],
                             (["@%(id)s やめて、%(name)s氏",
                               "@%(id)s %(name)s氏、やめて",
                               "@%(id)s やめて…",
                               "@%(id)s だめ",
                               "@%(id)s やめて"], 1))
        elif check("ぎゅ"):
            return choice_i([(20, ["@%(id)s きゃうん！",
                                  "@%(id)s きゃうっ！",
                                  "@%(id)s きゃん！",
                                  "@%(id)s やめて、%(name)s氏",
                                  "@%(id)s %(name)s氏、やめて"])],
                            (["@%(id)s やめて、%(name)s氏",
                              "@%(id)s %(name)s氏、やめて",
                              "@%(id)s やめて…","@%(id)s だめ",
                              "@%(id)s やめて"], -2))   
        elif check("ぺろ") or check("ちゅ"):
            return choice_i([(6, ["@%(id)s きゃうん！",
                                  "@%(id)s きゃうん…",
                                  "@%(id)s きゃん！",
                                  "@%(id)s やめて、%(name)s氏",
                                  "@%(id)s %(name)s氏、やめて"])
                                  ],
                            (["@%(id)s やめて、%(name)s氏",
                              "@%(id)s %(name)s氏、やめて",
                              "@%(id)s やめて…",
                              "@%(id)s やめて"], -2)) 
        elif check("早い"):
            return "@%(id)s UserStreamを使っているから"
        elif check("rm"):
            return random.choice(["@%(id)s Deny","@%(id)s Permission Denied"])
        elif check("やあ"):
            return withimpression("@%(id)s やあ", 1)
        elif check("PC"):
            return "@%(id)s Dvorak配列で、キートップに何も記されていないノートPC"
        elif check("ほげ"):
            return "@%(id)s ほげ"
        elif check("えっ"):
            return "@%(id)s えっ"


    if status.in_reply_to_screen_name == None or \
       status.in_reply_to_screen_name == SCREEN_NAME:

        #フィボナッチ・サインの判定
        fib = lambda i:FIBONACCI_SIGN[i].search(status.text)
        if fib("dec"):
            return withimpression("@%(id)s 5", 2)
        elif fib("bin") or fib("bin3"):
            return withimpression("@%(id)s 101", 2)
        elif fib("bin4"):
            return withimpression("@%(id)s 0101", 2)
        elif fib("bin5"):
            return withimpression("@%(id)s 00101", 2)
        elif fib("oct"):
            return withimpression("@%(id)s 05", 2)
        elif fib("hex"):
            return withimpression("@%(id)s 0x5", 2)
        elif fib("hex2"):
            return withimpression("@%(id)s 0x05", 2)
        elif fib("jpn") or fib("jpn2"):
            return withimpression("@%(id)s ご", 2)

        if check("ちゃん"):
            return "@%(id)s 《ちゃん》は不要"

        elements = chatter.get_elements(IGNORE.sub("", status.text))
        if elements:
            assoc, score = env.association.extract(elements)
    
        if MENTION_REGEX.search(status.text) and elements:
            if assoc:
                return withimpression("@%(id)s " + \
                                      chatter.greedygenerate(env.markovtable, assoc), 1)
            else:
                return withimpression("@%(id)s " + \
                                      chatter.greedygenerate(env.markovtable, elements), 1)                
        
        if score >= RESPONSE_THRESHOLD:
            return withimpression("@%(id)s " + \
                                  chatter.greedygenerate(env.markovtable, assoc), 1)            

        if check("リサ"):
            env.api.favorite(status.id)
            return withimpression(None, 1)

def respond(env, status):
    """Respond to specified status."""
    if status.user.screen_name == SCREEN_NAME:
        return #自分の発言は無視
    
    now = datetime.datetime.utcnow() #現在の時間を取得
    status.text = RT_REGEX.sub("", status.text).strip() #RTを取り除いた本文を取得
    context = {"id": status.user.screen_name,
               "name": status.user.name,
               "text": status.text,
               "created_at": status.created_at,
               "now": now.strftime("%a %b %d %H:%M:%S +0000 %Y")}
    
    env.status_count += 1

    if "#ping" in status.text:
        env.api.reply(status.id,
                      "@%(id)s #pong %(now)s (#ping %(created_at)s)" %
                      context)
        return

    if not TZ_ACTIVITY(env):
        return #寝ている間は反応しない
    
    if "下校時間です" in status.text:
        if status.user.screen_name == "mizutani_j_bot":
            if env.conversation:
                env.api.post(".%s 《下校》" %
                         reduce(lambda a, b:a + " " + b
                                if len(a + b) <= 135 else "",
                                itertools.imap(lambda x: "@" + x,
                                               env.conversation)))
            else:
                env.api.post("帰る")
        else:
            env.api.reply(status.id, "@%(id)s えっ" % context)
        return

    if re.search("虚数単位[iｉ]以外のアイなんてあるの[？\?]|アイって[？\?]", status.text):
        env.api.reply(status.id,
                      random.choice(["@%(id)s Iterationのi",
                                     "@%(id)s Indexのi",
                                     "@%(id)s Integerのi"]) % context)
        return

    response = get_response(env, status)
    if response:
        if not status.user.screen_name in env.conversation:
            env.conversation.append(status.user.screen_name)
        env.api.reply(status.id,
                      response.replace(chatter.END_SYMBOL,"") % context)
    if not status.user.protected and status.source != "twittbot.net":
        env.daemon.put(launcher.Trigger(), action.Study(status)) #学習させるタスクを追加
    if status.in_reply_to_status_id:
        target = env.api.status(status.in_reply_to_status_id)
        env.association.learn(chatter.get_elements(target.text),
                              chatter.get_elements(status.text))