# coding:utf-8
"""
Lisabot2 actions
"""
from __future__ import unicode_literals
from __future__ import division

import random
import re

from pysocialbot.action import Action

from lisabot2.core import vocab, chatter

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
        if not (self.status.user.protected or self.status.source in ["twittbot.net"]):
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
    return env.api.post(random.choice(("起床", "作業再開", "起きた"))+ \
                        random.choice((" 1,1,2,3,",
                                       " 00001,00001,00010,00011,",
                                       "")))

def sleep(env):
    """Go to bed tweet."""
    return env.api.post(random.choice(("就寝", "作業中断", "寝る"))+ \
                        random.choice((" 1,1,2,3,",
                                       " 00001,00001,00010,00011,",
                                       "")))

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
