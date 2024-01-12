import sqlite3

conn=sqlite3.connect("student.db")
cur=conn.cursor()
cur.execute("SELECT CLASS FROM STUDENT WHERE NAME=\"tommy\";")
rows=cur.fetchall()
for row in rows:
    print(row)