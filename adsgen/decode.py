from unidecode import unidecode
from re import sub


def decode(s):
    # Does its best to substitute ASCII characters for
    # Unicode characters
    return unidecode(s)


def sanitize(s):
    # Removes spaces, apostrophes, and Unicode
    return sub('[ \']', '', decode(s))


def sane(s):
    # I'm sure there used to be a reason for this being a
    # separate method, but realistically it only remains
    # as such now because I can't be arsed to change a few
    # lines of code elsewhere in the project.
    return sanitize(s)
