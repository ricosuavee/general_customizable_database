from columns import * 

def input_tab():
    """
    Prompts user for the name of a table inside a .db file
    Return type: string
    """
    input_tab = raw_input("Table name: ")
    return input_tab

def pull_table_names(cur):
     """
     Lists all tables housed in a .db file given cursor connection.
     Return type: list
     """
     # Execute SQLite command that pulls all table names from the current cursor
     cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
     # cur.fetchall returns the table names as a list of tuples
     tuple_output = (cur.fetchall())

     # Initiate output variable
     table_list = []

     for i in tuple_output:
         table_list.append(str(i)[2:7])

     return table_list

def print_table_names(table_list):
    """
    Dependencies: takes output from pull_table_names()
    Return type: null
    """

    print "The database currently contains these tables:"
    print "============================================"
    for i in table_list:
        print i

    print "============================================"

def compare_input_to_db(table_name, table_list):
    """
    Compare the table name input by the user to the existing tables within a database
    Return type: BOOLEAN
    """

    output = False

    for i in table_list:
        if i == table_name:
            output = True

    return output

def view_or_create_table(boolean_value, table_name):
    """
    Executes two different paths depending on boolean value input
    dependencies: depends on output of input_tab and compare_input_to_db
    Return type: string
    """

    if boolean_value == True:
        user_answer = raw_input(table_name + " already exists. \n \n Would you like to edit (e), view (v) the contents of this table, or enter a new (n) table name? \n Enter e, v, or n\t")
        return user_answer
    else:
        user_answer = raw_input(table_name + " does not exist in this database. Would you like to create a new table (nt), or re-enter a different table (dt)? \n Enter nt or dt \t  ")
        return user_answer

def table_fork(cur):
    """
    Asks the user to input a table, then based on input, directs user either to edit/view a table or create a table
    Dependencies: pull_table_names(), print_table_names(), input_tab(), view_or_create_table(), assembling_columns(), assemble_sql_create_tbl(), create_table_if_not_exists()
    Return type: null
    """

    tab_list = pull_table_names(cur)
    print_table_names(tab_list)

    tab_name = input_tab()

    test = compare_input_to_db(tab_name, tab_list)

    input_letter = view_or_create_table(test, tab_name)

    if input_letter == "dt" or input_letter == "n":
        table_fork(cur)
    elif input_letter == "nt":
        col_list = assembling_columns()
        print 2.2
        sql_str = assemble_sql_create_tbl(col_list, tab_name)
        print sql_str
        print 2.3
        create_table_if_not_exists(cur, sql_str)
        print "New table " + tab_name + " created"
    elif input_letter == "e":
        pass
    elif input_letter == "v":
        pass
    else:
        print "None of the letters entered match an option"
        return table_fork(cur)

def create_table_if_not_exists(cursor, sql_command):
    """
    Given a string SQLite command and a cursor object, executes the CREATE TABLE IF NOT EXISTS SQLite command
    dependencies: relies on output from assemble_sql_create_tbl() and create_cursor()
    Return type: Null (creates or edits table with .db file)
    """

    #cursor.execute("""DROP TABLE test_budget;""")

    cursor.execute(sql_command)

#========================================================================
## In Development
def add_row_to_table(db, table, input_list):
    """
    Creates a new entry in a table with the contents of an input_list
    """
    connection = open_connection(db)
    cursor = connection.cursor()

    #print("We got here")
    #print(input_list)
    #print(len(input_list))

    todays_date = get_date()
    input_list.append(todays_date)

     #if input_list[0] != NULL:
         #input_list.insert(0, NULL)

    input_tup = tuple(input_list)
    print("Data to be added to the table:")
    print(input_tup)

    insert_string = "INSERT INTO {tn} VALUES (NULL,?,?,?,?,?,?,?)"
    cursor.execute(insert_string.format(tn = table), input_tup)

    # Saves the changes
    print(connection.total_changes)
    connection.commit()

    connection.close()
