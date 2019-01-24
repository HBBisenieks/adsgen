from __future__ import unicode_literals
from builtins import str
from unidecode import unidecode
from re import sub


def decode(s):
    return unidecode(str(s))


def sanitize(s):
    return sub('[ \']', '', s)


def sane(s):
    return sanitize(decode(s))
