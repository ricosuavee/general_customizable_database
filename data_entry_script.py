import sqlite3
import datetime

# Working directory for this project
def set_wd():
    """
    Allows flexibility in working directory between developes
    Should be included in running of the program for all tests
    Return type: string
    """
    print "Enter the full path for your working directory"

    workdir = raw_input("File path: \t")


    print "\n You've set your working directory to:"
    print workdir + "\n"
    return workdir

# ==========================================================================
## HELPER FUNCTIONS ##

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

def input_tab():
    """
    Prompts user for the name of a table inside a .db file
    Return type: string
    """
    input_tab = raw_input("Table name: ")
    return input_tab

def get_date():
    """
    Returns current date in YYYY-MM-DD format
    Return type: string
    """
    return datetime.date.today().strftime("%Y-%m-%d")


# ==========================================================================
## CURSORS and CONNECTIONS ##

def open_db_connection(db):
    """
    Returns connection with specified database file
    Return type: connection object
    """
    # print(dbname)
    return sqlite3.connect(db)

def set_output_to_text(connection):
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

# =============================================== ===========================
## DATA NAVIGATION ##

## Table navigation ##
def view_tables(cur):
     """
     Lists all tables housed in a .db file given cursor connection.
     Return type: list
     """
     cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
     print "The db currently contains these tables \n"
     # cur.fetchall returns the table names as a list of tuples
     tuple_output = (cur.fetchall())
     print tuple_output
     str_output = ' '.join(map(str, tuple_output))
     print str_output


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

##  Defining columns for a table ##
def col_question():
    """
    dependencies: calls assembling_columns()
    Return type: List or null list
    """
    answer = raw_input("\tWould you like to define table columns (y/n)\t")
    if answer == 'y':
        print # Formatting print statement
        return input_col_names()
    elif answer == 'n':
        return []
    else:
        print "'y' and 'n' are the only options. Please pick one"

def num_columns():
    """
    Establishes the number of columns to be added to a table
    Return type: int
    """
    answer = raw_input("\tHow many columns would you like to add? \n\t (Answer must be an integer):\t")
    count = 0
    return int(answer)

def col_names():
    """
    Prompts user to enter string for column name
    dependencies: none
    Return type: string
    """
    col_input = raw_input("Enter column name:\t")

    return col_input

def input_data_types():
    """
    Prompts user to enter data types
    Function dependence: None
    Return type: string
    """
    # Create menu of options for the user
    print "These are the available data types"
    print "\ttext# --- A text field(# = number of possible characters allowed. Max = 255)"
    print "\tnum   --- A real number field"
    print "\tdate  --- A field for entering the date"

    data_type = raw_input("Enter data type for this column:\t ")


    # Verify that the data type matches one of the three options
    if data_type[0:4] == "text" and int(data_type[4:])<=255 or data_type == "num" or data_type == "date":
        return data_type
    else:
        print "Data type must be input exactly as displayed in the menu"
        return input_data_types()

def assembling_columns():
    """
    Prompts user for number of num_columns
    Asks user to enter name and data type for each new columns
    Returns a list of tuples of column names and data types
    dependencies: num_columns(), col_names(), input_data_types()
    Return type: list of tuples
    """
    #Initialize empty master list
    master_list = []

    col_count = num_columns()
    count = 0
    while count < col_count:
        col_name = col_names()
        col_type = input_data_types()

        # Make a list pairing column name and data type
        col_list = [col_name, col_type]
        # Convert list to tuple so it is immutable
        col_tuple = tuple(col_list)
        master_list.append(col_tuple)
        count = count + 1


    print "These are the column names and data types"
    return master_list

def assemble_sql_create_tbl(tuple_list, table_name):
    """
    Input type: list of tuples
    Note: Input is intended to come from assembling_columns() fxn
    Given a list of tuple pairs, return a CREATE TABLE IF NOT EXISTS SQLite command
    Return type: string
    """
    #    Issue flag: The three SQLite data types used here are DATE, VARCHAR, and FLOAT. If numbers put into FLOAT columns are integers, will this cause a problem?

    sql_str = "CREATE TABLE IF NOT EXISTS " + table_name + " (entry_number INTEGER PRIMARY KEY"

    for (col_name, data_type) in tuple_list:
        sql_str = sql_str + ", " + col_name

        if data_type[0:4] == "text":
            sql_str = sql_str + " VARCHAR" + "(" + data_type[4:] + ")"
        elif data_type == "num":
            sql_str = sql_str + " FLOAT"
        else:
            sql_str = sql_str + " DATE"

    sql_str = sql_str + ");"

    # Returns a string
    return sql_str

## Creating a table from defined columns ##
def create_table_if_not_exists(cursor, sql_command):
    """
    Given a string SQLite command and a cursor object, executes the CREATE TABLE IF NOT EXISTS SQLite command
    dependencies: relies on output from assemble_sql_create_tbl() and create_cursor()
    Return type: Null (creates or edits table with .db file)
    """

    #cursor.execute("""DROP TABLE test_budget;""")

    cursor.execute(sql_command)

## Within table navigation ##
def view_columns(cur):
    """
    Lists all columns in table of a .db file given cursor connection.
    """
    table = raw_input("Table name: ")
    cur.execute('SELECT * FROM ' + table)
    col_names = [cn[0] for cn in cur.description]
    rows = cur.fetchall()
    print(col_names)

# ==========================================================================
## DATA ENTRY ##
def budget_list():
    """
    Prompts users for six entries to populate a budget-specific table
    Entries: source, notes, category, type, date, amount
    """
    # perhaps shift these variable names to col1, col2, etc, so that they apply not just to a budget, but any table
    # The text can be substituted with column headers eg. Enter <col1_header>:
    src = raw_input("Enter expenses source: \t\t")
    nts = raw_input("Any notes? Enter here: \t\t")

    # Here I could create a proxy drop-down menu with print statements and creative use of variables, with single letter codings
    # eg entertainment = e, transportation = t, daily_living = d, etc
    # Then, with a long if statement, I could create the options for the second tier...it would be like a crude drop down menu
    # eg if tier_one == "e", print a menu with all the "types" from that category

    # but for now, to test, just a crude text entry:
    cat = raw_input("Enter expenses category: \t")
    typ = raw_input("Enter category type: \t\t")
    dat = raw_input("Enter date (YYYY-MM-DD): \t")
    amt = float(raw_input("Enter amount: \t\t\t"))

    entry_list = [src, nts, cat, typ, dat, amt]
    print entry_list
    return entry_list


## -------------------------------------------------------------------------
## Ryan's working on 'menu' of options and matching for source and category...

def r_budget_list():
        """
        (Ryan's version of the budget_list() function)
        Prompts users to populate a budget-specific table
        Entries: source, notes, category, #type, date, amount
        """
        sources = ['Staples', 'Home Depot', 'Target', 'Alex', 'Ryan']
        # in time, create a bit list of sources
        categories = list_to_unique()
        dat = raw_input("Date (YYYY-MM-DD): \t")
        # in time, build a date robustness feature
        src = test_input(sources, "Source")
        cat = test_input(categories, "Category")
        nts = raw_input("Notes: \t\t\t")
        amt = float(raw_input("Amount: \t\t"))
        entry_list = [src, nts, cat, dat, amt]
        print entry_list
        return entry_list

# need a function that reads in column names
# need a function that reads in category names from column 'category'

def list_to_unique():
    """
    Returns set of unique objects from potentially repetitive list.
    """
    lst = ['groceries', 'eating out', 'home goods', 'home improvements', 'eating out', 'eating out', 'home goods', 'groceries', 'groceries', 'outdoor rec', 'home goods', 'groceries', 'home goods', 'home goods', 'home goods', 'home goods', 'home goods', 'eating out']
    cat_set = set(lst)
    #for i in cat_set: print "\t", i
    return cat_set

def test_input(incoming_set, input_type):
    """
    Allows for short-hand user input when typing from a set of options.
    If input non-existent, alerts user of new item creation.
    """
    print "\t---------------------"
    for i in incoming_set: print "\t", i
    user_input = raw_input("{}:\t\t".format(input_type))
    for i in incoming_set:
        if i.startswith(user_input):
            yn = raw_input("\tDid you mean '{}'? (y/n)\t".format(i))
            if yn == 'y':
                user_input = i
                break
            if yn == 'n':
                continue
    else:
        print "\t'{}' did not match an existing".format(user_input), input_type.lower()
        user_input = raw_input("\tWhat did you mean?\t")
    if user_input not in incoming_set:
        print "\tNew", input_type.lower(), "'{}' created.".format(user_input)
    print "\t\t\t", user_input
    return user_input


## -------------------------------------------------------------------------

def budget_input():
    """
    Checks if the user would like to enter a budget item
    """
    enter_data = raw_input("Would you like to enter a budget item? (y/n): ")

    if enter_data == "n":
        print("Congratulations, you're done budgeting today!")

    elif enter_data == "y":
        return budget_list()
    else:
        print("Error: 'y' or 'n' required as input")
        budget_input()

# ==========================================================================
## DATA VERIFICATION ##

def check_changes(db, table):
    """
    Returns all of the entries from a specific date for data quality control and validation
    """
    date = (get_date(),)

    # Open or create a database 'db'
    connection = open_connection(db)

    # Open a cursor object
    cursor = connection.cursor()

    # Return a string instead of default Unicode object
    connection.text_factory = str

    # Print all of the rows that were modified today
    select_string = 'SELECT * FROM {tn} WHERE entry_date=?'
    for row in cursor.execute(select_string.format(tn = table), date):
        print(row)

    connection.close()


# ==========================================================================
## USER INTERFACE FUNCTIONS ##

# Need a function to modify rows individually by their entry code in
#      case of data entry errors.

# Instead of relying on the user to input a "type" of database,
#       ask the user to either create or open a .db file and table.

# If the user wants to update a database, pull the table names

# If the user wants to update a table, pull the colum names


# ==========================================================================
## RUNNING THE PROGRAM ##

print("Running data_entry_script.py...\n")
print("Today's date is {} \n".format(get_date()))

## Test block WH ##
# The following block goes through the following step (numbers correspond to print statements)
# 1) Opens a databate connection and creates a cursor object (open_db_connection(), create_cursor())
# 2) Inspects tables in the database (view_tables()); prompts user to enter a new table name or current table names (input_tab());
# 2.1) As if the user had entered a new table name, the script prompts the user to enter column name and data types for a new table (assembling_columns())
# 2.2)  The script assembles an SQLite command from the input column names and data_types to create the table if it does not exist (assemble_sql_create_tbl())
# 2.3) The script creates a new table in the database if it does not already exist
# 2.4) The script inspects tables in the databases again
# 3) The script closes the database connection.
#=====================================

# Set the working directory
workdir = set_wd()
print 1

# working_db generates the full path + file name of working Database
# Note: Does not actually open a connection to any database
working_db = add_file_path(input_db(), workdir)

#conn is an open connection to the working database
conn = open_db_connection(working_db)
# cur is an active cursor from a database connection w/ working_db file
cur = create_cursor(conn)

# This changes the output from Unicode to UTF-8 (removes "u" from the front of each entry returned by SQLite)
set_output_to_text(conn)

print 2
view_tables(cur)
# test_tab = input_tab()
# print 2.1
# col_list = assembling_columns()
# print 2.2
# sql_str = assemble_sql_create_tbl(col_list, test_tab)
# print sql_str
# print 2.3
# create_table_if_not_exists(cur, sql_str)
# print "New table " + test_tab + " created"
# print 2.4
# view_tables(cur)
#
# print 3
# close_db_connection(conn)
# #=====================================
#
# # #view_columns(cur)
# #
# # #r_budget_list()
# # print 4
# # #working_list = budget_input()
# # print 5
# # #add_row_to_table(working_db, working_tab, working_list)
# # print 6
# # #check_changes(working_db, working_tab)
print("Success. Closing script.")


# ==========================================================================
