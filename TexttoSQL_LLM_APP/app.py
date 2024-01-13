from dotenv import load_dotenv
import pandas as pd

load_dotenv()


import streamlit as st
import os
import sqlite3
import google.generativeai as genai

#configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## FunctionTo Load Google Gemini Model

def get_gemini_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.text

def get_gemini_formatted_response(question,prompt):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[1],question])
    return response.text


## Function to retrieve query from the Database

def read_sql_query(sql,db):
    conn=sqlite3.connect(db)
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    for row in rows:
        print(row)
    return rows


## Define Your Prompt
prompt=[
      """
      You are an expert in converting English questions to SQL query!
      The SQL database has the name STUDENT and has the following columns - NAME, CLASS, 
      SECTION \n\nFor example,\nExample 1 - How many entries of records are present?, 
      the SQL command will be something like this SELECT COUNT(*) FROM STUDENT ;
      \nExample 2 - Tell me all the students studying in Machine learning class?, 
      the SQL command will be something like this SELECT * FROM STUDENT 
      where CLASS="Machine learning"; 
      also the sql code should not have ``` in beginning or end and sql word in output

      """, 
      """
Reformat the SQL output responses from a student database. 
The database has the following columns: NAME, CLASS, SECTION, MARKS.Ensure that 
If the response is a single numerical value it may represent the total number of entries in the database.
"""
]

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App to Retrieve SQL Data")

# Connect to SQLite
connection = sqlite3.connect("student.db")
cursor = connection.cursor()

# Display all records in a table
st.title("Student Database")
data = cursor.execute('''SELECT * FROM STUDENT''')
columns = [description[0] for description in cursor.description]
df = pd.DataFrame(data.fetchall(), columns=columns)
st.table(df)

# Close the connection
connection.close()

# Display example prompts below the database
st.subheader("Example Prompts")
st.text("1. How many entries of records are present?")
st.text("2. Tell me all the student names studying in Machine learning class?")
st.text("3. Give me the average marks of students in each class.")

st.subheader("Input: ")

question=st.text_input("",key="input")

submit=st.button("Ask the Question")


# If submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=str(read_sql_query(response,"student.db"))
    formatted_response = get_gemini_formatted_response(response,prompt)
    st.subheader("The Response is")
    st.write(formatted_response)
    # for row in response:
    #     my_string = str(row)

    #     print(my_string)
        
