# coding:utf-8
"""
Lisabot2 actions
"""
from __future__ import unicode_literals
from __future__ import division

import random
import re
import xml.sax.saxutils

from pysocialbot import launcher
#from pysocialbot.twitter import userstream
from lisabot2.core import vocab, chatter


IGNORE = re.compile("\.(@\w+ )+|http:\/\/(\w+|\.|\/)*|RT @\w+:?|#\w+|@\w+")

class Tweet(launcher.Action):
    
    """tweet."""
    
    def __call__(self, env):
        return env.api.post(chatter.greedygenerate(env.markovtable, []))
    
    def __repr__(self):
        return "random tweet"

class Cleanup(launcher.Action):
    
    """Cleanup bad word from markov table."""
    
    def __call__(self, env):
        
        #for key in env.markovLtoR:
        #    if not NGWORD.search(' '.join(key)):
        #        del env.markovLtoR[key]
        #for key in env.markovRtoL:
        #    if NGWORD.search(' '.join(key)):
        #        del env.markovRtoL[key]
        return True
    
    def __repr__(self):
        return "clean up bad words"


class Somniloquy(launcher.Action):
    
    """Post somniloquy."""
    
    def __call__(self, env):
        return env.api.post(random.choice(vocab.SOMNILOQUY))
    
    def __repr__(self):
        return "somniloquy tweet"


class Getup(launcher.Action):
    
    """Get up tweet."""
    
    def __call__(self, env):
        return env.api.post(random.choice(("起床", "作業再開", "起きた"))+ \
                            random.choice((" 1,1,2,3,",
                                           " 00001,00001,00010,00011,",
                                           "")))
        
    def __repr__(self):
        return "get up tweet"

class Sleep(launcher.Action):
    
    """Go to bed tweet."""
    
    def __call__(self, env):
        return env.api.post(random.choice(("就寝", "作業中断", "寝る"))+ \
                            random.choice((" 1,1,2,3,",
                                           " 00001,00001,00010,00011,",
                                           "")))
        
    def __repr__(self):
        return "go to bed tweet"

class Post(launcher.Action):
    
    """Post specified text."""
    
    def __init__(self, text):
        launcher.Action.__init__(self)
        self.text = text
    
    def __call__(self, env):
        return env.api.post(self.text)
    
    def __repr__(self):
        return "post(%s)" & self.text

class Study(launcher.Action):
    
    """Study text."""
    
    def __init__(self, status):
        launcher.Action.__init__(self)
        self.text = status.cleaned()
    
    def __call__(self, env):
        chatter.extend_table(env.markovtable, self.text)
        return True
    
    def __repr__(self):
        return "Study('%s')" & self.text

class Poststat(launcher.Action):
    
    """Post statistics."""
    
    def __call__(self, env):
        
        #if lisabot2.tz_activity():
        #    text = "タイムライン速度:%g/min" % (env.status_count / 60)
        #else:
        #    text = ""
        #env.status_count = 0
#        if text:
#            return env.api.post(text)
        return True         
    
    def __repr__(self):
        return "post statistics"

class Debugstat(launcher.Action):
    
    """Debug informations."""
    
    def __call__(self, env):
        return True
    
    def __repr__(self):
        return "print debug informations"

class Managefriends(launcher.Action):#フォロー管理
    
    """Manage following. todo: Report as Spam"""
    
    def __call__(self, env):
        env.api.updatefriends()

        def follow(i):
            source = env.api.follow(i)
            if source:
                env.api.post(vocab.follow_l(env) % source.asdict())
                name, conv = source.screen_name, env.conversation
                return (name in conv or conv.append(name), name)[1]
        lmap = lambda x, y: len(map(x, y))
        return "added %s removed %s" % (lmap(follow, env.api.unrewarded()),
                                        lmap(env.api.remove,
                                             env.api.unrequited()))
    
    def __repr__(self):
        return "manage following"

class Reset(launcher.Action):
    
    """Reset internal state."""
    
    def __call__(self, env):
        #env.stream = userstream.UserStream(env.api, LisabotStreamHandler(env))
        env.conversation = []
        return True
    
    def __repr__(self):
        return "reset daily variables"
