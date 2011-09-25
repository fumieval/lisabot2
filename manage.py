#!/usr/bin/python
"""
Lisabot Manager
"""

import os
from pysocialbot.twitter import management
from pysocialbot import daemontools

PATH = os.path.abspath(os.path.dirname(__file__))

RUNPATH = os.path.join(PATH, "var/run")

param = {"screen_name": "Lisa_math",
         "SCRIPT": os.path.join(PATH, "lisabot.py"),
         "RUNPATH": RUNPATH,
         "PIDFILE": os.path.join(RUNPATH, "lisabot.pid")
         }

if __name__ == "__main__":
    management.execute_manager(param, daemontools.DAEMONTOOLS_COMMAND)
