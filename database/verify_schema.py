import sqlite3

conn=sqlite3.connect("../data/sqlite/execumind.db")

cursor=conn.cursor()
cursor.execute("""select name from sqlite_master where type='table'""")
tables=cursor.fetchall()

print("\nTables in Database :\n")

for table in tables:
    print(table[0])

conn.close()



