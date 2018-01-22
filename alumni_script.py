import csv_db
dbname = 'mydb'
cur = csv_db.gen_db(['alumni.csv', 'dev_db.csv'], dbname=dbname)

# text = """
# update alumni set first='holla' where first='Walter';
# """
# cur = csv_db.connect(dbname)
# csv_db.query(text, cur, cmnd_line=True, print_out=False)
