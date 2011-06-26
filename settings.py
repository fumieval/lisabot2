"""
Lisabot settings
"""

from pysocialbot.launcher import (dailysection, InDailyPeriod,
                                  Regular, Hourly, Daily, Randomly, 
                                  DT)
from lisabot2.core import action

TZ_ACTIVITY = InDailyPeriod(dailysection(6, 30), dailysection(23, 0))
TZ_REMSLEEP = InDailyPeriod(dailysection(0, 0), dailysection(5, 30))

TRIGGER = {TZ_ACTIVITY & Regular(5) & Randomly(0.0003): action.Tweet(),
           TZ_REMSLEEP & Regular(10) & Randomly(0.0001): action.Somniloquy(),
           Hourly(): action.Poststat(),
           Hourly(DT(minutes=10)): action.Managefriends(),
           Daily(DT(hours=6, minutes=30)): action.Getup(),
           Daily(DT(hours=23, minutes=30)): action.Sleep(),
           Daily(): action.Reset(),
           }