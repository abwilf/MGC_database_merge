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


def create_db(dbname, conn):
    print("Creating database \""+dbname+"\"")
    text = "create database " + dbname
    cur = conn.cursor()
    cur.execute(text)
    conn = psycopg2.connect(host="localhost",database=dbname, user="postgres", password="postgres")
    cur = conn.cursor()
    return cur


# R: array of input_files = [<filename>.csv], dbname (optional), if files being inputted are in xlsx format or not
# E: returns db cursor with dbname, having incorporated input files to db with <filename> as table name
def gen_db(input_files=[], dbname="db", excel=False):    
    conn = psycopg2.connect(host="localhost", user="postgres", password="postgres")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    text = "select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('" + dbname + "'));"
    db_exists = query(text, cur, print_out=False)[0][0]

    # if not db, ask and create or exit
    if not db_exists:
        dbs = [x[0] for x in query("select datname from pg_catalog.pg_database", cur, print_out=False)]
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
            cur = create_db(dbname, conn)

    # else (db exists), ask if they want to overwrite it with csvs or exit
    else:
        s = input("\"" + dbname + "\" already exists.  Do you want to overwrite it with the csv's you entered? [y] or [n]\n")
        if s == 'n':
            print("\nExiting the program.  Next time around, either choose to overwrite the database or choose an unused database name.")
            print("Database names in use: ")
            for x in query("select datname from pg_catalog.pg_database", cur, print_out=False):
                print(x[0], end="\t")
            print()
            exit()
        else:
            # drop and regenerate database
            print("Dropping database \"" + dbname + "\"")
            cur.execute("drop database if exists " + dbname)
            cur = create_db(dbname, conn)
    
    # populate db with csvs using pandas
    print("Populating database from csv files...")
    if excel:
        input_files = create_csvs(input_files)  

    engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/' + dbname)
    for input_file in input_files:
        df = pd.read_csv(input_file)
        df.to_sql(input_file.split('.')[0], engine)

    print("Done")
    return cur


def write_to_csv(rows, filename):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)


# Requires: query text (in SQL format)
#    database cursor (the return value of gen_db)
#    print: do you want it to print anything (to csv or command line?) Default=True
#    cmnd_line: do you want it to print to the command line? True or False. By default the function prints results to a csv
#    file_out: If not printing to command line, specify the filename you would like to write to - defaults to "out.csv"
#
# Modifies: db (wherever cursor is connected)
#
# Effects: always returns results as python object for programmer
#    if cmnd_line, returns results on command line
#    else, prints results to file_out in csv format
def query(text, cursor, print_out=True, cmnd_line=False, file_out="out.csv"):
    cursor.execute(text)
    colnames = [col.name for col in cursor.description]
    res = cursor.fetchall()

    # tempres = []
    # if res:
    #     # fieldnames = list(res[0].keys())
    #     # deal with byte encoding problem
    #     for elt in res:
    #         tempres.append({k: (v.decode('UTF-8') if type(v) == bytes else v) for k, v in elt.items()})
    # res = tempres

    if print:
        if cmnd_line:
            print('\n******* QUERY RESULT *******')
            for elt in colnames:
                print(elt, end="\t")
            print() #\n

            for elt in res:
                for sub_elt in elt:
                    print(sub_elt, end="\t")
                print()
        else:
            write_to_csv([colnames] + res, file_out)

    return res