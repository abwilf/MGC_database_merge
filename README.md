# Men's Glee Club Database Merge Script
#### Table of Contents
[Description and Motivation](https://github.com/abwilf/MGC_database_merge#description-and-motivation)

[Installing the Prerequisites](https://github.com/abwilf/MGC_database_merge#installing-the-prerequisites)

[Running the Scripts](https://github.com/abwilf/MGC_database_merge#running-the-scripts)

[FAQ](https://github.com/abwilf/MGC_database_merge#FAQ)

## Description and Motivation
An easy to use computer utility that takes in excel documents from SMTD's development office and the MGC alumni database, merges them, and returns a new excel file.

This is important because having an up to date database is critical for student-alumni engagement efforts.  The Club cannot simply copy development's database every month, however, because it needs to keep its own data (i.e. who was in the Friars, tour information, executive board positions held...etc).  Additionally, no database system should be implemented in anything more complicated than excel because (1) the development office only sends us excel files and (2) not every Alumni Relations Manager is a Computer Science major and the risk exists that a future Club will abandon our database altogether if it is too confusing to operate (as occurred in 2014), leading to lost data about our alumni and a time intensive effort to restore the system.

Due to these constraints, we need a database that has the operational capability of a complex database system, but the ease of use and access of an excel file.  Bridging that gap is the purpose of this project.

It is worth noting that in pursuit of this goal, some intermediary functionalities were necessary to implement, for example code that converts between database languages and excel, and command line utilities processing queries into those databases.  These functionalities turned out to be important to other branches of Club as well, so some of their functionalities may be ported to different projects.  Details on this, the project's installation, and examples to get you started are below.

## Installing the prerequisites (Mac)
```        
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update
brew install git
brew install python3
cd ~/Desktop/
git clone https://github.com/abwilf/MGC_database_merge.git
python3 -m venv env
source env/bin/activate
brew services start postgres
pip3 install -r requirements.txt
psql -U postgres
create database mydb;
create user postgres with superuser password 'password';
\q
```

## Running the scripts
### Alumni Relations Manager
Ask development to send you a spreadsheet in excel format - `.xlsx` - with the following columns:

`dev_id, title, first, last, no_contact, no_solicitation, no_email, email, address, city, state, zip, home, cell`

Clean up the file they send you by naming it `dev.xlsx` and changing the column names to match the ones above.  It does not matter if there are extra columns, but the spreadsheet must have the columns above named properly to work.  The colors of the spreadsheet don't affect the program's performance.

Move the files `alumni.xlsx` and `dev.xlsx` into the `mgc_db_merge` folder.

NOTE: It is important that you name the files exactly as they are named above.  You can also name them `alumni.csv` and `dev.csv`, but you will need to type `#` at the beginning of line 3 of `alumni_script.py`, delete the `#` at the beginning of line 4, and save the file before you run the program.  If you don't have a coding text editor, I would just convert the files from `.csv` to `.xlsx`.

Copy and paste the following code into your terminal.

The new database is in the file `alumni_new.csv`

Change the name of `alumni_new.csv` to `alumni.csv` and reupload it to the Alumni Google Drive so the rest of the team has an updated copy.

```
source env/bin/activate
python3 alumni_script.py
```

### Business Team
To manage the inventory database, you'll need to access functions in `csv_db.py`.  The relevant functions you'll use are below.  For a full example, scroll down or [click here](https://github.com/abwilf/MGC_database_merge#full-example).

#### Generate Database
```python
# Requires: array of input_files = [<filename>.csv or <filename>.xlsx], dbname (optional), excel: if files being inputted are in xlsx format or not (True/False)
# Effects: returns db cursor (this is how we'll access the database later) with dbname, having incorporated input files to db with <filename>s as table names
def gen_db(input_files, dbname="db", excel=False):
```
##### Example 1
This code passes in two test files in excel format with the database name "hey" (generates database `hey.sqlite3`).  Saves return result to `cursor` variable for future use in queries (more on this below).  `hey.sqlite3` will have two tables, `test1` and `test2`.
```python
cursor = csv_db.gen_db(["test1.xlsx", "test2.xlsx"], dbname="hey", excel=True)
```

##### Example 2
This code takes in one csv file, generates database called `db.sqlite3` by default.  Note: there's no need to pass an `excel` variable here because it defaults to `False`
```python
cursor = csv_db.gen_db(["test1.csv"])
```

#### Query Database
```python
# Requires: query text (in SQL format)
#    database cursor (the return value of gen_db)
#    print: do you want it to print anything? (to csv or command line). Default=True
#    cmnd_line: do you want it to print to the command line? True or False. By default the function prints results to a csv
#    file_out: If not printing to command line, specify the filename you would like to write to - defaults to "out.csv"
#
# Modifies: db.sqlite3 (or whatever db cursor is connected to)
#
# Effects: always returns results as python object for programmer
#    if cmnd_line, returns results on command line
#    else, prints results to file_out in csv format
def query(text, cursor, print=True, cmnd_line=False, file_out="out.csv"):
```
##### Example 1
This code executes a query on the database passed in by `cursor`, the return value of `gen_db()`.  The first parameter is text in SQL format.  The second is the cursor variable.  The third specifies that the user would like to print the results of the query to the command line.  Since the user specified `cmnd_line=True`, there is no need to specify `file_out`, since the program will print to the command line instead of a csv file.

Note: I will not be writing a tutorial of SQL commands, as that has been done more effectively by real experts.  [Start here](https://www.w3schools.com/sql/sql_syntax.asp) if you'd like to learn.

```python
csv_db.query("select * from test1", cursor, cmnd_line=True)
```

##### Example 2
This code executes a query on the database passed in by `cursor`. Since no other parameters are passed in, it writes the results to a csv, `out.csv`, by default.
```python
csv_db.query("select * from test1", cursor)
```

##### Example 3
This code executes a query on the database passed in by `cursor`. This writes the results of the query to `blah.csv`.
```python
csv_db.query("select * from test1", cursor, file_out="blah.csv")
```

#### Full Example
1. We have a file: `example.py`.  The code here takes in 2 excel files (since the inputs are excel files, mark excel=True) as inputs; creates a database named "hey" (which turns into `hey.sqlite3`), queries the table `test1` and writes the results to the command line. 

   ```python
   import csv_db
   cursor = csv_db.gen_db(["test1.xlsx", "test2.xlsx"], dbname="hey", excel=True)
   csv_db.query("select * from test1", cursor, cmnd_line=True)
   ```

2. In terminal, run `python3 example.py` to see this in action.

   ```
   $ python3 example.py
   Converting excel sheets to csv...
   Creating and populating database from csv files...
   Done

   ******* QUERY RESULT *******
   yoo hay hoow/   
   woot    wat?    hye 
   ow  ow  yah 
   ```

## FAQ
* [Basic SQL Statement Syntax and Concepts](https://www.w3schools.com/sql/sql_syntax.asp)
* [Great PostgreSQL tutorial for different statements](http://www.postgresqltutorial.com/)
* [PostgreSQL Command Line "Cheat Sheet"](https://gist.github.com/Kartones/dd3ff5ec5ea238d4c546)
* Getting the error "column not found" when executing a SQL query?  Don't use capitalized column names in your excel sheets, or you'll have to turn your postgresql query from 
`select A from one;` to `select "A" from one;`.  
NOTE: double quotes are used for column or table names, single quotes are used for specific query strings.  e.g. `select "A" from one where name='bob';`.  More on that [here](https://stackoverflow.com/questions/41396195/what-is-the-difference-between-single-quotes-and-double-quotes-in-postgresql).
* If you see this error: `pandas.errors.EmptyDataError: No columns to parse from file`, you may have tried to specify a filename with a path (ex: `files/alumni.xlsx`) in your `csv_db.gen_db()` function.  That function doesn't support file paths at this moment.  If there's demand, let me know and I'll add it.