import sqlite3
import datetime

# Working directory for this project
def set_wd():
    """
    Allows flexibility in working directory between developes
    Should be included in running of the program for all tests
    """
    print "Enter the full path for your working directory"

    workdir = raw_input("File path: \t")

    print "You've set your working directory to:"
    print workdir
    return workdir

# ==========================================================================
## HELPER FUNCTIONS ##

def input_db():
    """
    Prompts user for a .db file
    """
    name = raw_input("Database to open or edit: ")
    if name.endswith('.db'):
        input_db = name
    else:
        input_db = name + '.db'
    print input_db
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


# ==========================================================================
## CURSORS and CONNECTIONS ##

def open_connection(db):
    """
    Returns active cursor connection with database file
    """
    dbname = workdir + db
    # print(dbname)
    return sqlite3.connect(dbname).cursor()

def open_database():
    """
    Returns cursor connection to database file of user's choice
    """
    return open_connection(input_db())


# ==========================================================================
## DATA NAVIGATION ##

def view_tables(cur):
     """
     Lists all tables housed in a .db file given cursor connection.
     """
     cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
     print(cur.fetchall())

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

# If the user wants to update a table, pull the colum names


# ==========================================================================
## RUNNING THE PROGRAM ##

print("Running data_entry_script.py...")
#print("Today's date is {} ".format(get_date()))

#cur = open_database()

#view_tables(cur)
#view_columns(cur)

# Set the working directory
set_wd()

r_budget_list()

#working_list = budget_input()
#add_row_to_table(working_db, working_tab, working_list)
#check_changes(working_db, working_tab)
print("Success. Closing script.")


# ==========================================================================
