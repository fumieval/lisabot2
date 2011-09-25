"""
Controller for Kyorobot
"""

import cPickle as pickle
import sys
import threading
import traceback
from itertools import imap, takewhile, repeat

from pysocialbot.botlib.association import Association
from pysocialbot.prototype import bot_twitter_userstream
from pysocialbot.struct import Object
from pysocialbot.util import attempt


from lisabot2.core import action
from lisabot2.settings import TRIGGER, SCREEN_NAME
from lisabot2.core.respond import LisabotStreamHandler

class LisabotController(threading.Thread):
    
    def __init__(self, bot):
        threading.Thread.__init__(self)
        self.daemon = True
        self.bot = bot
        
    def run(self):
        print("Controller started.")
        while True:
            line = ""
            while True:
                c = url.read(1)
                if c == "\n":
                    break
                line += c
            command = t.split()
            if command[0] == "do":
                try:
                    print(getattr(action, command[1])(self.bot.env))
                except:
                    print >> sys.stderr, "##START##"
                    traceback.print_exc()
                    print >> sys.stderr, "##END##"
            elif command[0] == "post":
                try:
                    print(self.bot.env.api.post(' '.join(command[1:])))
                except:
                    print >> sys.stderr, "##START##"
                    traceback.print_exc()
                    print >> sys.stderr, "##END##"
            elif command[0] == "retweet":
                try:
                    print(self.bot.env.api.retweet(command[1]))
                except:
                    print >> sys.stderr, "##START##"
                    traceback.print_exc()
                    print >> sys.stderr, "##END##"

            
def create(param={}):
    """start-up sequence."""
    try:
        env = Object(pickle.load(open(param["ENV_PATH"], "r")))
    except IOError:
        env = Object()
    
    env.param = param
    
    bot = bot_twitter_userstream(env,
                                 SCREEN_NAME,
                                 TRIGGER,
                                 LisabotStreamHandler)
    bot.reset()
    attempt(lambda: bot.load(open(param["STATE_PATH"], "r")), IOError)
    
    env.conversation_count = {}
    try:
        env.markovtable = pickle.load(open(param["DICTIONARY_PATH"], "r"))
    except:
        env.markovtable = {}
    
    assoc = Association()
    attempt(lambda: assoc.load(open(param["ASSOCIATION_PATH"], "r")), IOError)
    env.association = assoc
    
    return bot
