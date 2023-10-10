import pandas as pd
from sqlalchemy import create_engine
import os

# Initialization of MS SQL Server database connection
DB_NAME = 'Voka'
SERVER_NAME = 'ASUS_FLORIS'
URL = f'mssql+pyodbc://{SERVER_NAME}/{DB_NAME}?trusted_connection=yes&driver=ODBC+Driver+17 for SQL Server'

# Read CSV into Pandas DataFrame
DATA_DIR = os.path.join(os.getcwd(), 'data_clean')

def fill_db(file):

    print(f"Reading {file}")
    df = pd.read_csv(os.path.join(DATA_DIR, file), sep=',')

    print("Connecting to database")

    engine = create_engine(URL)

    print("Writing to database")

    try:
        table_name = file[:-10]
        table_name = table_name.replace(' ', '_')
        df.to_sql(table_name, con=engine, if_exists='append', index=False)

    except:
        print(f"Error writing {file} to database\nTrying again after all other files are written")
        failed_files.append(file)
        return False

    print("Done\n============================\n")
    engine.dispose()

failed_files = []

for file in os.listdir(DATA_DIR):
    if file.endswith(".csv") and (not file.endswith("_Merge.csv")):

        result = fill_db(file)
        if result == False:
            continue

print("Trying to write failed files again")

for file in failed_files:
    
    result = fill_db(file)
    if result == False:
        continue