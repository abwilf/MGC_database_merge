import csv_db
cursor = csv_db.gen_db(["test1.xlsx", "test2.xlsx"], dbname="hey", excel=True)
csv_db.query("select * from test1", cursor)
