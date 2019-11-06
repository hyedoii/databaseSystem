import psycopg2 as pg


db_connector = {
    'host': "postgres",
    'user': "dbuser",
    'dbname': "dbapp",
    'password': "1234"
}

connect_string = "host={host} user={user} dbname={dbname} password={password}".format(
    **db_connector)

with pg.connect(connect_string) as conn:
    with conn.cursor() as cur:
        cur.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
        for table in cur.fetchall():
            print(table)

# with pg.connect(connect_string) as conn:
#     with conn.cursor() as cur:
#         cur.execute(
#             "CREATE TABLE guser (      id integer primary key,      name varchar(20),      email varchar(20)    );")
