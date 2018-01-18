import csv_db
cursor = csv_db.gen_db(["a.xlsx", "b.xlsx"], dbname="hey", excel=True)
# query = "select * from ALUMNI_CLEANED where dev_id=2487861"
# csv_db.query(query, cursor, cmnd_line=True)
