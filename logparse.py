#!/usr/bin/python
'''
USAGE: ./logparse.py <logfile> <month> <date>

DESC: This script takes three mandatory command line arguments. [1] Name of
      the logfile. [2] Three letter month (ie. jan, feb, etc). [3]. Dates from
      1-31.  It then parses the log file and generate a csv file which
      contains the percentage value for each corresponsing file system.

BACKGROUND:

LAST REVISION: 18th June 2012
AUTHOR: Gene Ordanza <geronimo.ordanza@fisglobal.com>
'''

import sys, re

def headers(csv):
    # Print the column headings to the file and return 'None' value.

    headings = '%-5s %-8s %-5s %-4s %-5s %-4s %-4s %-4s %-6s %-5s %-8s' % \
              ('DATE', '|/vitria', '|/ora2', '|/ora', '|/ctc', '|/rp', '|/op',
               '|/cf', '|/appl1', '|/appl', '|/mailbox\n')

    csv.write(headings)
    return


def parse(string, fs, year=False):
    # This function takes a string parameter, split it into a list object and
    # test it against year and elements in fs.
    # Return a dictionary in format {filesystem:percentage}.

    line = string.split()

    if line[-1] == year:
        return {'date': '%s%s' % (line[1], line[2])}

    # This. List comprehension if you absolutely have to pick one Python idiom.
    val = [{key: str(line[-2])} for key in fs if key == line[-1]]

    if val:
        return val[0]


def main(logs, csv):
    # The main function is mostly for variable initialization, iterating over
    # the file object and calling the actual parser, and writes the results to a
    # csv file.  It takes two file object as paramter and return None value

    year    = '2012'
    rowdict, switch = {}, False
    month, date = sys.argv[2].capitalize(), sys.argv[3]

    fields = ('date', '/vitria', '/ora2', '/ora', '/ctc', '/ctc/ctcprod/data/rp',
              '/ctc/ctcprod/data/op', '/ctc/ctcprod/data/cf', '/appl1',
              '/appl', '/appl/ce/ceunix/database/mailbox')

    format = '%%(%s)-5s |%%(%s)-6s |%%(%s)-6s |%%(%s)-4s |%%(%s)-4s'  + \
             '|%%(%s)-4s |%%(%s)-3s |%%(%s)-3s |%%(%s)-6s |%%(%s)-5s' + \
             '|%%(%s)-8s\n'

    entries = format % fields

    pattern = r'.*\b%s\b.*\b%s\b.* %s$' % (month, date, year)
    match   = re.compile(pattern)

    headers(csv)

    for line in logs:

        if match.search(line):
            switch = True
            data = parse(line, fields, year)
            if data: rowdict.update(data)
            continue

        if switch:
            data = parse(line, fields, year)
            if data: rowdict.update(data)

        if len(rowdict) == 11:
            csv.write(entries % rowdict)
            rowdict = {}


if  __name__ == '__main__':

    if len(sys.argv) != 4:
        print __doc__
        sys.exit(1)

    logfile = open(sys.argv[1], 'rU')
    csvfile = open('csv.txt', 'w')

    try:
        main(logfile, csvfile)
    finally:
        logfile.close()
        csvfile.close()
