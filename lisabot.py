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
    """run lisabot."""
    options, args = util.getoptions()
    bot = lisabot2.controller.create(DEFAULT_PARAM)
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
            traceback.print_exc()
            print >> sys.stderr, "##END##"
    else:
        if options.debug:
            #bot.debug = True
            try:
                bot.run()
            except KeyboardInterrupt:
                print(action.dump(bot.env))
        else:
            with daemontools.daemoncontext(options.pidfile,
                                           options.logfile,
                                           options.errfile):
                bot.run()

if __name__ == "__main__":
    main()
