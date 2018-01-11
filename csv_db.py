import sqlite3
import sys
import os
import csv


# R: [<filename>.xlsx]
# E: [<filename>.csv]
def create_csvs(input_files):
    print("Converting excel sheets to csv...")
    to_ret = []

    for input_file in input_files:
        out = input_file.split('.')[0] + ".csv"
        os.system("in2csv " + input_file + " > " + out)
        to_ret.append(out)

    return to_ret

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# R: array of input_files = [<filename>.csv], dbname (optional)
# E: returns db cursor with dbname, having incorporated input files to db with <filename> as table name
def gen_db(input_files, dbname="db", excel=False):
    # convert to csv if necessary
    if excel:
        input_files = create_csvs(input_files)

    print("Creating and populating database from csv files...")
    
    # create and populate db
    conn = sqlite3.connect(dbname + ".sqlite3")
    conn.text_factory = bytes
    conn.row_factory = dict_factory
    c = conn.cursor()
    
    for input_file in input_files:
        file = input_file.split('.')[0]
        c.execute("drop table if exists " + file)
        os.system("csvsql --db sqlite:///" + dbname + ".sqlite3 --table " + file + " --insert " + input_file)

    print("Done")
    return c


def write_to_csv(fieldnames, filename, result):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in result:
            writer.writerow(row)


# R: query text (in SQL format)
#    database cursor: i.e. return value of gen_db
#    cmnd_line: do you want it to print to the command line?  by default it prints results to a csv
#    file_out - specify the filename you would like to write to - defaults to "out.csv"
#
# M: db.sqlite3 (or whatever db cursor is connected to)
#
# E: always returns results as python object for programmer
#    if cmnd_line, returns results on command line
#    else, prints results to file_out in csv format
def query(text, cursor, cmnd_line=False, file_out="out.csv"):
    res = cursor.execute(text).fetchall()

    tempres = []

    if res:
        fieldnames = list(res[0].keys())
        # deal with byte encoding problem
        for elt in res:
            tempres.append({k: v.decode('UTF-8') for k, v in elt.items()})
    res = tempres

    if cmnd_line:
        print('\n******* QUERY RESULT *******')
        for elt in fieldnames:
            print(elt, end="\t")
        print() #\n

        for elt in res:
            for key, val in elt.items():
                print(val, end="\t")
            print()
    else:
        write_to_csv(fieldnames, file_out, res)

    return res