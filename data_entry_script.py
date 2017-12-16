import sqlite3
import datetime

# Working directory for this project
workdir = '/Users/ryanmcelroy/Desktop/ryan/coding/general_customizable_database/'

# ==========================================================================
## To Do ##
# Break into modules and packages. It will be more useful this way.


# ==========================================================================
## HELPER FUNCTIONS ##

def input_db():
    """
    Prompts user for a .db file
    """
    input_db = raw_input("Database name (must have .db extension): ")
    return input_db

def input_tab():
    """
    Prompts user for the name of a table inside a .db file
    """
    input_tab = raw_input("Table name: ")
    return input_tab

def get_date():
    """
    Returns current date in YYYY-MM-DD format
    """
    return datetime.date.today().strftime("%Y-%m-%d")

## WORK ON THIS FUNCTION
#def view_tables(db):
#     """
#     List all of the tables housed in a .db file
#     """
#     SELECT name FROM my_db.sqlite_master WHERE type='table';


# ==========================================================================
## CURSORS and CONNECTIONS ##

def open_connection(db):
    dbname = workdir + db
    print(dbname)
    # Return dbname as either opened or new .db file
    return sqlite3.connect(dbname)


# ==========================================================================
## DATA ENTRY ##

def budget_list():
    """
    Prompts users for six entries to populate a budget-specific table
    Entries: source, notes, category, type, date, amount
    """
    # perhaps shift these variable names to col1, col2, etc, so that they apply not just to a budget, but any table
    # The text can be substituted with column headers eg. Enter <col1_header>:
    src = raw_input("Enter expenses source: ")
    nts = raw_input("Any notes? Enter here: ")

    # Here I could create a proxy drop-down menu with print statements and creative use of variables, with single letter codings
    # eg entertainment = e, transportation = t, daily_living = d, etc
    # Then, with a long if statement, I could create the options for the second tier...it would be like a crude drop down menu
    # eg if tier_one == "e", print a menu with all the "types" from that category

    # but for now, to test, just a crude text entry:
    cat = raw_input("Enter expenses category: ")
    typ = raw_input("Enter category type: ")
    dat = raw_input("Enter date (YYYY-MM-DD, numeric values only): ")
    amt = float(raw_input("Enter amount: "))

    entry_list = [src, nts, cat, typ, dat, amt]
    print entry_list
    return entry_list

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

def create_table_if_not_exists(db, table, input_list):
    """
    Writes an input list to a specified table in a specified database
    If the database does not exist, it will be created
    If the table does not exist within the database, it will be created
    """
    # Can this be more general? Right now it's pretty specific to a budget

    # Opens a cursor object
    # A cursor is used to traverse the records from the result set
    connection = open_connection(db)

    cursor = connection.cursor()
    #cursor.execute("""DROP TABLE test_budget;""")

    sql_command = "CREATE TABLE IF NOT EXISTS " + table + "(entry_number INTEGER PRIMARY KEY, source VARCHAR(30),notes VARCHAR(60), category VARCHAR (20), type VARCHAR (20), transaction_date DATE, amount FLOAT, entry_date DATE);"

    cursor.execute(sql_command)
    connection.commit()
    connection.close()

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

#     if input_list[0] != NULL:
#         input_list.insert(0, NULL)

    input_tup = tuple(input_list)
    print("Data to be added to the table:")
    print(input_tup)

    insert_string = "INSERT INTO {tn} VALUES (NULL,?,?,?,?,?,?,?)"
    cursor.execute(insert_string.format(tn = table), input_tup)

    # Saves the changes
    print(connection.total_changes)
    connection.commit()

    connection.close()

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

# If the user wants to update a table, pull the table names


# ==========================================================================
## RUNNING THE PROGRAM ##

print("Running data_entry_script.py")
working_db = input_db()
working_tab = input_tab()
working_date = get_date()
print(working_date)
open_connection(working_db)
#working_list = budget_input()
#add_row_to_table(working_db, working_tab, working_list)
#check_changes(working_db, working_tab)
print("Success")


# ==========================================================================
