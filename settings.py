"""
Lisabot settings
"""

from pysocialbot.trigger import (dailysection, InDailyPeriod,
                                  Regular, Hourly, Daily, Randomly, 
                                  DT)
from pysocialbot.action import Call
from lisabot2.core import action

TZ_ACTIVITY = InDailyPeriod(dailysection(6, 30), dailysection(23, 45))
TZ_REMSLEEP = InDailyPeriod(dailysection(0, 0), dailysection(5, 30))

TRIGGER = {TZ_ACTIVITY & Regular(5) & Randomly(0.0003): Call(action.tweet),
           TZ_REMSLEEP & Regular(10) & Randomly(0.0001): Call(action.somniloquy),
           Hourly(): Call(action.poststat),
           Hourly(DT(minutes=10)): Call(action.managefriends),
           Daily(DT(hours=6, minutes=30)): Call(action.getup),
           Daily(DT(hours=23, minutes=30)): Call(action.sleep),
           Daily(): Call(action.reset),
           }

SCREEN_NAME = "Lisa_math"