#coding:utf-8
from __future__ import unicode_literals

import re
import random

FOLLOW = ["@%(screen_name)s フォロー完了",
            "@%(screen_name)s フォロー完了:%(id)d",
            "@%(screen_name)s フォローした",]

FOLLOW_L = ["@%(screen_name)s フォロー完了(遅延あり)",
            "@%(screen_name)s 遅れたがフォローした",]

def follow(env):
    return random.choice(FOLLOW)
def follow_l(env):
    return random.choice(FOLLOW_L)

PATTERN = {"もしゃ":re.compile("もしゃもしゃ|モシャモシャ"),
           "もふ":re.compile("もふもふ|モフモフ"),
           "ぺろ":re.compile("ぺろぺろ|ペロペロ"),
           "ちゅ":re.compile("ちゅっちゅ|チュッチュ"),
           "ぎゅ":re.compile("ぎゅ[っうぅー]?"),
           "ちゃん":re.compile("(リサ|りさ)(ちゃん|チャン)"),
           "リサ":re.compile("リサ(?!イタル|イクル|ージュ|ーチ)"),
           "えっ":re.compile("えっ$"),
           "ほげ":re.compile("ほげ"),
           "REC":re.compile("(●|○)?REC(●|○)?$"),
           "こんにちは":re.compile("こんにちは"),
           "やあ":re.compile("やあ"),
           "rm":re.compile("rm -(rf|fr) (.|/)"),
           "ぬるぽ":re.compile("ぬるぽ|NullPointerException"),
           "早い":re.compile("(フォロー|反応|リプ|リプライ|返信|レス)(が|は)?(早|速)"),
           "PC":re.compile("(どういう)?(PC|パソコン|コンピュータ)を(使って|使用して)(い)?る(の|んだ)?？"),
           "ただいま":re.compile("ただいま[！。ー$][^が]*"),
           "おはよう":re.compile("おはよう[！。ー$][^が]*|お早う[！。][^が]*"),
           "おやすみ":re.compile("(お|御)(やす|休)み[！。ー]?。?$|寝るまーす"),
           "聞きかじった単語を言っただけか":re.compile(r"聞き(かじった|齧った|囓った)(単語|言葉)を言っただけか"),
           "アイ": re.compile(r"虚数単位[iｉ]以外のアイなんてあるの[？\?]|アイって[？\?]"),
           "ぬるぽ": re.compile("NPE|[Nn]ull[Pp]ointer([Ee]xception|[Aa]ssignment)|ぬるぽ|NULLPO|Nullpo|NullPo|nullpo"),
           "5":re.compile("5$|101$"),
           "NagatoBot_End": re.compile("参考になった|……そう|考慮に値する情報として処理させてもらう|面白い人"),
           }

FIBONACCI_SIGN = {"dec":re.compile(r"(1|１)[\s,\.、。]+(1|１)[\s,\.、。]+(2|２)[\s,\.、。]+(3|３)[\s,\.、。]*"),
                  "bin":re.compile(r"1[\s,\.、。]+1[\s,\.、。]+10[\s,\.、。]+11[\s,\.、。]*"),
                  "bin3":re.compile(r"001[\s,\.、。]+001[\s,\.、。]+010[\s,\.、。]+011[\s,\.、。]*"),
                  "bin4":re.compile(r"0001[\s,\.、。]+0001[\s,\.、。]+0010[\s,\.、。]+0011[\s,\.、。]*"),
                  "bin5":re.compile(r"00001[\s,\.、。]+00001[\s,\.、。]+00010[\s,\.、。]+00011[\s,\.、。]*"),
                  "oct":re.compile(r"01[\s,\.、。]+01[\s,\.、。]+02[\s,\.、。]+03[\s,\.、。]*"),
                  "hex":re.compile(r"0x1[\s,\.、。]+0x1[\s,\.、。]+0x2[\s,\.、。]+0x3[\s,\.、。]*"),
                  "hex2":re.compile(r"0x01[\s,\.、。]+0x01[\s,\.、。]+0x02[\s,\.、。]+0x03[\s,\.、。]*"),
                  "jpn":re.compile(r"いち[\s,\.、。]+いち[\s,\.、。]+に[\s,\.、。]+さん[\s,\.、。]*"),
                  "jpn2":re.compile(r"いーち[\s,\.、。]+いーち[\s,\.、。]+にーい[\s,\.、。]+さーん[\s,\.、。]*"),
                  }

SOMNILOQUY = ["zzz…", "(咳)"]