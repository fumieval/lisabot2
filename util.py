"""
lisabot2 utility
"""

import os
import optparse


PATH = os.path.abspath(os.path.dirname(__file__))

def getoptions():
    """get option parameters."""
    parser = optparse.OptionParser()
    parser.add_option("", "--pidfile", dest="pidfile",
                      help="pid file",
                      metavar="FILE",
                      default=os.path.join(PATH, "var/run/lisabot.pid"))
    
    parser.add_option("", "--logfile", dest="logfile",
                      help="log file",
                      metavar="FILE",
                      default=os.path.join(PATH, "var/stdout.log"))
    
    parser.add_option("", "--errfile", dest="errfile",
                      help="error log",
                      metavar="FILE",
                      default=os.path.join(PATH, "var/stderr.log"))
    
    parser.add_option("", "--envfile", dest="envfile",
                      help="environment variables",
                      metavar="FILE",
                      default=os.path.join(PATH, "var/env.dump"))

    parser.add_option("", "--dictfile", dest="dictfile",
                      help="dictionary",
                      metavar="FILE",
                      default=os.path.join(PATH, "var/dict.dump"))
    
    parser.add_option("", "--statefile", dest="statefile",
                      help="state dump file",
                      metavar="FILE",
                      default=os.path.join(PATH, "var/state.dump"))
    
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      help="don't run as daemon",
                      default=False)
    
    return parser.parse_args()
