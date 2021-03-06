import psycopg2
import sys
import os
import csv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


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


def create_db(dbname, conn, cur):
    print("Creating database \""+dbname+"\"")
    text = "create database " + dbname
    cur.execute(text)
    cur.close()
    conn.close()
    conn = psycopg2.connect(host="localhost",database=dbname, user="postgres", password="postgres")
    cur = conn.cursor()
    return cur, conn


# Requires: array of input_files = [<filename>.csv], dbname (optional)
#       excel= if files being inputted are in xlsx format or not (all must be in same format)
# Effects: returns db cursor with dbname, having incorporated input files to db with <filename> as table name
def gen_db(input_files=[], dbname="db", excel=False):    
    conn = psycopg2.connect(host="localhost", user="postgres", password="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    text = "select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('" + dbname + "'));"
    db_exists = query(text, cur)[0][0]

    # if not db, ask and create or exit
    if not db_exists:
        dbs = [x[0] for x in query("select datname from pg_catalog.pg_database", cur)]
        input_text = "*** NOTE ***\nYou're trying to connect to a database called \""+ dbname + "\", which does not exist.\n"
        input_text +=  "The following databases exist on your system: "
        for x in dbs:
            input_text += x + ', '
        input_text.rstrip(', ')
        input_text += "\nDo you want to create a new database named \"" + dbname + "\"? [y] or [n]\n"
        user_input = input(input_text)

        if user_input=='n':
            print('Exiting the program.  Please specify an existing database name in the python code, or choose to create one next time around.\n')
            exit()
        else: # create db
            # testing
            # print("SHOULD BE FALSE: " + query("select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('" + dbname + "'));", cur, print_out=False)[0][0])
            cur, conn = create_db(dbname, conn, cur)

    # else (db exists), ask if they want to overwrite it with csvs or exit
    else:
        s = input("\"" + dbname + "\" already exists.  Do you want to overwrite it with the files you entered? [y] or [n]\n")
        if s == 'n':
            print("\nExiting the program.  Next time around, either choose to overwrite the database or choose an unused database name.")
            print("Database names in use: ")
            for x in query("select datname from pg_catalog.pg_database", cur):
                print(x[0], end="\t")
            print()
            exit()
        else:
            # drop and regenerate database
            print("Dropping database \"" + dbname + "\"")
            cur.execute("drop database if exists " + dbname)
            cur, conn = create_db(dbname, conn, cur)
    
    # populate db with csvs using pandas
    print("Populating database from csv files...")
    if excel:
        input_files = create_csvs(input_files)  

    for x in input_files:
        if '.xlsx' in x:
            exit('ERROR: The files you enetered contain .xlsx. Maybe you meant to use the excel=True option of gen_db().  Please rewrite the function and rerun the code.')

    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/' + dbname)
    for input_file in input_files:
        df = pd.read_csv(input_file)
        df.to_sql(input_file.split('.')[0], engine)

    print("Done")
    return cur, conn


def write_to_csv(rows, filename):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    print("Result is in", filename)

# Requires: dbname must be a database in postgres on this machine, postgres must be running (brew services start postgres),
# must have user and superuser privileges for postgres, postgres == (username, password)
# Effects: returns cursor and connection objects connected to postgreSQL database <dbname>
def connect(dbname):
    conn = psycopg2.connect(host="localhost", database=dbname, user="postgres", password="postgres")
    cur = conn.cursor()
    return cur, conn

# Requires: query text (in postgreSQL format)
#    database cursor (one of the return values of gen_db)
#    res: Does this query return anything?  e.g. "select * from alumni" returns something, but 
#       "update alumni set name='hey'" doesn't. Defaults to True.
#    cmnd_line: if the query returns a result, do you want it to print to the command line? Defaults to False.
#    csv: if the query returns a result, do you want it to print the result to a csv? Defaults to False.
#    file_out: if (csv): specify the filename you would like to write to - defaults to "out.csv".
#
# Modifies: db (wherever cursor is connected)
#
# Effects: queries database
#    if (res): returns results as python object for programmer
#    if cmnd_line, prints results on command line
#    if csv, prints results to file_out in csv format
def query(text, cursor, res=True, cmnd_line=False, csv=False, file_out="out.csv"):
    cursor.execute(text)
    result = not(not cursor.description)
    if res and not result:
        text_print = """ERROR: Problem in query function: you asked the function to print the results (res=True by default) but you didn't give it a SQL query that it could print something from.  Example: 'update one set a=4;'. This doesn't return anything to print.  If you want to do this with an 'update' statement, check out the SQL 'returning' statement online, or specify res=False\n\nExiting program now."""
        exit(text_print)

    if res:
        res = cursor.fetchall()
        colnames = [col.name for col in cursor.description]
        if cmnd_line:
            print('\n******* QUERY RESULT *******')
            for elt in colnames:
                print(elt, end="\t")
            print() #\n

            for elt in res:
                for sub_elt in elt:
                    print(sub_elt, end="\t")
                print()
        if csv:
            write_to_csv([colnames] + res, file_out)
        return res

# R: valid cursor and connection objects connected to postgreSQL databases
# M: commits changes executed by cur on db
# E: closes connection, commits changes.  MUST call this function at end of code
def end(cur, conn):
    conn.commit()
    cur.close()
    conn.close()