from unidecode import unidecode
from re import sub

def decode(str):
    return unidecode(unicode(str,'utf_8'))

def sanitize(str):
    return sub('[ \'-]','',str)

def sane(str):
    return sanitize(decode(str))
