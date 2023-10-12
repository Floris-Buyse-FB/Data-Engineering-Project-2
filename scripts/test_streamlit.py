import streamlit as st
import pyodbc

# Define the connection string
connection_string = r'DRIVER={ODBC Driver 17 for SQL Server};SERVER=LAPTOP-MAX;DATABASE=Voka;Trusted_Connection=yes;'

# Create a function to connect to the SQL Server database
def connect_to_database():
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except pyodbc.Error as e:
        return None

# Define a Streamlit app with multiple pages
def main():
    st.title('Multi-Page Streamlit App with SQL Server')

    # Create a sidebar for page navigation
    page = st.sidebar.checkbox("Select a page:", ["Home", "Request Data","Input Data"])

    if page == "Home":
        st.subheader("Home Page")
        st.write("Welcome to the SQL Server Database App. Use the sidebar to navigate.")

    elif page == "Display Data":
        st.subheader("Display Data from SQL Server")
        conn = connect_to_database()
        if conn:
            cursor = conn.cursor()
            st.table(cursor.execute("SELECT TOP 10 * FROM Account"))
            result = cursor.fetchall()
            st.write("Sample Data:")
            st.write(result)
            cursor.close()
            conn.close()
        else:
            st.error("Connection to the database failed. Check the connection string.")

if __name__ == '__main__':
    main()
