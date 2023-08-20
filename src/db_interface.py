"""
    @author: Matheus José Oliveira dos Santos
    Last Edit: 26/05/2023
"""

import pandas as pd
import urllib.parse 
import psycopg2

# ex:
# import os
# variable_value = os.getenv('VARIABLE_NAME')

class DB_interface:
    def __init__(self,db_name) -> None:
        print('connecting in: '+db_name)

        self.db = psycopg2.connect(
        host="localhost",
        port=5432,
        database=db_name,
        user="Matheus",
        password="password",
        )

        self.cursor = self.db.cursor()
        return

    def __enter__(self):
        pass
    
    def __exit__(self,exc_type, exc_value, exc_traceback):
        self.close_db()

    def add_row(self,table_name:str, *args) -> None:
        if type(args[0]) == list:
            aux_values = ','.join(["'"+str(i)+"'" for i in args[0]])
        else:
            aux_values = ','.join(["'"+str(i)+"'" for i in args])
        command = "INSERT INTO {0} VALUES ({1});".format(table_name,aux_values)
        #print(command)
        self.cursor.execute(command)

    def replace_table(self,table_name:str,df:pd.DataFrame, should_print = False) -> None:
        self.delete_all_rows_of_table(table_name)
        self.append_table_fast(table_name,df)
        #for linha in range(0, df.shape[0]):
        #    aux = df.loc[linha, :].values.tolist()
        #    if should_print == True:
        #        print(aux)
        #    self.add_row(table_name,aux)
    
    def replace_table_slow(self,table_name:str,df:pd.DataFrame, should_print = False) -> None:
        self.delete_all_rows_of_table(table_name)
        for linha in range(0, df.shape[0]):
            aux = df.loc[linha, :].values.tolist()
            if should_print == True:
                print(aux)
            self.add_row(table_name,aux)

    def append_table(self,table_name:str,df:pd.DataFrame, should_print = False) -> None:
        for linha in range(0, len(df)):
            aux = df.loc[linha, :].values.tolist()
            try:
                self.add_row(table_name,aux)
            except Exception as e:
                print(e)
            if should_print == True:
                print(aux)

    def append_table_fast(self,table_name:str,df:pd.DataFrame) -> None:

        divs = [df[i:i + 1000] for i in range(0, len(df), 1000)]
        i=0
        for div in divs:
            sql_query = f"INSERT INTO {table_name} ({', '.join(div.columns)}) VALUES "
            sql_query += ', '.join(['(' + ', '.join([f"'{str(val)}'" if pd.notna(val) else 'NULL' for val in row]) + ')' for row in div.values])
            i=i+1
            print(i)
            self.cursor.execute(sql_query)
    
    def delete_all_rows_of_table(self,table_name:str) -> None:
        command = "DELETE FROM {0}".format(table_name)
        self.cursor.execute(command)

    def get_table(self,table_name:str, company_name = None) -> pd.DataFrame:

        if company_name == None:
            command = "SELECT * FROM {0}".format(table_name)
        else:
            command = "SELECT * FROM {0} where BBGTicker = '{1}'".format(table_name,company_name)

        df_return = pd.read_sql_query(command, self.db)
        
        return df_return
    
    def read_by_command(self, command:str) -> pd.DataFrame:
        return pd.read_sql_query(command, self.db)

    def execute_command(self, command:str) -> None:
        self.cursor.execute(command)

    def close_db(self):
        self.db.close()
        print('DB Closed')

    def save_db(self):
        self.db.commit()
        print('DB Saved')