import csv

# open FILENAME
def opening():
    f = open(FILENAME)
    csv_i = csv.reader(f)
    csv_i.next()
    return csv_i

# reading in column labels
def readLabels():
    f = open(FILENAME)
    csv_i = csv.reader(f)
    for i in range(1):
        labels = csv_i.next()
    cols = {}
    for i in range(len(labels)):
        cols[labels[i]] = i
    print 'fields:\t', labels, '\n'
    return [cols, labels]

# show unique elements in a column
def printCol():
    print 'Show unique values in a field...'
    csv_i = opening()
    field = raw_input('field:\t')
    record_list = []
    if field in COLS.keys():
        for entry in csv_i:
            record_list.append(entry[COLS[field]])
    for e in set(record_list):
        print e
    print ''

# filtering - show (field elements) where (filter field) is (filter val)
def filtering():
    print 'Show elemets of field given filtering...'
    csv_i = opening()
    view_field = raw_input('show:\t')
    filter_field = raw_input('where:\t')
    filter_val = raw_input('is:\t')
    if view_field and filter_field in COLS.keys():
        for entry in csv_i:
            if entry[COLS[filter_field]] == filter_val:
                print entry[COLS[view_field]]
    print ''

# searching - search (field) for (val), show all entries
def search():
    print 'Search for entries (all or field-specific)...'
    csv_i = opening()
    search_field = raw_input('field:\t')
    search_val = raw_input('for:\t')
    if search_field == 'all':
        for entry in csv_i:
            for element in entry:
                if search_val.lower() in element.lower():
                   print entry
                #else: print 'No records found.'
    if search_field in COLS.keys():
        for entry in csv_i:
            if search_val.lower() in entry[COLS[search_field]].lower():
               print entry
    print ''

# change value of an entry
def changeVal():
    new_contents = []
    with open(FILENAME, 'rb') as fi:
        csv_i = csv.reader(fi)
        print 'Change value of an entry...'
        search_field = raw_input('where:\t')
        search_val = raw_input('is:\t')
        if search_field in COLS.keys():
            for entry in csv_i:
                if search_val.lower() in entry[COLS[search_field]].lower():
                    print 'entry:\t',entry
                    change_field = raw_input('change field:\t')
                    if change_field in COLS.keys():
                        change_val = raw_input('to:\t\t')
                        entry[COLS[change_field]] = change_val
                        print 'new:\t',entry
                new_contents.append(entry)
    with open(FILENAME, 'wb') as fo:
        csv_o = csv.writer(fo)
        csv_o.writerows(new_contents)
    print ''

# add entry
def add():
    to_add = []
    with open(FILENAME, 'rb') as fi:
        csv_i = csv.reader(fi)
        print 'Add a new book...'
        for field in LABELS:
            data = raw_input(field+':\t')
            to_add.append(data)
    with open(FILENAME, 'a') as fo:
        csv_o = csv.writer(fo)
        csv_o.writerow(to_add)
    print ''

# delete entry
def delete():
    to_remove = []
    new_contents = []
    with open(FILENAME, 'rb') as fi:
        csv_i = csv.reader(fi)
        print 'Search for book to remove...'
        search_field = raw_input('field:\t')
        search_val = raw_input('for:\t')
        if search_field == 'all':
            for entry in csv_i:
                new_contents.append(entry)
                for element in entry:
                    if search_val.lower() in element.lower():
                       print 'Entry to remove: ', entry
                       to_remove.append(entry)
        if search_field in COLS.keys():
            for entry in csv_i:
                new_contents.append(entry)
                if search_val.lower() in entry[COLS[search_field]].lower():
                   print 'Entry to remove: ', entry
                   to_remove.append(entry)
        rem = raw_input('Remove record? (y/n) >>  ')
        if rem in ['y','Y','yes','Yes', 'YES']:
            for row in to_remove:
                new_contents.remove(row)
            print 'Records removed.'
        else:
            print 'Records kept.'
    with open(FILENAME, 'wb') as fo:
        csv_o = csv.writer(fo)
        csv_o.writerows(new_contents)
    print ''



# ================================================================== #
## MAIN ##
FILENAME = 'booklist.csv'
label_data = readLabels()
COLS = label_data[0]
LABELS = label_data[1]
go = True
todo = raw_input("""\
What would you like to do? \n
- LIST       by field?
- FILTER     records?
- SEARCH     records?
- EDIT       a record?
- ADD        a record?
- REMOVE     a record?

>>> """).lower()
options = ['list','search','filter','edit','add','remove','q']
def check():
    global todo
    while todo not in options:
         print 'Sorry. Please type one of the options:\n', options
         todo = raw_input('>>> ').lower()
    print ''
check()

def recheck():
    global todo
    todo = raw_input('>>> ')
    check()

while go:
    if todo == 'list':
        printCol()
        recheck()
    if todo == 'search':
        search()
        recheck()
    if todo == 'filter':
        filtering()
        recheck()
    if todo == 'edit':
        changeVal()
        recheck()
    if todo == 'remove':
        delete()
        recheck()
    if todo == 'add':
        add()
        recheck()
    if todo == 'q':
        break




# ================================================================== #
