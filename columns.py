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

#========================================================================
## In Development
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
