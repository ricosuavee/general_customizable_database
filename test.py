import datetime

# ==========================================================================
## HELPER FUNCTIONS ##

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
def get_date():
    """
    Returns current date in YYYY-MM-DD format
    Return type: string
    """
    return datetime.date.today().strftime("%Y-%m-%d")

# ==========================================================================
## CURSORS and CONNECTIONS ##
from database_access import *

# =============================================== ===========================
## DATA NAVIGATION ##
from tables import *

# ==========================================================================
## DATA ENTRY ##

## In development
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
## In development
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
## In development
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
## In development
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
table_fork(cur)
print 3
close_db_connection(conn)
print("Success. Closing script.")
# #=====================================




# ==========================================================================
