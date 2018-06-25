import ldap
import sys
import csv
import argparse
import ConfigParser
import io
from datetime import date
from adsgen.decode import sane
from adsgen.hrs_student_utils import gOrg,adPath
from adsgen.hrs_pw import hrspw

def bind(server,username,password):
    ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT,0)
    connection = ldap.initialize(server)
    connection.simple_bind_s(username,password)
    return connection

def lsearch(connection,org,query):
    return connection.search_s(org,ldap.SCOPE_SUBTREE,query)

def checkDuplicate(connection,org,tempList,importID):
    for row in tempList:
        if len(row) > 0:
            if row[0] == importID:
                return True
    query = "(importid=" + importID + ")"
    if lsearch(connection,org,query):
        return True
    return False

def adOrg(classYear):
    # return Active Directory Org
    base = ",dc=headroyce,dc=org"
    if classYear.isdigit():
        return "ou=students" + base
    return "ou=domainusers" + base

def localDup(tempList,username):
    for row in tempList:
        if len(row) > 0:
            return row[5] == username

def checkCollision(connection,tempList,first,last,classYear,org):
    lFirst = first.lower()
    lLast = last.lower()
    collision = False

    if classYear.isdigit():
        i = 1
        username = lFirst + lLast[:i] + str(classYear)
        query = "(samaccountname=" + username + ")"
        while i <= len(lLast) and (lsearch(connection,org,query) or localDup(tempList,username)):
            i += 1
            username = lFirst + lLast[:i] + str(classYear)
            query = "(samaccountname=" + username + ")"
            collision = True
    else:
        i = 1
        username = lFirst[:i] + lLast
        query = "(samaccountname=" + username + ")"
        while i <= len(lLast) and (lsearch(connection,org,query) or localDup(tempList,username)):
            i += 1
            username = lFirst[:i] + lLast
            query = "(samaccountname=" + username + ")"
            collision = True

            if collision:
                name = first + " " + last
                print "Username collision for " + name + ". Username is " + username

    return username

def generateLine(row,tempList,connection):
    # Row is: ImportID,Last,First,ID,ClassYear,AddrImportID
    # Returns a list in the form: ImportID,Surname,GivenName,Name,StudId,SamAccountName,Password,ADDR-ImportID,ContactType,Email,Path,Org
    line = []
    importID = row[0]
    last = sane(row[1])
    first = sane(row[2])
    id = row[3]
    classYear = row[4]
    org = adOrg(row[4])
    addr = row[5]
    name = first + " " + last
    if checkDuplicate(connection,org,tempList,importID):
        print "Duplicate found for " + name + " with Import ID " + importID
    else:
        username = checkCollision(connection,tempList,first,last,classYear,org)
        email = username + "@headroyce.org"
        org = gOrg(classYear)
        path = adPath(classYear)
        password = hrspw(2,1)
        line = [importID,last,first,name,id,username,password,addr,"E-Mail",email,path,org]

    return line

def generateHeader():
    header = ["ImportID","Surname","GivenName","Name","StudId","SamAccountName","Password","ADDR-ImportID","ContactType","Email","Path","Org"]
    return header

def handleArguments(args):
    description = "Takes a CSV export from Blackbaud in the form ImportID,Last,First,StudentID,ClassYear,Address-ImportID, santizes data to the best of its ability and creates a CSV of user data for import to Google Apps, via GAM, and Active Directory, via Powershell, calculating username collisions on the fly."
    epilog = "This script is only as smart as the user running it. Remember to always sanity-check output CSV before importing data."

    parser = argparse.ArgumentParser(description = description,epilog = epilog)
    parser.add_argument("infile",type = str,help = "CSV input file - fields must be in order: ImportID,Last,First,StudentID,ClassYear,Address-ImportID (ClassYear is either a 4-digit integer for students or FAC|STAFF|ADMIN for employees)")
    parser.add_argument('-o','--outfile',default = '',type = str,help = "Path to output file. If -o is not specified, output file will be named [DATE]-new-users.csv where [DATE] is the current ISO 8601 date (see xkcd 1179).")
    parser.add_argument('--noheader',action = "store_true",help = "Use only if the input file contains no header row. Default behavior is to skip the first row of the input file.")
    parser.add_argument('--silent',action = "store_true",help = "Run silently. Default behavior is to print contents of outfile to STDOUT as well as writing it to file. Note: even with --silent specified, duplicate warnings will still print.")
    parser.add_argument('--nowrite',action = "store_true",help = "Do not write output to a file.")

    return parser.parse_args()

def fileName(outfile):
    if outfile:
        return outfile
    return date.today().isoformat() + '-new-users.csv'

def parseConfig():
    with open("/etc/adsgen.cfg") as f:
        cf = f.read()

    config = ConfigParser.RawConfigParser(allow_no_value = True)
    config.readfp(io.BytesIO(cf))

    s = config.get('server','address')
    u = config.get('server','username')
    p = config.get('server','password')

    if not s and u and p:
        print "Invalid config. Please ensure that settings are correct in /etc/adsgen.cfg"
        sys.exit(1)
    else:
        return s,u,p

def main(args = None):
#    s = "ldaps://hrsads01.headroyce.org"
#    u = "script@headroyce.org"
#    p = "serverUsagecat0"
    s,u,p = parseConfig()

    if args is None:
        args = sys.argv[1:]
    options = handleArguments(args)

    connection = bind(s,u,p)
    tempList = []
    tempList.append(generateHeader())

    with open(options.infile,'r') as infile:
        reader = csv.reader(infile)
        if not options.noheader:
            next(reader,None)
        for row in reader:
            tempList.append(generateLine(row,tempList,connection))

    connection.unbind_s()
    if not options.silent:
        print tempList

    if not options.nowrite:
        outfile = fileName(options.outfile)
        with open(outfile,'wb') as f:
            writer = csv.writer(f)
            writer.writerows(tempList)

if __name__ == '__main__':
    main()
