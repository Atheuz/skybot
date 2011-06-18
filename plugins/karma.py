# Karma plugin for Skybot
# Written by GhettoWizard(2011)

import time
import re

from util import hook, timesince

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

def allowed(db, nick, nick_vote):
    check = db.execute("""SELECT epoch FROM karma_voters WHERE voter=? AND votee=?""",
            (nick.lower(), nick_vote.lower())).fetchone()

    if check:
        check = check[0]
        if time.time() - check >= 3600:
            db.execute("""INSERT OR REPLACE INTO karma_voters(
                       voter,
                       votee,
                       epoch) values(?,?,?)""", (nick.lower(), nick_vote.lower(), time.time()))
            db.commit()
            return True, 0
        else:
            return False, timesince.timeuntil(check, now=time.time()-3600)
    else:
        db.execute("""INSERT OR REPLACE INTO karma_voters(
                   voter,
                   votee,
                   epoch) values(?,?,?)""", (nick.lower(), nick_vote.lower(), time.time()))
        db.commit()
        return True, 0

@hook.command('k')
@hook.command
def karma(inp, nick='', chan='', db=None):
    """.k/.karma <nick><++>/<--> / karma <nick> -- upvotes or downvotes a <nick>'s karma or returns stats for <nick>"""

    db.execute("""CREATE TABLE if not exists karma(
               nick_vote TEXT PRIMARY KEY,
               up_karma INTEGER,
               down_karma INTEGER,
               total_karma INTEGER)""")

    db.execute("""CREATE TABLE if not exists karma_voters(
               voter TEXT,
               votee TEXT,
               epoch FLOAT,
               PRIMARY KEY(voter, votee))""")

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

    vote = re.match('(.+)(\+\+|\-\-)', inp)
    if vote:
        nick_vote = vote.group(1).strip()
        vote_allowed, time_since = allowed(db, nick, nick_vote)
        if vote_allowed:
            if vote.group(2) == '++':
                db.execute("""INSERT or IGNORE INTO karma(
                    nick_vote,
                    up_karma,
                    down_karma,
                    total_karma) values(?,?,?,?)""", (nick_vote.lower(),0,0,0))
                up(db, nick_vote)

            if vote.group(1) == '--':
                db.execute("""INSERT or IGNORE INTO karma(
                    nick_vote,
                    up_karma,
                    down_karma,
                    total_karma) values(?,?,?,?)""", (nick_vote.lower(),0,0,0))
                down(db, nick_vote)
        else:
            return "you can't vote for that person right now, you need to wait %s" % time_since

    return
