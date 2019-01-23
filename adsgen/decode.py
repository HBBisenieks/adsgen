from unidecode import unidecode
from re import sub


def decode(str):
    return unidecode(str(str))


def sanitize(str):
    return sub('[ \']', '', str)


def sane(str):
    return sanitize(decode(str))
