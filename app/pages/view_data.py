import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData, desc, inspect
from sqlalchemy.orm import declarative_base
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
        URL = f'mssql+pyodbc://{st.secrets["SERVER_NAME"]}/{st.secrets["DB_NAME"]}?trusted_connection=yes&driver=ODBC+Driver+17 for SQL Server'
        engine = create_engine(URL)
        conn = engine.connect()
        return conn
    except:
        return 'Error while connecting to database.'
    
# Retrieve data from the database
conn = connect_to_database()

inspect = inspect(conn)
table_list = inspect.get_table_names()
table_list.sort()
table_name= st.selectbox('Select a table', table_list)
if table_name:
    st.subheader('Data from  ' + table_name + ' table')

    if conn:
        
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, conn)
            
        conn.close()

        # Display the retrieved data in a table
        st.dataframe(data)

    else:
        st.error('Connection to the database failed. Check the connection string.')
