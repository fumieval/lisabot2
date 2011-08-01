# coding:utf-8
"""
Lisabot2 actions
"""
from __future__ import unicode_literals
from __future__ import division

import random
import re
import datetime

from pysocialbot.action import Action

from lisabot2.core import vocab, chatter, holiday

IGNORE_SOURCE = ["twittbot.net", "Tumblr", "Google2Tweet"]

WEEKDAY= {0: "月曜日", 1: "火曜日", 2:"水曜日", 3: "木曜日", 4: "金曜日", 5: "土曜日", 6: "日曜日"}

class Post(Action):
    
    """Post specified text."""
    
    def __init__(self, text):
        Action.__init__(self)
        self.text = text
    
    def __call__(self, env):
        return env.api.post(self.text)
    
    def __repr__(self):
        return "post(%s)" & self.text

class Study(Action):
    
    """Study text."""
    
    def __init__(self, status):
        Action.__init__(self)
        self.status = status
        self.text = status.cleaned()
    
    def __call__(self, env):
        if not (self.status.user.protected or self.status.source in IGNORE_SOURCE):
            #twittbotの発言も学習してほしい？　だ が 断 る
            chatter.extend_table(env.markovtable, self.text)
        
        if self.status.in_reply_to_status_id: #会話を学習する
            target = env.api.status(self.status.in_reply_to_status_id)
            env.association.learn(enumerate(chatter.getelements(target.cleaned())),
                                  enumerate(chatter.getelements(self.text)))

        return True
    
    def __repr__(self):
        return "Study('%s')" & self.text

def tweet(env):
    """tweet."""
    return env.api.post(chatter.greedygenerate(env.markovtable, []))

def cleanup(env):
    """Cleanup bad word from markov table."""
    return True

def somniloquy(env):
    """Post somniloquy."""
    return env.api.post(random.choice(vocab.SOMNILOQUY))

def getup(env):
    """Get up tweet."""
    today = datetime.datetime.today()
    if today.weekday() or holiday.holiday_name(datetime.datetime.today):
        return env.api.post("%s %s %s 作業を再開する" % (today.strftime("%m月%d日"),
                             WEEKDAY[today.weekday()]))
    else:
        return env.api.post("起床 " + "00001,00001,00010,00011," * random.randint(0, 1))

def sleep(env):
    """Go to bed tweet."""
    return env.api.post(random.choice(("就寝", "作業中断", "寝る"))+ \
                        random.choice((" 1,1,2,3,",
                                       " 00001,00001,00010,00011,",
                                       "")))

def gethome(env):
    return env.api.post("帰宅")

def poststat(env):
    """Post statistics."""
    #if lisabot2.tz_activity():
    #    text = "タイムライン速度:%g/min" % (env.status_count / 60)
    #else:
    #    text = ""
    #env.status_count = 0
    #        if text:
    #            return env.api.post(text)
    return True
    
def managefriends(env):
    """Manage following. todo: Report as Spam"""
    return True
    env.api.updatefriends()
    def follow(i):
        source = env.api.follow(i)
        if source:
            env.api.post(vocab.follow_l(env) % source.asdict())
            name, conv = source.screen_name, env.conversation
            if name not in conv:
                conv.append(name)
            return name
    lmap = lambda x, y: len(map(x, y))
    return "added %s removed %s" % (lmap(follow, env.api.unrewarded()),
                                    lmap(env.api.remove, env.api.unrequited()))

def reset(env):
    """reset daily variables"""
    env.conversation = []
    return True

def dump(env):    
    """Save Daemon Data."""
    data = {}
    data["status_count"] = env.status_count
    data["impression"] = env.impression
    data["conversation"] = env.conversation

    pickle.dump(data, open(env.param["ENV_PATH"], "w"))
    env.daemon.dump(open(env.param["STATE_PATH"], "w"))
    
    pickle.dump(env.markovtable, open(env.param["DICTIONARY_PATH"], "w"))
    env.association.dump(open(env.param["ASSOCIATION_PATH"], "w"))

    return "Dumped at %s, %s" % (env.param["ENV_PATH"], env.param["STATE_PATH"])
