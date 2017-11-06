import sqlite3
import sys
import click
import os

@click.command()
@click.option('--dev_title', prompt="Hello!  ENTER DEV DATA PLZ")
@click.option('--alumni_title', prompt="ENTER ALUMNI TITLE PLZ")
def hello(dev_title, alumni_title):
    # os.system("in2csv ")
    print('DEV TITLE: ' + dev_title)
    print('ALUMNI TITLE: ' + alumni_title)


    # change .xlsx to .csv
    new_dev = dev_title.split(".")[0] + ".csv"
    new_alumni = alumni_title.split(".")[0] + ".csv"
    os.system("in2csv " + dev_title + " > " + new_dev)
    os.system("in2csv " + alumni_title + " > " + new_alumni)

    print('NEW ALUMNI: ' + new_alumni)
    print('NEW DEV: ' + new_dev)
    # create and populate db
    os.system("sqlite3 db.sqlite3")   
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute("drop table if existslumni")
    os.system("csvsql --db sqlite:///db.sqlite3 --table alumni --insert " + new_alumni)
    c.execute("drop table if exists dev")
    os.system("csvsql --db sqlite:///db.sqlite3 --table dev --insert " + new_dev)
    # test_alumni = c.execute("select * from " + new_alumni).fetchall()
    # test_dev = c.execute("select * from " + new_dev).fetchall()

    # print('TEST_ALUMNI IS: ' + str(test_alumni))
    # print('TEST_DEV IS: ' + str(test_dev))

if __name__ == '__main__':
    hello()


# echo -e ".separator ","\n.import /Users/RachelWilf/Desktop/blah/blah.csv qt_exported2" | sqlite3 testdatabase.db