#!/usr/bin/env python
"""
Lisabot controller
"""
try:
    import cPickle as pickle
except ImportError:
    import pickle

from pysocialbot import daemontools, twitter
from pysocialbot.launcher import Daemon, Action, Hourly, DT
from pysocialbot.util import attempt
from pysocialbot.util.convert import convert_object
from pysocialbot.twitter.userstream import UserStream
from pysocialbot.botlib.association import Association

from lisabot2 import util
from lisabot2.settings import TRIGGER
from lisabot2.core.respond import LisabotStreamHandler

OPTIONS, ARGS = util.getoptions()

class Dump(Action):
    
    """Save Daemon Data."""
    
    def __call__(self, env):
        data = {}
        data["status_count"] = env.status_count
        data["impression"] = env.impression
        data["conversation"] = env.conversation

        pickle.dump(data, open(OPTIONS.envfile, "w"))
        pickle.dump(env.markovtable, open(OPTIONS.dictfile, "w"))
        env.association.dump(open(OPTIONS.dictfile + ".assoc", "w"))
        env.daemon.dumpstate(open(OPTIONS.statefile, "w"))
        
        return "Dumped at %s, %s" % (OPTIONS.envfile, OPTIONS.statefile)

    def __repr__(self):
        return "dump environment variables"
    
def createbot(env):
    """Create minimal twitter-bot using UserStream."""
    bot = Daemon(env)
    bot.trigger = TRIGGER

    bot.env.api = twitter.Api("Lisa_math")
    bot.env.stream = UserStream(bot.env.api, LisabotStreamHandler(bot.env))
    
    bot.hooks.append(lambda env: env.stream.start())
    return bot

def main():
    """run lisabot."""
    dumpdata = Dump()

    bot = \
    createbot(convert_object(pickle.load(open(OPTIONS.envfile, "r"))))

    bot.trigger[Hourly(DT(minutes=55))] = dumpdata
    
    bot.resetstate()
    attempt(lambda: bot.loadstate(open(OPTIONS.statefile, "r")), IOError)
    
    #bot.env.markovtable = {}
    bot.env.markovtable = pickle.load(open(OPTIONS.dictfile, "r"))

    bot.env.association = Association()
    bot.env.association.load(open(OPTIONS.dictfile + ".assoc", "r"))
    if OPTIONS.debug:
        try:
            bot.run()
        except KeyboardInterrupt:
            print(dumpdata(bot.env))
    else:
        with daemontools.daemoncontext(OPTIONS.pidfile,
                                       OPTIONS.logfile,
                                       OPTIONS.errfile):
            bot.run()

if __name__ == "__main__":
    main()