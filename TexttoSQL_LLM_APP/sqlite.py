import sqlite3

## Connect to SQLite
connection=sqlite3.connect("student.db")

# Create a cursor object to insert record, Create table
cursor=connection.cursor()

#create the table
table_info="""
Create table STUDENT(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25), MARKS INT);

"""
cursor.execute(table_info)

#Insert Records

cursor.execute('''Insert Into STUDENT values('John','Web Development','A',90)''')
cursor.execute('''Insert Into STUDENT values('Smith','Web Development','B',100)''')
cursor.execute('''Insert Into STUDENT values('Gracia','Web Development','C',86)''')
cursor.execute('''Insert Into STUDENT values('Sophia','Cryptography','A',50)''')
cursor.execute('''Insert Into STUDENT values('Olivia','Cryptography','B',35)''')
cursor.execute('''Insert Into STUDENT values('Michael','Cryptography','C',40)''')
cursor.execute('''Insert Into STUDENT values('Tommy','Machine learning','A',65)''')
cursor.execute('''Insert Into STUDENT values('Pol','Machine learning','A',73)''')
cursor.execute('''Insert Into STUDENT values('Arthur','Machine learning','B',20)''')
cursor.execute('''Insert Into STUDENT values('Linda','Machine learning','C',10)''')



# Display all records

print('The inserted records are')
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

# Commit your connection
connection.commit()
connection.close()





