# Men's Glee Club Database Merge Script
#### Table of Contents
[Description and Motivation](https://github.com/abwilf/MGC_database_merge#description-and-motivation)

[Installing the Prerequisites](https://github.com/abwilf/MGC_database_merge#installing-the-prerequisites)

[Running the Scripts](https://github.com/abwilf/MGC_database_merge#running-the-scripts)

[FAQ](https://github.com/abwilf/MGC_database_merge#FAQ)

## Description and Motivation
This program implements an easy to use computer utility that takes in spreadsheets from SMTD's development office and the MGC alumni database, merges them, and returns a new spreadsheet.

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
1. Ask development to send you a spreadsheet in excel format (`.xlsx`) with the following columns:

   `dev_id, title, first, last, no_contact, no_solicitation, no_email, email, address, city, state, zip, home, cell`

2. Clean up the file they send you by naming it `dev.xlsx` and changing the column names to match the ones above.  It doesn't matter if there are extra columns, but the spreadsheet **must have the columns above named properly to work**.  The colors of the spreadsheet don't affect the program's performance.

3. Move the files `alumni.xlsx` and `dev.xlsx` into the `mgc_db_merge` folder, overwriting files if necessary.

   NOTE: It is important that you name the files exactly as they are named above.  If you'd _really_ like to, you can also name them `alumni.csv` and `dev.csv`, but you will need to type `#` at the beginning of line 3 of `alumni_script.py`, delete the `#` at the beginning of line 4, and save the file before you run the commands below.  If you don't have a coding text editor, I would just convert the files from `.csv` to `.xlsx`.

4. Copy and paste this code into your terminal.

   ```
   source env/bin/activate
   python3 alumni_script.py
   ```
The new database is in the file `alumni_new.csv`

5. Open `alumni_new.csv` in excel, save it as `alumni.xlsx` (tutorial on that [here](https://support.office.com/en-us/article/save-a-workbook-in-another-file-format-6a16c862-4a36-48f9-a300-c2ca0065286e)) and reupload it to the Alumni Google Drive so the rest of the team has an updated copy.


### Business Team
To manage the inventory database, you'll need to access functions in `csv_db.py`.  The relevant functions you'll use are below.  For a full example, see [`alumni_script.py`](https://github.com/abwilf/MGC_database_merge/blob/master/alumni_script.py), or [a simpler example in this document](https://github.com/abwilf/MGC_database_merge#full-example).

#### Generate Database
```python
# Requires: array of input_files = [<filename>.csv], dbname (optional)
#       excel = if files being inputted are in xlsx format or not (all must be in same format)
# Effects: returns db cursor with dbname, having incorporated input files to db with <filename> as table name
def gen_db(input_files=[], dbname="db", excel=False)  
```
##### Example 1
This code passes in two test files in excel format with the database name "hey" (generates database `hey` on your postgreSQL server, which you can access at the command line with `psql hey`.  See the [FAQ](https://github.com/abwilf/MGC_database_merge#faq) for tips on working with postgreSQL).  Saves return result to `cursor` and `connection` variables for future use in queries (more on this below).  `hey` will have two tables, `test1` and `test2`.
```python
cursor, connection = csv_db.gen_db(["test1.xlsx", "test2.xlsx"], dbname="hey", excel=True)
```

##### Example 2
This code takes in one csv file, generates database called `db` by default.  Note: there's no need to pass an `excel` variable here because it defaults to `False`
```python
cur, conn = csv_db.gen_db(["test1.csv"])
```

#### Query Database
```python
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
def query(text, cursor, res=True, cmnd_line=False, csv=False, file_out="out.csv")
```
##### Example 1
This code executes a query on the database passed in by `cursor`, the return value of `gen_db()`.  The first parameter is text in SQL format.  The second is the cursor variable.  The third specifies that the user would like to print the results of the query to the command line.

Note: I will not be writing a tutorial of SQL commands, as that has been done more effectively by real experts.  [Start here](https://www.w3schools.com/sql/sql_syntax.asp) if you'd like to learn.

```python
csv_db.query("select * from test1;", cursor, cmnd_line=True)
```

##### Example 2
This code also executes a query on the database passed in by `cursor`. Since the `csv` parameter is specified, it writes the results to a csv, `out.csv`, by default.  It returns the result to `res`
```python
res = csv_db.query("select * from test1", cursor, csv=True)
```

#### Connect to Existing Database
```python
# Requires: dbname must be a database in postgres on this machine, postgres must be running (brew services start postgres),
# must have user and superuser privileges for postgres, postgres == (username, password)
# Effects: returns cursor and connection objects connected to postgreSQL database <dbname>
def connect(dbname)
```

##### Example
```python
cur, conn = csv_db.connect(dbname)
```

#### End the Program
```python
# R: valid cursor and connection objects connected to postgreSQL databases
# M: commits changes executed by cur on db
# E: closes connection, commits changes.  MUST call this function at end of code
def end(cur, conn):
```



#### Full Example
1. We have a file: `example.py`.  The code here takes in 2 excel files (since the inputs are excel files, mark excel=True) as inputs; creates a database named "hey" (which turns into `hey`), queries the table `test1` and writes the results to the command line. 

   ```python
   import csv_db
   cursor, connection = csv_db.gen_db(["test1.xlsx", "test2.xlsx"], dbname="hey", excel=True)
   csv_db.query("select * from test1", cursor, cmnd_line=True)
   csv_db.end(cursor, connection)
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
* How can I connect to and test my database without using `query()`?
   More on this in the bullet points below, but here's a short tutorial
   1. Pop open a terminal shell
   2. run `psql -U postgres` to connect to your server
   3. enter `\lt` to see the list of databases
   4. enter `\q` to quit, `psql <db_name>` to access that database directly
   5. run `\dt` to see what tables you have
   6. execute any queries you'd like
* [Basic SQL Statement Syntax and Concepts](https://www.w3schools.com/sql/sql_syntax.asp)
* [Great PostgreSQL tutorial for different statements](http://www.postgresqltutorial.com/)
* [PostgreSQL Command Line "Cheat Sheet"](https://gist.github.com/Kartones/dd3ff5ec5ea238d4c546)
* Getting the error "column not found" when executing a SQL query?  Don't use capitalized column names in your excel sheets, or you'll have to turn your postgresql query from 
   `select A from one;` to `select "A" from one;`.  
   NOTE: double quotes are used for column or table names, single quotes are used for specific query strings.  e.g. `select "A" from one where name='bob';`.  More on that [here](https://stackoverflow.com/questions/41396195/what-is-the-difference-between-single-quotes-and-double-quotes-in-postgresql).
* If you see this error: `pandas.errors.EmptyDataError: No columns to parse from file`, you may have tried to specify a filename with a path (ex: `files/alumni.xlsx`) in your `csv_db.gen_db()` function.  That function doesn't support file paths at this moment.  If there's demand, let me know and I'll add it.