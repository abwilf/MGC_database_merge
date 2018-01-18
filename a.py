#!/usr/bin/env/python3
# import psycopg2
import csv_db
# conn = psycopg2.connect(host="localhost",database="mydb", user="postgres", password="postgres")
# cur = conn.cursor()

# dbname = 'mydb'
# text = "select exists(SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('" + dbname + "'));"

cur = csv_db.gen_db(['x.csv'], dbname="heya")
csv_db.query("select * from x;", cur, cmnd_line=True)

# text = "select * from a;"
# csv_db.query(text, cur, cmnd_line=True)
# cur.execute()
# colnames = [col.name for col in cur.description]
# print(colnames)
# print(cur.fetchall())
# csv_db.query("select * from a;", cur, cmnd_line=True)