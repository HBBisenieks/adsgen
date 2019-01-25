from unidecode import unidecode
from re import sub


def decode(s):
    return unidecode(s)


def sanitize(s):
    return sub('[ \']', '', decode(s))


def sane(s):
    return sanitize(s)
