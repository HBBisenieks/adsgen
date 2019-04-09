from datetime import date

# A set of utilities for working with student data
# during account creation


def grade(classYear):
    # turns a 4-digit year classYear and returns
    # a numeric grade for the current school year
    # based on a July 1 rollover date
    year = date.today().year
    if date.today().month > 6:
        year += 1
    return (12 - (int(classYear) - year))


def division(grade):
    # returns a string, Division, based on numeric grade
    if grade > 8:
        return "Upper"
    elif grade > 5:
        return "Middle"
    else:
        return "Lower"


def readableGrade(grade):
    # returns a string, readableGrade, based on
    # a numeric grade, Kingergarten, 1st, 2nd, 3rd, ...
    post = 'th'
    if grade > 3:
        return str(grade) + post
    elif grade == 3:
        return "3rd"
    elif grade == 2:
        return "2nd"
    elif grade == 1:
        return "1st"
    else:
        return "Kingergarten"


def insertDelimiter(s, d='/'):
    # appends a delimiting string, d, onto a string, s, if
    # d is not already present at the end of s
    # strips leading commas
    if len(s) == 0:
        if d[0] == ',':
            return d[1:]
    if s[-len(d):] == d:
        return s
    return s + d


def path(classYear, schema, delimiter):
    # generalized method for returning an LDAP/Google path
    # given a class year, schema, and delimiter
    structure = schema['student_sub_structure'].split(',')
    g = grade(classYear)
    if 'division' in structure:
        div = division(g)
    if 'grade' in structure:
        rGrade = readableGrade(g)
    if 'class' in structure:
        classOf = schema['class_prefix'] + str(classYear)

    p = ''

    for element in structure:
        p = insertDelimiter(p, delimiter)
        if element == 'division':
            p = p + div
        if element == 'grade':
            p = p + rGrade
        if element == 'class':
            p = p + classOf
    return p


def gOrg(classYear, gSchema):
    if classYear.isdigit():
        return path(classYear, gSchema, '/')
    else:
        for div in gSchema['employee_sub'].split(','):
            if classYear[:2].upper() == div[:2].upper():
                return '/' + gSchema['employee_base'] + '/' + div


def adPath(classYear, aSchema):
    base = "," + aSchema['domain']
    if classYear.isdigit():
        return path(classYear, aSchema, ',ou=') + base
    else:
        return aSchema['employee_base'] + base
