import csv_db
dbname = 'mydb'
cur, conn = csv_db.gen_db(['alumni.xlsx', 'dev.xlsx'], dbname=dbname, excel=True)
# cur, conn = csv_db.gen_db(['alumni.csv', 'dev.csv'], dbname=dbname) 
# cur, conn = csv_db.connect(dbname)

# set everything except email and cell (find alums with matching first names first, then dev_id)
q = """
update alumni
set 
dev_id = dev.dev_id,
prefix=dev.title,
first=dev.first,
last=dev.last,
address=dev.address,
city=dev.city,
state=dev.state,
zip=dev.zip,
home=dev.home,
no_contact=dev.no_contact,
no_solicitation=dev.no_solicitation,
no_email=dev.no_email
from dev
where alumni.first=dev.first and alumni.last = dev.last
returning alumni.dev_id, alumni.first, alumni.last;
"""
csv_db.query(q, cur)

q = """
update alumni
set 
dev_id = dev.dev_id,
prefix=dev.title,
first=dev.first,
last=dev.last,
address=dev.address,
city=dev.city,
state=dev.state,
zip=dev.zip,
home=dev.home,
no_contact=dev.no_contact,
no_solicitation=dev.no_solicitation,
no_email=dev.no_email
from dev
where alumni.dev_id = dev.dev_id
returning alumni.dev_id, alumni.first, alumni.last;
"""
csv_db.query(q, cur)

# set email
q = """update alumni
set
email=dev.email
from dev
where alumni.dev_id = dev.dev_id and alumni.email_dirty_bit != TRUE
returning alumni.dev_id, alumni.first, alumni.last;
"""
csv_db.query(q, cur)

# set cell phone
q = """update alumni
set
cell=dev.cell
from dev
where alumni.dev_id = dev.dev_id and alumni.cell_dirty_bit != TRUE
returning alumni.dev_id, alumni.first, alumni.last;
"""
csv_db.query(q, cur)


csv_db.query("select * from alumni", cur, csv=True, file_out="alumni_new.csv")
csv_db.end(cur, conn)