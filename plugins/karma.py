# Karma plugin for Skybot
# Written by GhettoWizard(2011)

from util import hook


@hook.command('k')
@hook.command
def karma(inp, db=None):
    """.k/.karma <up>/<down> <nick> / <karma> <nick> -- either ups or downs a nick's karma or gets karma stats for nick"""

    db.execute("""CREATE TABLE if not exists karma(
               nick TEXT PRIMARY KEY,
               up_karma INTEGER,
               down_karma INTEGER,
               total_karma INTEGER)""")

    karma_stats = re.match('karma', inp)
    if karma_stats:
        out = db.execute("""SELECT * FROM karma WHERE nick=?""",
                (inp.lower(),)).fetchall()

        if not out:
            return "no karma"
        else:
            return "%s has %s positive karma, %s negative karma, %s total"
                    " karma" % (out[0])

    return inp

