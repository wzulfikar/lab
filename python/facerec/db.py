import postgresql

def setup_db():
    db = postgresql.open('pq://user:pass@localhost:5434/db')
    db.execute("create extension if not exists cube;")
    db.execute("drop table if exists vectors")
    db.execute("create table vectors (id serial, file varchar, vec_low cube, vec_high cube, profile_id int);")
    db.execute("create table profiles (id serial, name varchar);")
    db.execute("create index vectors_vec_idx on vectors (vec_low, vec_high);")

setup_db()
