# rock paper scissors game plugin for Skybot
# Written by GhettoWizard(2011)

import re
from random import choice

from util import hook

def win(db, chan, nick):
    db.execute("""INSERT or IGNORE INTO rockpaperscissors(
               nick,
               chan,
               wins,
               losses,
               ties,
               total) values(?,?,?,?,?,?)
               """, (nick.lower(),chan.lower(),0,0,0,0))
    db.execute("""UPDATE rockpaperscissors SET
               wins = wins+1,
               total = total+1
               WHERE nick=? AND chan=?""", (nick.lower(), chan.lower()))
    db.commit()

def loss(db, chan, nick):
    db.execute("""INSERT or IGNORE INTO rockpaperscissors(
               nick,
               chan,
               wins,
               losses,
               ties,
               total) values(?,?,?,?,?,?)
               """, (nick.lower(),chan.lower(),0,0,0,0))
    db.execute("""UPDATE rockpaperscissors SET
               losses = losses+1,
               total = total+1
               WHERE nick=? AND chan=?""", (nick.lower(), chan.lower()))
    db.commit()

def tie(db, chan, nick):
    db.execute("""INSERT or IGNORE INTO rockpaperscissors(
               nick,
               chan,
               wins,
               losses,
               ties,
               total) values(?,?,?,?,?,?)
               """, (nick.lower(),chan.lower(),0,0,0,0))
    db.execute("""UPDATE rockpaperscissors SET
               ties = ties+1,
               total = total+1
               WHERE nick=? AND chan=?""", (nick.lower(), chan.lower()))
    db.commit()

def get_stats(db, chan, nick):
    return db.execute("""SELECT * FROM rockpaperscissors WHERE nick=? AND chan=?""", ( nick.lower(), chan.lower() ) ).fetchall()

@hook.command('rps')
@hook.command()
def rockpaperscissors(inp, nick='', chan='', db=None):
    """.rps/.rockpaperscissors <hand>/<stats> -- plays rock-paper-scissors with
    you or returns stats for all plays"""

    stats = re.match('stats', inp)
    if stats:
        out = get_stats(db, chan, nick)

        if not out:
            return "no plays"
        else:
            return "you've won %s times, lost %s times, tied %s times and" \
                   " played a total of %s times" % (out[0][2:])

    hands = ['rock', 'paper', 'scissors']

    db.execute("""CREATE TABLE if not exists rockpaperscissors(
               nick TEXT PRIMARY KEY,
               chan TEXT,
               wins INTEGER,
               losses INTEGER,
               ties INTEGER,
               total INTEGER)
               """)

    if inp and inp.lower() in hands:
        player_hand = inp.lower()
        bot_hand = choice(hands)

        if player_hand == bot_hand:
            tie(db, chan, nick)
            return "%s - tie" % bot_hand
        if player_hand == 'rock':
            if bot_hand == 'paper':
                loss(db, chan, nick)
                return "%s - you lose" % bot_hand
            if bot_hand == 'scissors':
                win(db, chan, nick)
                return "%s - you win" % bot_hand
        if player_hand == 'paper':
            if bot_hand == 'scissors':
                loss(db, chan, nick)
                return "%s - you lose" % bot_hand
            if bot_hand == 'rock':
                win(db, chan, nick)
                return "%s - you win" % bot_hand
        if player_hand == 'scissors':
            if bot_hand == 'rock':
                loss(db, chan, nick)
                return "%s - you lose" % bot_hand
            if bot_hand == 'paper':
                win(db, chan, nick)
                return "%s - you win" % bot_hand
    else:
        return
