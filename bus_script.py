import csv_db
# FIXME: CHANGE THESE NAMES TO THE NAMES OF YOUR FILES
cursor, connection = csv_db.gen_db(["test1.xlsx", "test2.xlsx"], dbname="temp", excel=True)


# FIXME: replace this with your query text
q = "select * from test1"
csv_db.query(q, cursor, csv=True)


csv_db.end(cursor, connection)