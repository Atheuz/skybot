# rock paper scissors game plugin for Skybot
# Written by GhettoWizard(2011)
# http://www.smbc-comics.com/index.php?db=comics&id=2131#comic ??

# "2 people threw rock, 3 threw paper, 5 threw scissors"
# so everyone who threw rock ties once, loses 3 times, wins 5 times, net +2
# and then paper players would get -2, scissors -1

# I would also like the option of specifying a particular person to throw against, which would be done outside of this pool
# so that someone could have a 1v1 without interruption from others

import re
from random import choice

from util import hook

def win(db, nick):
    db.execute("""UPDATE rockpaperscissors SET
               wins = wins+1,
               total = total+1 WHERE nick=?""", (nick.lower(),))
    db.commit()

def loss(db, nick):
    db.execute("""UPDATE rockpaperscissors SET
               losses = losses+1,
               total = total+1 WHERE nick=?""", (nick.lower(),))
    db.commit()

def tie(db, nick):
    db.execute("""UPDATE rockpaperscissors SET
               ties = ties+1,
               total = total+1 WHERE nick=?""", (nick.lower(),))
    db.commit()

@hook.command('rps')
@hook.command()
def rockpaperscissors(inp, nick='', db=None):
    """.rps/.rockpaperscissors <hand>/<stats> -- plays rock-paper-scissors with you or returns stats for all plays"""

    db.execute("""CREATE TABLE if not exists rockpaperscissors(
               nick TEXT PRIMARY KEY,
               wins INTEGER,
               losses INTEGER,
               ties INTEGER,
               total INTEGER)""")

    stats = re.match('stats', inp)
    if stats:
        out = db.execute("""SELECT * FROM rockpaperscissors WHERE nick=?""",
                (nick.lower(),)).fetchall()

        if not out:
            return "no plays"
        else:
            return "you've won %s times, lost %s times, tied %s times and" \
                   " played a total of %s times" % (out[0][1:])

    hands = ['rock', 'paper', 'scissors']
    hand_beats = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}

    if inp and inp.lower() in hands:
        db.execute("""INSERT or IGNORE INTO rockpaperscissors(
                   nick,
                   wins,
                   losses,
                   ties,
                   total) values(?,?,?,?,?)""", (nick.lower(),0,0,0,0))
        player_hand = inp.lower()
        bot_hand = choice(hands)

        if player_hand == bot_hand:
            tie(db, nick)
            return "%s - tie" % bot_hand
        if hand_beats[player_hand] == bot_hand:
            win(db, nick)
            return "%s - you win" % bot_hand
        else:
            loss(db, nick)
            return "%s - you lose" % bot_hand

    return
