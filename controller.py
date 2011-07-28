"""
Controller for Kyorobot
"""

from pysocialbot import daemontools, twitter
from pysocialbot.action import Call
from pysocialbot.botlib.association import Association
from pysocialbot.prototype import bot_twitter_userstream
from pysocialbot.struct import Object
from pysocialbot.trigger import Hourly, DT
from pysocialbot.util import attempt

from lisabot2.settings import TRIGGER, SCREEN_NAME
from lisabot2.core.respond import LisabotStreamHandler

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

    bot.trigger[Hourly(DT(minutes=55))] = Call(dump)
    
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