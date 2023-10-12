import streamlit as st
import pyodbc
import pandas as pd

st.set_page_config(page_title="View Data")

st.markdown("# View Data")
st.sidebar.header("View Data")
st.write(
    """Use the buttons below to view data from the Voka Database."""
)

# Define the connection string
connection_string = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-MAX;DATABASE=Voka;Trusted_Connection=yes;'

# Create a function to connect to the SQL Server database
def connect_to_database():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        return None
    
if st.button("Select Accounts"):
    st.subheader('Data from SQL Server')

    conn = connect_to_database()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Account")  # Replace 'Accounts' with your table name
        data = cursor.fetchall()
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'Account'")
        column_names = [row.COLUMN_NAME for row in cursor.fetchall()]
    
        conn.close()

        # Display the retrieved data in a table
        if data:
            st.write(column_names)
            df = pd.DataFrame(data, columns=column_names)

            st.table(df)
        else:
            st.warning('No data found.')
    else:
        st.error('Connection to the database failed. Check the connection string.')
