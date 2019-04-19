from datetime import date
import subprocess

# A set of utilities for working with student data
# during account creation


def grade(classYear, rollover=True):
    # turns a 4-digit year classYear and returns
    # a numeric grade for the current school year
    # based on a July 1 rollover date
    year = date.today().year
    if date.today().month > 6 and rollover:
        year += 1
    return (12 - (int(classYear) - year))


def division(grade):
    # returns a string, Division, based on numeric grade
    # TODO: implement configurable division names/boundaries
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
        return "Kindergarten"


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


def path(classYear, schema, delimiter, rollover=True):
    # generalized method for returning an LDAP/Google path
    # given a class year, schema, and delimiter
    structure = schema['student_sub_structure'].split(',')
    g = grade(classYear, rollover)
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
        return '/' + gSchema['student_base'] + path(classYear, gSchema, '/')
    else:
        for div in gSchema['employee_sub'].split(','):
            if classYear[:2].upper() == div[:2].upper():
                return '/' + gSchema['employee_base'] + '/' + div


def adPath(classYear, aSchema):
    base = "," + aSchema['domain']
    if classYear.isdigit():
        p = path(classYear, aSchema, ',ou=') + ',' + aSchema['student_base']
        return p + base
    else:
        return aSchema['employee_base'] + base


def yesNo(question):
    while True:
        r = str(input(question + " (y/n): ")).lower().strip()
        if r[0] == 'y':
            return True
        if r[0] == 'n':
            return False


def promoteOU(grade, gSchema, dryRun):
    command = ['gam', 'update', 'org']

    year = date.today().year + (12 - grade)
    if grade < 13:
        command.append(path(year, gSchema, '/', False))
    else:
        command.append('/' + gSchema['student_base'] + '/' +
                       gSchema['student_graduate'] + '/' +
                       gSchema['class_prefix'] + str(year))
    command.append('parent')
    if grade < 12:
        newParent = path(year + 1, gSchema, '/', False)
        r = len(gSchema['class_prefix']) + len(str(year)) + 1
        command.append(newParent[:-r])
    elif grade == 12:
        command.append('/' + gSchema['student_base'] + '/' +
                       gSchema['student_graduate'])
    else:
        command.append('/' + gSchema['suspended'])

    command.append('inherit')
    if dryRun:
        command.insert(0, 'echo')
    return command


def rotateGroup(grade, gSchema, addRemove, dryRun):
    command = ['gam', 'update', 'group']
    if grade < 13:
        command.append('grade' + str(grade))
    else:
        command.append(gSchema['graduate_group'])
    command.extend([addRemove, 'ou_and_children'])
    classYear = date.today().year + (12 - grade)
    r = len(gSchema['class_prefix']) + len(str(classYear)) + 1
    if addRemove == 'add':
        org = path(classYear, gSchema, '/', False)
        command.append(org[:-r])
    elif addRemove == 'remove':
        if grade < 11:
            org = path(classYear + 1, gSchema, '/', False)
            command.append(org[:-r])
        elif grade == 12:
            command.append('/' + gSchema['student_base'] + '/' +
                           gSchema['student_graduate'])
        else:
            command.append('/' + gSchema['suspended'] + '/' +
                           gSchema['class_prefix'] + str(classYear))
    if dryRun:
        command.insert(0, 'echo')
    return command


def promoteAccounts(gSchema, dryRun):
    promoteCommands = []
    groupAddCommands = []
    groupRemoveCommands = []
    for grade in range(0, 14):
        print(grade)
        promoteCommands.append(promoteOU(grade, gSchema, dryRun))
        if grade > 3:
            groupAddCommands.append(rotateGroup(grade, gSchema, 'add', dryRun))
            groupRemoveCommands.append(rotateGroup(grade, gSchema, 'remove',
                                       dryRun))
    print("The following commands will be run to promote OUs:")
    for command in promoteCommands:
        print(' '.join(command))

    if yesNo("Execute these commands to promote student OUs?"):
        for command in promoteCommands:
            subprocess.run(command)
        print('OU promotion complete.')
    else:
        print("Aborting. OU promotion not run.")
    print('The following commands will be run to rotate email groups:')
    for command in groupRemoveCommands:
        print(' '.join(command))
    for command in groupAddCommands:
        print(' '.join(command))
    if yesNo("Execute these commands to rotate email groups?"):
        for command in groupRemoveCommands:
            subprocess.run(command)
        for command in groupAddCommands:
            subprocess.run(command)
        print('Group rotation complete.')
    else:
        print("Aborting. Group rotation not run.")
