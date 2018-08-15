# A set of utilities for working with student data
# during account creation

from datetime import date

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

def studentOrg(classYear):
    # takes a 4-digit year and returns a string
    # for G Suite organizational units
    g = grade(classYear)
    d = division(g)
    r = readableGrade(g)
    org = "/Student/" + d + "/" + r + "/ClassOf" + str(classYear)
    return org

def studentPath(classYear):
    # takes a 4-digit year and returns a valid
    # ldap path
    g = grade(classYear)
    d = division(g)
    r = readableGrade(g)
    path = "ou=ClassOf" + str(classYear) + ",ou=" + r + ",ou=" + d + ",ou=Students"
    return path

def gOrg(classYear):
    if classYear.isdigit():
        return studentOrg(classYear)
    else:
        if classYear[0].upper() == 'F':
            return "/Staff/Faculty"
        elif classYear[0].upper() == 'A':
            if classYear[1].upper() == 'S':
                return "/Staff/ASP"
            else:
                return "/Staff/School-Admin"
        else:
            return "/Staff"

def adPath(classYear):
    base = ",dc=headroyce,dc=org"
    if classYear.isdigit():
        return studentPath(classYear) + base
    else:
        return "ou=DomainUsers" + base
