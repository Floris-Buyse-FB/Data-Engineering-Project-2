import pandas as pd
from sqlalchemy import create_engine
import os

# Initialization of MS SQL Server database connection
DB_NAME = 'Voka'
SERVER_NAME = 'ASUS_FLORIS'
URL = f'mssql+pyodbc://{SERVER_NAME}/{DB_NAME}?trusted_connection=yes&driver=ODBC+Driver+17 for SQL Server'

# Read CSV into Pandas DataFrame
DATA_DIR = os.path.join(os.getcwd(), 'data_clean')
csv_path = f'{DATA_DIR}/Account_fixed.csv'

print("Reading CSV file")

df = pd.read_csv(csv_path)

print("Connecting to database")

# Connect to the database
engine = create_engine(URL)

print("Writing to database")

# Write DataFrame to SQL
table_name = 'Account'  # Change this to match your table name
df.to_sql(table_name, con=engine, if_exists='append', index=False)

print("Done")
# Close the connection
engine.dispose()
