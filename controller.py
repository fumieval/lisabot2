"""
Controller for Kyorobot
"""

import cPickle as pickle
import sys
import threading

from pysocialbot import daemontools, twitter
from pysocialbot.action import Call
from pysocialbot.botlib.association import Association
from pysocialbot.prototype import bot_twitter_userstream
from pysocialbot.struct import Object
from pysocialbot.trigger import Hourly, DT
from pysocialbot.util import attempt


from lisabot2.core import action
from lisabot2.settings import TRIGGER, SCREEN_NAME
from lisabot2.core.respond import LisabotStreamHandler

class LisabotController(threading.Thread):
    
    def __init__(self, bot):
        threading.Thread.__init__
        self.bot = bot
        
    def run(self):
        for line in sys.stdin:
            if self.bot.is_alive():
                print("The bot is not aliving")
            command = line.split()
            if command[0] == "do":
                print(repr(self.bot.env.api.post(getattr(action, command[1])(self.bot.env))))
            
def create(param={}):
    """start-up sequence"""
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
    
    bot.env.conversation_count = {}

    try:
        bot.env.markovtable = pickle.load(open(param["DICTIONARY_PATH"], "r"))
    except IOError:
        bot.env.markovtable = {}
    
    assoc = Association()
    attempt(lambda: assoc.load(open(param["ASSOCIATION_PATH"], "r")), IOError)
    bot.env.association = assoc
    
    return bot
