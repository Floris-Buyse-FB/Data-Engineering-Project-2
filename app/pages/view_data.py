import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.exc import ProgrammingError
import re
import pandas as pd

st.set_page_config(page_title="View Data")

st.markdown("# View Data")
st.sidebar.header("View Data")
st.write(
    """Use the buttons below to view data from the Voka Database."""
)

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

# Get a list of all tables in the database
inspect = inspect(conn)
table_list = inspect.get_table_names()
table_list.sort()

# Check if the user wants to see the column names of a table
see_col_names = st.checkbox('See column names')

# Get the list of columnnames for the selected table and determine ID column
table_name= st.selectbox('Select a table', table_list)
table_name_index = table_list.index(table_name)
columns_list = inspect.get_columns(table_list[table_name_index])

if see_col_names:

    ###########################################
    # List representation of the column names #
    ###########################################
    st.write([x['name'] for x in columns_list])

    ###############################################
    # Markdown representation of the column names #
    ###############################################
    # cols_list_name = [x['name'] for x in columns_list]
    # list_as_text = '\n'.join([f'- {item}' for item in cols_list_name])
    # st.markdown(list_as_text)

# Give a list of possible queries to select from
query_list = ['SELECT * FROM ' + table_name
              , 'KIES ZELF EEN QUERY'
              , 'SELECT TOP 100 * FROM ' + table_name
              , 'SELECT TOP 1000 * FROM ' + table_name
              ,
]

# Generate a list of possible queries to select from
for col in columns_list:
    query_list.append('SELECT ' + col['name'] + ' FROM ' + table_name)

query = st.selectbox('Select a query to retrieve data from the database', query_list)

# If the user wants to enter a custom query, give the option to do so
if query == 'KIES ZELF EEN QUERY':
    custom_query = st.text_input('Enter a query to retrieve data from the database')
    if custom_query:
        query = custom_query

# Display the data from the selected table
if table_name:
    st.subheader('Data from  ' + table_name + ' table')

    if conn:
        
        if query:
            try:
                data = pd.read_sql(query, conn)
            
                conn.close()

                # Display the retrieved data in a table
                st.dataframe(data)

            except ProgrammingError as e:
                error_lines = str(e).split('\n')

                pattern = r"Invalid column name '([^']+)"

                match = re.search(pattern, error_lines[0])

                if match:
                    column_name_error = match.group(0)
                    st.error(f"{column_name_error}'")


    else:
        st.error('Connection to the database failed. Check the connection string.')
