import hashlib

from util import hook


@hook.command
def md5(inp):
    """.md5 <text> -- returns MD5 hash of <text>"""
    return hashlib.md5(inp).hexdigest()


@hook.command
def sha1(inp):
    """.md5 <text> -- returns SHA1 hash of <text>"""
    return hashlib.sha1(inp).hexdigest()


@hook.command
def hash(inp):
    """.hash <text> -- returns hashes of <text>"""
    return ', '.join(x + ": " + getattr(hashlib, x)(inp).hexdigest()
            for x in 'md5 sha1 sha256'.split())
