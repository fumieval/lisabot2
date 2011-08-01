# coding:utf-8
"""
Lisabot2 response library
"""
from __future__ import unicode_literals

import itertools
import random
import datetime
import re

from pysocialbot import trigger
from pysocialbot.twitter import userstream

from lisabot2.core.vocab import PATTERN, FIBONACCI_SIGN
from lisabot2.core import chatter, action, vocab
from lisabot2.settings import TZ_ACTIVITY, SCREEN_NAME

RT_REGEX = re.compile(r"(RT|QT) @\w:?.*")
REPLY_REGEX = re.compile(r"^\.?[@＠][Ll][Ii][Ss][Aa]_[Mm][Aa][Tt][Hh]\W")
MENTION_REGEX = re.compile(r"[@＠][Ll][Ii][Ss][Aa]_[Mm][Aa][Tt][Hh]\W")

RESPONSE_THRESHOLD = 3
CONVERSATION_LIMIT = 16

class LisabotStreamHandler(userstream.StreamHandler):
    
    """Userstream handler."""
    
    def __init__(self, env):
        userstream.StreamHandler.__init__(self)
        self.api = env.api
        self.env = env

    def status(self, status):
        respond(self.env, status)

    def follow(self, source):
        if source.screen_name == SCREEN_NAME:
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
        return

    if not status.user.id in env.impression:
        env.impression[status.user.id] = 0
    
    def increment_impression(value):
        """increment the impression."""
        env.impression[status.user.id] += value
    
    def withimpression(value, increment=0):
        """return value with changing impression."""
        increment_impression(increment)
        return value
    
    def choice_i(data, els):
        """choice response by impression."""
        for i in data:
            if env.impression[status.user.id] >= i[0]:
                if len(i) == 3:
                    increment_impression(i[2])
                return random.choice(i[1])
        
        if len(els) == 2:
            increment_impression(els[1])
        return random.choice(els[0])  

    def check(pattern):
        return PATTERN[pattern].search(status.text)

    isreply = bool(REPLY_REGEX.search(status.text))
    ismentions = isreply or bool(MENTION_REGEX.search(status.text))
    
    #todo: これらの汚い条件文をpysocialbot.botlib.patternに置き換える
    if isreply:
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
        elif check("なで"):
            choice_i([(3, ["@%(id)s ……", "@%(id)s つづけて"])],
                            (["@%(id)s 邪魔しないで", "@%(id)s 不要"], 0))
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
        elif check("rm") or check("REC"):
            return random.choice(["@%(id)s Deny", "@%(id)s Permission Denied"])
        elif check("アイ"):
            return random.choice(["@%(id)s Iterationのi",
                                  "@%(id)s Indexのi",
                                  "@%(id)s Integerのi"])
        
        elif check("PC"):
            return "@%(id)s Dvorak配列で、キートップに何も記されていないノートPC"
        
        elif check("NagatoBot_End"):
            return None

    if status.in_reply_to_screen_name == None or \
    status.in_reply_to_screen_name == SCREEN_NAME:

        #フィボナッチ・サインの判定
        fib = lambda i: FIBONACCI_SIGN[i].search(status.text)
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
            env.api.favorite(status.id)
            return "@%(id)s 《ちゃん》は不要"

        elements = chatter.getelements(status.cleaned())
        if elements:
            assoc, score = env.association.extract(elements, random.randint(3, 6))
            assoc = map(lambda x: x[1], assoc)
            if ismentions: #基本的にメンションには反応する
                keywords = chatter.getkeywords(status.cleaned())
                text = chatter.greedygenerate(env.markovtable, assoc + keywords)
                if text:
                    return withimpression("@%(id)s " + text, 1)
            else:
                if status.in_reply_to_screen_name == None and \
                score >= len(elements) * RESPONSE_THRESHOLD:
                    keywords = chatter.getkeywords(status.cleaned())
                    text = chatter.greedygenerate(env.markovtable, assoc + keywords)
                    if text:
                        return withimpression("@%(id)s " + text, 1)

    if check("リサ"):
        env.api.favorite(status.id)
        return withimpression(None, 1)

def respond(env, status):
    """Respond to specified status."""
    if status.user.screen_name == SCREEN_NAME:
        return #Ignore the status that created by oneself
    
    now = datetime.datetime.utcnow()
    status.text = RT_REGEX.sub("", status.text).strip()
    context = {"id": status.user.screen_name,
               "name": status.user.name,
               "text": status.text,
               "created_at": status.created_at,
               "now": now.strftime("%a %b %d %H:%M:%S +0000 %Y")}
    
    env.status_count += 1

    if "#ping" in status.text:
        env.api.reply(status.id,
                      "@%(id)s #pong %(now)s ( #ping %(created_at)s)" %
                      context)
        return

    if not TZ_ACTIVITY(env):
        return #The bot doesn't respond during It's sleeping
    
    if status.in_reply_to_status_id:
        if status.id in env.conversation_count:
            env.conversation_count[status.id] = env.conversation_count[status.in_reply_to_status_id] + 1
            del env.conversation_count[status.in_reply_to_status_id]
        else:
            env.conversation_count[status.id] = 0

        if env.conversation_count[status.id] >= CONVERSATION_LIMIT:
            del env.conversation_count[status.id]
            return

    if "下校時間です" in status.text:
        if status.user.screen_name == "mizutani_j_bot":
            if env.conversation: #今日会話した人に下校を知らせる
                env.api.post(".%s 《下校》" % \
                reduce(lambda a, b: a + " " + b if len(a + b) <= 134 else "",
                       itertools.imap(lambda x: "@" + x, env.conversation)))
            else: #ぼっち
                env.api.post("帰る")
        else: #お前瑞谷女史じゃないだろ
            env.api.reply(status.id, "@%(id)s えっ" % context)
        return

    response = get_response(env, status)
    if response:
        if not status.user.screen_name in env.conversation and \
           status.in_reply_to_screen_name == SCREEN_NAME:
            env.conversation.append(status.user.screen_name)
        env.api.reply(status.id, (response % context)[:140])

    env.daemon.push(trigger.Trigger(), action.Study(status))
