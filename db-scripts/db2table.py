#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Extract data from sqlite database, and convert into
dict, dataframe, ...

Tong Zhang <zhangt@frib.msu.edu>
2017-10-12 14:10:56 PM EDT
"""

from argparse import ArgumentParser
import os

import sqlite3
import sys


parser = ArgumentParser(prog=os.path.basename(sys.argv[0]),
            description="Convert SQLite database into table.")
parser.add_argument("--format", dest="fmt", default='json',
        help="Output file format, 'csv' or 'json'")
parser.add_argument("db", help="File name of SQLite database.")
parser.add_argument("outfile", help="File name of output table.")
parser.add_argument("--tab", action="append", 
        help="Table name from database")

if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args(sys.argv[1:])

db, fmt, outfile = args.db, args.fmt, args.outfile
tab = ['function'] if args.tab is None else args.tab

conn = sqlite3.connect(db)
c = conn.cursor()
for t in tab:
    c.execute("SELECT * FROM {}".format(t))
    header = [desc[0] for desc in c.description]

    if fmt == 'json':
        d = []
        for line in c:
            d.append(dict(zip(header, line)))

        import json
        json.dump(d, open(outfile, 'wb'), indent=2, sort_keys=True)

    if fmt == 'csv':
        import csv
        with open(outfile, 'wb') as f:
            w = csv.writer(f)
            w.writerow(header)
            w.writerows(c.fetchall())

