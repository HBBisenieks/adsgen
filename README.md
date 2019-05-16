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
                        students or one of the configured affiliations
                        corresponding with organizational units for employees)

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

# Installation
Clone the repo to your local system and install with `pip3 install adsgen` (may
require sudo).

## Initial Setup
Before first usage, `/etc/adsgen.cfg` must be modified for your environment.
As coded, this script makes certain assumptions about your Google domain,
specifically related to how your OUs are organized. For employee accounts, the
assumption is that there is a top-level OU for employee accounts with multiple
child OUs underneath and that the names of these child OUs are sufficiently
unique that only the first two characters of the OU name need to be captured
to make a match at runtime.

# Usage
`adsgen` requires one argument, the path to a CSV file with columns for
Import ID[^1], last name, first name, ID number, class year/employee
affiliation, and Address Import ID.[^2] When called, the script will run
through each line of the CSV excluding the first[^3] and calculate a username
for that new user, skipping duplicate users and calculating username collisions
as needed. The class year/employee affiliation field differentiates between
student and employee user accounts, so account types can be mixed in a single
file if desired.

After running, a new CSV file will be written to your working directory with a
name in the default format `YYYY-MM-DD-new-users.csv`[^4][^5]

[^1]: The Import ID field is a unique identifier configured with a custom
Active Directory attribute and used to check for duplicate accounts.
Modifications should be made to the code before installation if a different
field is used as your unique identifier.

[^2]: The Address Import ID is an identifier used in some environment to link
records from disparate databases. If this attribute is not used in your
environment, junk data can be substituted, or the field can be removed from
the codebase for your use case.

[^3]: The `--noheader` flag can be used to avoid this behavior.

[^4]: Using the `--outfile` flag, you can specify a different file name.

[^5]: *Note:* if the script is run multiple times with different input on a
single date, the output of subsequent runs will overwrite the first unless a
different filename is specified for the output file.
