import csv_db

dbname = 'mydb'
# cur = csv_db.gen_db(['alumni.xlsx', 'dev_db.xlsx'], dbname=dbname, excel=True)
# csv_db.gen_db(['one.xlsx', 'two.xlsx'], dbname='heya', excel=True)
cur = csv_db.connect(dbname)
text = """
select * from alumni where dev_id is NULL;
"""
csv_db.query(text, cur)
# text = """
# update alumni
# set first=dev_db.first_name,
# last=dev_db.last_name,
# address=dev_db.address,
# city=dev_db.city,
# state=dev_db.state,
# zip=dev_db.zip,
# cell=dev_db.cell,
# home=dev_db.home_phone,
# email=dev_db.email
# from dev_db
# where alumni.dev_id = dev_db.dev_id;
# """

# text = """
# select distinct * from (select alumni.first, alumni.last from alumni inner join dev_db on (alumni.last=dev_db.last_name) and (alumni.last='Cole')) as x;
# """
# csv_db.query(text, cur)

# text = """
# select count(alumni.dev_id) from alumni inner join dev_db on alumni.dev_id = dev_db.dev_id;
# """
# csv_db.query(text, cur, print_out=False, result=False)

# text = """
# update alumni
# set
# dev_id=dev_db.dev_id,
# address=dev_db.address,
# city=dev_db.city,
# state=dev_db.state,
# zip=dev_db.zip,
# cell=dev_db.cell,
# home=dev_db.home_phone,
# email=dev_db.email
# from dev_db
# where alumni.first=dev_db.first_name and alumni.last = dev_db.last_name;
# """
# csv_db.query(text, cur, print_out=False, result=False)



# # cur = csv_db.connect(dbname)
# text = """
# update alumni
# set first=dev_db.first_name,
# last=dev_db.last_name,
# address=dev_db.address,
# city=dev_db.city,
# state=dev_db.state,
# zip=dev_db.zip,
# cell=dev_db.cell,
# home=dev_db.home_phone,
# email=dev_db.email
# from dev_db
# where alumni.dev_id = dev_db.dev_id;
# """
# csv_db.query(text, cur, print_out=False, result=False)


# text = """
# update alumni
# set
# dev_id=dev_db.dev_id,
# address=dev_db.address,
# city=dev_db.city,
# state=dev_db.state,
# zip=dev_db.zip,
# cell=dev_db.cell,
# home=dev_db.home_phone,
# email=dev_db.email
# from dev_db inner join alumni on dev_db.dev_id=alumni.dev_id;
# """
# select alumni.dev_id from
# alumni inner join dev_db on alumni.dev_id = dev_db.dev_id
# where alumni.last <> dev_db.last_name;
# """
# csv_db.query(text, cur, cmnd_line=True)
