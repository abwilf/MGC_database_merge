

## Install prerequisites


#### Windows
**FIXME**

#### Mac
Copy and paste this into terminal (it may take a while)
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew update
brew install git
cd ~/Desktop
git clone https://github.com/abwilf/MGC_database_merge.git
brew install pip
brew install python3
pip install -r

```


## Run the scripts

### Alumni Relations Manager
**FIXME**

### Business Team
To manage the inventory database, you'll need to access functions in `csv_db.py`.  The relevant functions you'll use are below.  For a full example, scroll down or [click here](https://github.com/abwilf/MGC_database_merge#full-example)

#### Generate Database
```python
# Requires: array of input_files = [<filename>.csv], dbname (optional), excel: if files being inputted are in xlsx format or not (True/False)
# Effects: returns db cursor with dbname, having incorporated input files to db with <filename> as table name
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
#    cmnd_line (optional): Do you want it to print to the command line? True or False. 
#       By default the function prints results to a csv
#    file_out (optional): If not printing to command line, specify the filename
#        you would like to write to - defaults to "out.csv"
#
# Modifies: db.sqlite3 (or whatever db cursor is connected to)
#
# Effects: always returns results as python object for programmer
#    if cmnd_line, returns results on command line
#    else, prints results to file_out in csv format
def query(text, cursor, cmnd_line=False, file_out="out.csv"):
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

   You should see something like this:

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