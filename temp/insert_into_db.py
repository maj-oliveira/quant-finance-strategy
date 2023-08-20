import os
import sys

import pandas as pd
import sqlite3
import psycopg2


sys.path.append(os.getcwd()+'\\src')
import db_interface

def main():

    conn_sqlite3 = sqlite3.connect("temp/data.db")
    query = "SELECT * FROM data"
    df = pd.read_sql_query(query, conn_sqlite3)
    df = df.iloc[:,1:]
    print(df.head())
    
    first_row = df.iloc[0, :]
    list_of_values = first_row.tolist()

    my_db = db_interface.DB_interface("FINANCE_DB")

    with my_db:
        my_db.replace_table_slow("financials", df)
        my_db.save_db()



if __name__ == "__main__":
    main()