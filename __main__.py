import sqlite3
import sys
import click
import os
import csv
import unicodedata

def write_to_csv(fieldnames, filename, result):
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in result:
            writer.writerow(row)

# c == cursor
def find_missing_alumni(c):
    result = c.execute("select FIRST_NAME, LAST_NAME, EMAIL, EMAIL_2, GRAD_YEAR_1 from alumni where EMAIL in (select email from campaign) OR EMAIL_2 in (select email from campaign)").fetchall()
    fieldnames = ["FIRST_NAME", "LAST_NAME", "EMAIL", "EMAIL_2", "GRAD_YEAR", "GRAD_YEAR_1"]
    filename = 'campaign_names_found.csv'
    write_to_csv(fieldnames, filename, result)
    temp = c.execute("select EMAIL from alumni")
    result = c.execute("select * from campaign WHERE NOT (email in ?)", temp)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_csvs(dev_title, alumni_title, campaign_title, new_dev, new_alumni, new_campaign):
    os.system("in2csv " + dev_title + " > " + new_dev)
    os.system("in2csv " + alumni_title + " > " + new_alumni)
    os.system("in2csv " + campaign_title + " > " + new_campaign)
    return {"new_dev": new_dev, "new_alumni": new_alumni, "new_campaign": new_campaign}

def create_db(new_dev, new_alumni, new_campaign):
    # create and populate db
    os.system("sqlite3 db.sqlite3")   
    conn = sqlite3.connect("db.sqlite3")
    conn.text_factory = bytes
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("drop table if exists alumni")
    os.system("csvsql --db sqlite:///db.sqlite3 --table alumni --insert " + new_alumni)
    c.execute("drop table if exists dev")
    os.system("csvsql --db sqlite:///db.sqlite3 --table dev --insert " + new_dev)
    c.execute("drop table if exists campaign")
    os.system("csvsql --db sqlite:///db.sqlite3 --table campaign --insert " + new_campaign)
    return c

@click.command()
@click.option('--dev_title', prompt="Hello!  ENTER DEV DATA PLZ")
@click.option('--alumni_title', prompt="ENTER ALUMNI TITLE PLZ")
@click.option('--campaign_title', prompt="ENTER CAMPAIGN MONITOR TITLE PLZ")
@click.option('--create_csvs', prompt="Create csv's?")
@click.option('--find_alumni', prompt="Find alumni?")
def hello(dev_title, alumni_title, campaign_title, create_csvs, find_alumni):
    # change .xlsx to .csv
    new_dev = dev_title.split(".")[0] + ".csv"
    new_alumni = alumni_title.split(".")[0] + ".csv"
    new_campaign = campaign_title.split(".")[0]+".csv"

    if create_csvs == "yes":
        create_csvs(dev_title, alumni_title, campaign_title, new_dev, new_alumni, new_campaign)
        c = create_db(new_dev, new_alumni, new_campaign)
    else:
        conn = sqlite3.connect("db.sqlite3")
        conn.text_factory = bytes
        conn.row_factory = dict_factory
        c = conn.cursor()

    if find_alumni == "yes":
        leftover = find_missing_alumni(c)
        write_to_csv(["email"], "leftover_alums.csv", leftover)

    # test_alumni = c.execute("select * from " + new_alumni).fetchall()
    # test_dev = c.execute("select * from " + new_dev).fetchall()

    # print('TEST_ALUMNI IS: ' + str(test_alumni))
    # print('TEST_DEV IS: ' + str(test_dev))

if __name__ == '__main__':
    hello()


# echo -e ".separator ","\n.import /Users/RachelWilf/Desktop/blah/blah.csv qt_exported2" | sqlite3 testdatabase.db