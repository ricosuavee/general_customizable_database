import sqlite3

def input_db():
    """
    Prompts user for a .db filename
    Returns string of .db filename
    Note: this function does not open a connection to an SQLite DB
    Return type: string
    """
    name = raw_input("Database to open or edit: ")
    if name.endswith('.db'):
        input_db = name
    else:
        input_db = name + '.db'
    print "This is the file name"
    print input_db
    return input_db

def add_file_path(db_str, dir_str):
    """
    Input: string of .db filename, string with directory in which to find/create .db file
    Attaches the given directory to the .db file to return string of the full file path
    Return type: string
    """
    full_path = dir_str + db_str

    print "This is the full file path"
    print full_path
    return full_path

def open_db_connection(db):
    """
    Returns connection with specified database file
    Return type: connection object
    """
    # print(dbname)
    return sqlite3.connect(db)

def set_output_to_text(connection):
    """
    Sets the output of the fetchall method (and fetchone?) to text, rather than the default unicode output from a database
    Return type: null
    """
    connection.text_factory = str

def create_cursor(connection):
    """
    Returns active cursor
    Return type: cursor method of connection
    """
    return connection.cursor()

def close_db_connection(connection):
    """
    This method should save changes and closes a db connection
    Return type: null
    """
    connection.commit()
    connection.close()
    print "The connection has been closed"
