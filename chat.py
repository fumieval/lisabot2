#!/usr/bin/env python
# coding: utf-8
# Author:Fumiexcel
# 会話のテストを行う。
from __future__ import unicode_literals
import os
import cPickle as pickle
import random
from lisabot2.core import chatter

from pysocialbot import twitter

PATH = os.path.abspath(os.path.dirname(__file__))

def main():
    print "Loading..."
    #markovLtoR = {}
    #markovRtoL = {}
    markovLtoR = pickle.load(open(PATH + "/var/env.dump.ltor", "r"))
    markovRtoL = pickle.load(open(PATH + "/var/env.dump.rtol", "r"))
    while True:
        try:
            text = raw_input("> ").decode("utf-8")
        except EOFError:
            break
        except KeyboardInterrupt:
            break

        keywords = chatter.get_keywords(text)
        print chatter.generate(markovLtoR, markovRtoL, keywords)
        chatter.extend_table(markovLtoR, markovRtoL, text)
    pickle.dump(markovLtoR, open(PATH + "/var/markov_ltor", "w"))
    pickle.dump(markovRtoL, open(PATH + "/var/markov_rtol", "w"))
if __name__ == "__main__":
    main()