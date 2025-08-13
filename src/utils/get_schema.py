import pandas as pd
import sqlite3


def get_all_schema(db_path:str):
    """
    Params:
    db_path: the file path of SQLite database (.sqlite)

    Return ALL the table/columns, the corresponding foreign keys and primary keys in the database.
    """
    # results
    Tables_columns = ""
    Foreign_keys = []
    Primary_keys = []

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Extract the table names
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        # columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        primary_keys = [f"{table_name}.{col[1]}" for col in columns if col[5] == 1]
        
        # foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        foreign_keys_helper = cursor.fetchall()
        foreign_keys = [f"{table_name}.{fk[3]} = {fk[2]}.{fk[4]}" for fk in foreign_keys_helper]

        # store
        Tables_columns = Tables_columns + f"Table {table_name} , columns = [ {' , '.join(column_names)} ] "
        Primary_keys.extend(primary_keys)
        Foreign_keys.extend(foreign_keys)

    # close the connection'
    conn.close()
    # post-process
    seq_pk = f"Primary_keys = [ {' , '.join(Primary_keys)} ]"
    seq_fk = f"Foreign_keys = [ {' , '.join(Foreign_keys)} ]"

    return f"{Tables_columns}\n{seq_pk}\n{seq_fk}" 
    


def get_table_info(db_path:str, table_name:str):
    """
    Params:
    db_path: the file path of SQLite database (.sqlite)
    table_name: the name of table in the db

    Return the certain table/columns, the corresponding foreign keys and primary keys in the database.
    """

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Extract the table names
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # columns
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    primary_keys = [f"{table_name}.{col[1]}" for col in columns if col[5] == 1]
    
    # foreign keys
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    foreign_keys_helper = cursor.fetchall()
    foreign_keys = [f"{table_name}.{fk[3]} = {fk[2]}.{fk[4]}" for fk in foreign_keys_helper]

    # store
    tables_columns = f"Table {table_name} , columns = [ {' , '.join(column_names)} ] "


    # close the connection'
    conn.close()

    return tables_columns, primary_keys, foreign_keys



def get_schema_from_query(db_path:str, query:str):
    """
    Params:
    query: the VQL query
    db_path: the file path of SQLite database (.sqlite)

    Return the table/columns mentioned in the given query, the corresponding foreign keys and primary keys.
    """
    query_tokens = query.split(' ')
    Tables_columns = ""
    Foreign_keys = []
    Primary_keys = []

    table_indices = [index+1 for index, token in enumerate(query_tokens) if token == 'from']
    joint_indices = [index+1 for index, token in enumerate(query_tokens) if token == 'join']
    table_indices.extend(joint_indices)
    for idx in table_indices:
        table_name = query_tokens[idx]
        table_columns, primary_keys, foreign_keys = get_table_info(db_path, table_name)

        # store
        Tables_columns = Tables_columns + table_columns
        Primary_keys.extend(primary_keys)
        Foreign_keys.extend(foreign_keys)


    return Tables_columns.lower(), f"Primary_keys = [ {' , '.join(Primary_keys)} ]".lower(), f"Foreign_keys = [ {' , '.join(Foreign_keys)} ]".lower()


# test
if __name__ == "__main__":
    db_id = "party_people"
    # query = """visualize bar select minister , count ( minister ) from party where party_name != 'progress party' group by minister"""

    db_path = f"data/database/{db_id}/{db_id}.sqlite"
    # a, b,c = get_schema_from_query(db_path,query)
    a,b,c = get_all_schema(db_path)

    print(a.lower())

    print(b.lower())

    print(c.lower())
