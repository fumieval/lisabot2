#!/usr/bin/env python
# coding: utf-8
"""
Lisabot controller
"""

import traceback
import signal
import sys

from pysocialbot import daemontools

from lisabot2 import util
from lisabot2.settings import DEFAULT_PARAM

import lisabot2.controller

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
    options, args = util.getoptions()
    
    if options.managed:
        def handler(signum, frame):
            print >> sys.stdout, "Terminating stdout"
            print >> sys.stderr, "Terminating stderr"
        signal.signal(signal.SIGTERM, handler)
        try:
            bot = lisabot2.controller.create(DEFAULT_PARAM)
            lisabot2.controller.LisabotController(bot).start()
            bot.run()
        except:
            print >> sys.stderr, "##START##"
            traceback.print_last()
            print >> sys.stderr, "##END##"
    else:
        if OPTIONS.debug:
            bot.debug = True
            try:
                bot.run()
            except KeyboardInterrupt:
                print(action.dump(bot.env))
        else:
            with daemontools.daemoncontext(OPTIONS.pidfile,
                                           OPTIONS.logfile,
                                           OPTIONS.errfile):
                bot.run()

if __name__ == "__main__":
    main()
