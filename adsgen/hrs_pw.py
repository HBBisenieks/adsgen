import random

SYMBOLS = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')']


def insertSymbols(password):
    # Inserts a symbol in place of an existing character
    char_l = list(password)
    char_l[random.choice(list(range(len(char_l))))] = random.choice(SYMBOLS)
    return ''.join(char_l)


def hrspw(words=2, symbols=0, prefix='', postfix=''):
    # Returns a diceware-style password
    wordList = ['Anna',
                'ASP',
                'Becks',
                'BigToy',
                'Caravan',
                'citizenship',
                'Colla',
                'diversity',
                'excellence',
                'Expos',
                'FallOut',
                'Gatehouse',
                'gold',
                'green',
                'HeadsUp',
                'Jayhawk',
                'Josiah',
                'Lincoln',
                'Loop',
                'Lower',
                'Memoir',
                'MEW',
                'Middle',
                'Nods',
                'Pavilion',
                'Read',
                'Rotunda',
                'Royce',
                'SEP',
                'stairs',
                'treehouse',
                'Tuffy',
                'Turkeys',
                'Upper',
                'Voce',
                'WL']

    password = prefix

    for x in range(words):
        password += str(random.choice(wordList)).capitalize()

    while len(password) < 8:
        password += str(random.choice(wordList)).capitalize()

    password += postfix

    for y in range(symbols):
        password = insertSymbols(password)

    return password
