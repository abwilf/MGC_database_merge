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
    print("\n\nCreating csv's from excel sheets...")
    os.system("in2csv " + dev_title + " > " + new_dev)
    os.system("in2csv " + alumni_title + " > " + new_alumni)
    os.system("in2csv " + campaign_title + " > " + new_campaign)
    print("Done\n")
    return {"new_dev": new_dev, "new_alumni": new_alumni, "new_campaign": new_campaign}

def create_db(new_dev, new_alumni, new_campaign, to_find_title):
    print("Creating and populating database from csv files...")
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
    c.execute("drop table if exists alums_to_find")
    os.system("csvsql --db sqlite:///db.sqlite3 --table alums_to_find --insert " + to_find)
    print("Done\n")
    return c

@click.command()
@click.option('--dev_title', prompt="Hello!  ENTER DEV DATA PLZ")
@click.option('--alumni_title', prompt="ENTER ALUMNI TITLE PLZ")
@click.option('--campaign_title', prompt="ENTER CAMPAIGN MONITOR TITLE PLZ")
@click.option('--to_find_title', prompt="TO FIND TITLE PLZ")
@click.option('--updates', prompt="Any updates to excel sheets? (yes/no)")  # create csv's,
@click.option('--mode', prompt="Mode?") # find_alumni, query_db
def hello(dev_title, alumni_title, campaign_title, to_find_title, updates, mode):
    # change .xlsx to .csv
    new_dev = dev_title.split(".")[0] + ".csv"
    new_alumni = alumni_title.split(".")[0] + ".csv"
    new_campaign = campaign_title.split(".")[0]+".csv"

    if updates == "yes":
        create_csvs(dev_title, alumni_title, campaign_title, new_dev, new_alumni, new_campaign)
        c = create_db(new_dev, new_alumni, new_campaign, to_find_title)
    else:
        conn = sqlite3.connect("db.sqlite3")
        conn.text_factory = bytes
        conn.row_factory = dict_factory
        c = conn.cursor()

    # print(c.execute("select email from temp").fetchall());
    # write_to_csv(["email"], "alums_to_find.csv", c.execute("select email from alums_to_find").fetchall())

    # blah = "select dev.full_name, dev.age, dev.address, dev.primary_email from dev inner join alums_to_find on dev.primary_email = alums_to_find.email"
    # blah = "select dev.full_name, dev.age, dev.address, dev.primary_email from dev inner join alums_to_find on dev.primary_email = alums_to_find.email"
    # blah = c.execute(blah).fetchall()
    blah = c.execute("select email from alums_to_find").fetchall()
    # print(blah)
    # write_to_csv(["full_name", "Age", "address", "Primary_Email"], "emails_found_dev_db.csv", blah)
    # write_to_csv(["email"], "alums_to_find.csv", blah)
    # if mode == "find_alumni":

        # leftover = find_missing_alumni(c)
        # write_to_csv(["email"], "leftover_alums.csv", leftover)

    # test_alumni = c.execute("select * from " + new_alumni).fetchall()
    # test_dev = c.execute("select * from " + new_dev).fetchall()

    # print('TEST_ALUMNI IS: ' + str(test_alumni))
    # print('TEST_DEV IS: ' + str(test_dev))

if __name__ == '__main__':
    hello()


# echo -e ".separator ","\n.import /Users/RachelWilf/Desktop/blah/blah.csv qt_exported2" | sqlite3 testdatabase.db