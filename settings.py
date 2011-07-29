"""
Lisabot settings
"""

import os

from pysocialbot.trigger import (dailysection, InDailyPeriod,
                                  Regular, Hourly, Daily, Randomly, 
                                  DT)
from pysocialbot.action import Call
from lisabot2.core import action

PATH = os.path.abspath(os.path.dirname(__file__))

TZ_ACTIVITY = InDailyPeriod(dailysection(6, 30), dailysection(23, 45))
TZ_REMSLEEP = InDailyPeriod(dailysection(0, 0), dailysection(5, 30))

TRIGGER = {Daily(DT(hours=6, minutes=30)): Call(action.getup),
           TZ_ACTIVITY & Regular(5) & Randomly(0.0003): Call(action.tweet),
           Daily(DT(hours=23, minutes=30)): Call(action.sleep),
           TZ_REMSLEEP & Regular(10) & Randomly(0.0001): Call(action.somniloquy),
                      
           Hourly(DT(minutes=10)): Call(action.managefriends),

           Hourly(DT(minutes=55)): Call(action.dump),
           Daily(): Call(action.reset),
           }


DEFAULT_PARAM = {"ENV_PATH": PATH + "/var/env.dump",
                 "STATE_PATH": PATH + "/var/state.dump",
                 "DICTIONARY_PATH": PATH + "/var/dict.dump",
                 "ASSOCIATION_PATH": PATH + "/var/dict.dump.assoc",
                 }

SCREEN_NAME = "Lisa_math"
