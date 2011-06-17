# Karma plugin for Skybot
# Written by GhettoWizard(2011)

import re

from util import hook

def up(db, nick_vote):
    db.execute("""UPDATE karma SET
               up_karma = up_karma+1,
               total_karma = total_karma+1 WHERE nick_vote=?""", (nick_vote.lower(),))
    db.commit()

def down(db, nick_vote):
    db.execute("""UPDATE karma SET
               down_karma = down_karma+1,
               total_karma = total_karma+1 WHERE nick_vote=?""", (nick_vote.lower(),))
    db.commit()

@hook.command('k')
@hook.command
def karma(inp, chan='', db=None):
    """.k/.karma <up>/<down> <nick_vote> / <karma> <nick_vote> -- either ups or downs a nick's karma or gets karma stats for nick"""

    db.execute("""CREATE TABLE if not exists karma(
               nick_vote TEXT PRIMARY KEY,
               up_karma INTEGER,
               down_karma INTEGER,
               total_karma INTEGER)""")

    if not chan.startswith('#'):
        return

    karma_stats = re.match('(stats) (.+)', inp)
    if karma_stats:
        nick_vote = karma_stats.group(2)
        out = db.execute("""SELECT * FROM karma WHERE nick_vote=?""",
                (nick_vote.lower(),)).fetchall()

        if not out:
            return "no karma"
        else:
            out = out[0]
            return "%s has %s karma" % (nick_vote, out[1]-out[2])

    vote = re.match('(up|down) (.+)', inp)
    if vote:
        nick_vote = vote.group(2)
        if vote.group(1) == 'up':
            db.execute("""INSERT or IGNORE INTO karma(
                   nick_vote,
                   up_karma,
                   down_karma,
                   total_karma) values(?,?,?,?)""", (nick_vote.lower(),0,0,0))
            up(db, nick_vote)

        if vote.group(1) == 'down':
            db.execute("""INSERT or IGNORE INTO karma(
                   nick_vote,
                   up_karma,
                   down_karma,
                   total_karma) values(?,?,?,?)""", (nick_vote.lower(),0,0,0))
            down(db, nick_vote)

    return
