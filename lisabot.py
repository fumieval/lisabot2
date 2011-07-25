#!/usr/bin/env python
# coding: utf-8
"""
Lisabot controller
"""
try:
    import cPickle as pickle
except ImportError:
    import pickle

from pysocialbot import daemontools, twitter
from pysocialbot.action import Call
from pysocialbot.botlib.association import Association
from pysocialbot.prototype import bot_twitter_userstream
from pysocialbot.struct import Object
from pysocialbot.trigger import Hourly, DT
from pysocialbot.util import attempt

from lisabot2 import util
from lisabot2.settings import TRIGGER, SCREEN_NAME
from lisabot2.core.respond import LisabotStreamHandler

OPTIONS, ARGS = util.getoptions()

def dump(env):    
    """Save Daemon Data."""
    data = {}
    data["status_count"] = env.status_count
    data["impression"] = env.impression
    data["conversation"] = env.conversation

    pickle.dump(data, open(OPTIONS.envfile, "w"))
    pickle.dump(env.markovtable, open(OPTIONS.dictfile, "w"))
    env.association.dump(open(OPTIONS.dictfile + ".assoc", "w"))
    env.daemon.dump(open(OPTIONS.statefile, "w"))
        
    return "Dumped at %s, %s" % (OPTIONS.envfile, OPTIONS.statefile)

def createbot(env, screen_name, triggers, handler):
    """Create minimal twitter-bot using UserStream."""
    bot = Daemon(env)
    bot.trigger = triggers

    bot.env.api = twitter.Api(screen_name)
    bot.env.stream = UserStream(bot.env.api, handler(bot.env))
    
    bot.hooks.append(lambda env: env.stream.start())
    return bot

def main():
    """run lisabot.
    1.環境変数を読み込む
    2.Botのインスタンスを作成
    3.データのダンプのスケジュールを追加
    4.ステートの読み込み
    5.マルコフ連鎖表の読み込み
    6.連想記憶の読み込み
    7.実行
    """
    
    try:
        env = Object(pickle.load(open(OPTIONS.envfile, "r")))
    except IOError:
        env = Object()
    
    bot = bot_twitter_userstream(env,
                                 SCREEN_NAME,
                                 TRIGGER,
                                 LisabotStreamHandler)

    bot.trigger[Hourly(DT(minutes=55))] = Call(dump)
    
    bot.reset()
    attempt(lambda: bot.load(open(OPTIONS.statefile, "r")), IOError)
    
    bot.env.impression = bot.env.impression.asdict() #PySocialBot 0.3.0に移行したら消す

    try:
        bot.env.markovtable = pickle.load(open(OPTIONS.dictfile, "r"))
    except IOError:
        bot.env.markovtable = {}
    
    assoc = Association()
    attempt(lambda: assoc.load(open(OPTIONS.dictfile + ".assoc", "r")), IOError)
    bot.env.association = assoc

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
