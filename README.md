# adsgen

```
usage: adsgen [-h] [-o OUTFILE] [--noheader] [--silent] [--nowrite] infile

Takes a CSV export from Blackbaud in the form
ImportID,Last,First,StudentID,ClassYear,Address-ImportID, santizes data to the
best of its ability and creates a CSV of user data for import to Google Apps,
via GAM, and Active Directory, via Powershell, calculating username collisions
on the fly.

positional arguments:
  infile                CSV input file - fields must be in order:
                        ImportID,Last,First,StudentID,ClassYear,Address-
                        ImportID (ClassYear is either a 4-digit integer for
                        students or FAC|STAFF|ADMIN for employees)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        Path to output file. If -o is not specified, output
                        file will be named [DATE]-new-users.csv where [DATE]
                        is the current ISO 8601 date (see xkcd 1179).
  --noheader            Use only if the input file contains no header row.
                        Default behavior is to skip the first row of the input
                        file.
  --silent              Run silently. Default behavior is to print contents of
                        outfile to STDOUT as well as writing it to file. Note:
                        even with --silent specified, duplicate warnings will
                        still print.
  --nowrite             Do not write output to a file.

This script is only as smart as the user running it. Remember to always
sanity-check output CSV before importing data.
```
