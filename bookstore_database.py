# ------------------------------------------------------------------------------------------------
# TASK DESCRIPTION
# ------------------------------------------------------------------------------------------------

"""
Create a program that can be used by a bookstore clerks.
The program should allow the clerk to:
- Add new books to the database
- Update book information
- Delete books from the database
- Search the database to find a specific book

Create a database called ebookstore and a table called books.
The table should have the following structure:

columns: id, Title, Author, Qty
row1: 3001, A Tale of Two Cities, Charles Dickens, 30
row2: 3002, Harry Potter and the Philosopher's Stone, J.K. Rowling, 40
row3: 3003, The Lion, the Witch and the Wardrobe, C.S. Lewis, 25
row4: 3004, The Lord of the Rings, J.R.R. Tolkein, 37
row5: 3005, Alice in Wonderland, Lewis Carroll, 12

Populate the table with the above values.
You can also add your own values if you wish.

The program should present the user with the following menu:
1. Enter book
2. Update book
3. Delete book
4. Search books
0. Exit

The program should perform the function that the user selects.
The implementation of these functions is left up to you.
But - a demonstration of the topics we have covered should be shown.

"""

# ------------------------------------------------------------------------------------------------
#  DATABASE SETUP
# ------------------------------------------------------------------------------------------------

 # Import Python SQL module
import sqlite3

# Create a table called books
ebookstore = sqlite3.connect('books') # Create or open the database file
cursor = ebookstore.cursor()  # Get a cursor object

"""
Personal notes:
To make any changes to the database, we need a cursor object - used to execute SQL statements.
The statement '.commit' is used to save changes to the database, and 'close' is used to exit.
Always commit before closing or changes won't be saved.
"""

 # Create a table with the columns according to the task
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, Title TEXT,
                        Author TEXT, Qty INTEGER)
''')
 # Commit the changes to the database
ebookstore.commit()

# Table fields as list
table_fields = ["id","Title","Author","Qty"]

try: # Exception handling
    # Insert data rows according to the task description
    cursor.execute('''INSERT INTO books
                    VALUES ('3001', 'A Tale of Two Cities', 'Charles Dickens', '30'),
                    ('3002', "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', '40'),
                    ('3003', 'The Lion, the Witch and the Wardrobe', 'C.S. Lewis', '25'),
                    ('3004', 'The Lord of the Rings', 'J.R.R. Tolkein', '37'),
                    ('3005', 'Alice in Wonderland', 'Lewis Carroll', '12')''')
    # Commit the changes to the database
    ebookstore.commit()
except: # Exception handling
    pass

# ------------------------------------------------------------------------------------------------
#  FUNCTIONS
# ------------------------------------------------------------------------------------------------

# Display database
def display_database():
    cursor.execute('''SELECT * FROM books''')
    results = cursor.fetchall()
    print("------------------------------------------------------------------------------------------------------")
    print('EBOOKSTORE DATABASE')
    print("------------------------------------------------------------------------------------------------------")
    print(results)
    print("------------------------------------------------------------------------------------------------------")

# Display update menu
def update_menu():
    print("          [1] ID")
    print("          [2] Title")
    print("          [3] Author")
    print("          [4] Quantity (Qty)")
    print("          [0] Exit")

##############################################################
# MAIN PROGRAM SELECTIONS
##############################################################

while True:

    # ------------------------------------------------------------------------------------------------
    #  MAIN MENU
    # ------------------------------------------------------------------------------------------------

    print("------------------------------------------------------------------------------------------------------")
    print('EBOOKSTORE PROGRAM')
    print("------------------------------------------------------------------------------------------------------")
    print("Welcome to the ebookstore database main menu. Please select an option below:")
    print("          [1] Enter book")
    print("          [2] Update book")
    print("          [3] Delete book")
    print("          [4] Search book")
    print("          [0] Exit")

    # Possible selections
    selection_list = ['1','2','3','4','0']

    while True:
        selection = input()
        if selection not in selection_list:
            print("Selection not recognised. Please enter a number to select your option:")
            print("          [1] Enter book")
            print("          [2] Update book")
            print("          [3] Delete book")
            print("          [4] Search book")
            print("          [0] Exit")
        else:
            break

    # ------------------------------------------------------------------------------------------------
    #  [1] ENTER BOOK (Complete)
    # ------------------------------------------------------------------------------------------------

    # books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)

    if selection == '1':
        display_database()
        print("You have selected option - [1] Enter book.")
        print("Required entry fields: ID, TITLE, AUTHOR, QUANTITY.")

        print("Please enter book TITLE:")
        insert_title = input() # Title variable
        
        print("Please enter book AUTHOR:")
        insert_author = input() # Author variable
        
        print("Please enter book QUANTITY:")
        while True:
            insert_qty = input() # Quantity variable
            try: # Determine if provided qty is a valid input
                insert_qty = int(insert_qty) # User input as int
                break
            except:
                print("Please enter a valid QUANTITY:") # Error message

        print("Please enter book ID:")
        while True:
            insert_id = input() # ID variable
            try: # Determine if provided id is a valid input
                insert_id = int(insert_id)
                params = (insert_id,insert_title,insert_author,insert_qty)
                insert_query = "INSERT INTO books VALUES (?,?,?,?)" # Query syntax
                cursor.execute(insert_query,params) # Query
                ebookstore.commit() # Commit the changes to the database
                print("Thank you. Book entry has been added to database.")
                break
            except sqlite3.IntegrityError as error2: #sqlite3.IntegrityError: UNIQUE constraint failed: books.id
                print("Please enter a unique ID:") # Error message
                continue
            except ValueError as error1: # Wrong type entered
                print("Please enter a valid ID:") # Error message
                continue
        continue
        

    # ------------------------------------------------------------------------------------------------
    #  [2] UPDATE BOOK (Complete)
    # ------------------------------------------------------------------------------------------------

    # books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)

    elif selection == '2':
        display_database()
        print("You have selected option - [2] Update book.")
        print("Please enter the id number of the book to update:")
        while True:
            update_id = input() # User input id
            try: # Determine if provided id is a valid input
                update_int = int(update_id) # User input as int
                cursor.execute('''SELECT id FROM books WHERE id = (?)''', (update_int,))
                response = cursor.fetchall() # Book selection
                id_response = response[0][0] # Make sure selection exists
                break
            except:
                print("Please enter a valid id number of the book to update:") # Error message
                continue
        print("Please select the attribute to update:")
        update_menu() # Display options
        while True:
            selection = input() # Selected attribute to update
            if selection not in selection_list:
                print("Selection not recognised. Please select the attribute to update:")
                update_menu() # Display options
                continue
            elif selection != '0': # If not exit option
                print(f"You've selected option [{selection}]. Please enter the new value:")
                while True:
                    update_content = input() # User input variable
                    update_column = table_fields[int(selection)-1]  # Selected attribute index
                    try:
                        query = f"UPDATE books SET {update_column} = (?) WHERE id = (?)" # Query syntax
                        cursor.execute(query, (update_content,update_int,)) # Query
                        ebookstore.commit() # Commit the changes to the database
                        print("Thank you, the update is complete.") # End message
                        break
                    except:
                        print(f"Input not recognised. Please enter valid data for option [{selection}]:") # Error message
                        continue
            else: # If exit option
                print("- Exit to Main Menu - ") # Exit message
                break
        continue

    # ------------------------------------------------------------------------------------------------
    #  [3] DELETE BOOK (Complete)
    # ------------------------------------------------------------------------------------------------

    elif selection == '3':
        display_database()
        print("You have selected option - [3] Delete book.")
        print("Please enter the id number of the book to delete:")
        while True:
            delete_id = input() # User input variable
            try:
                delete_int = int(delete_id) # User input as int
                cursor.execute('''DELETE FROM books WHERE id = (?)''', (delete_int,)) # Query
                ebookstore.commit() # Commit the changes to the database
                print("Thank you, the selection has been deleted.") # End message
                break
            except:
                print("Please enter a valid id number of the book to delete:") # Error message
                continue
        continue

    # ------------------------------------------------------------------------------------------------
    #  [4] SEARCH BOOK (Complete)
    # ------------------------------------------------------------------------------------------------

    elif selection == '4':
        display_database()
        print("You have selected option - [4] Search book.")
        print("Search through book titles and author names.")
        print("Please enter a search keyword:")
        keyword = input()
        cursor.execute("SELECT * FROM books WHERE Title LIKE (?)",('%'+keyword+'%',)) # Query 1
        search_results_title = cursor.fetchall() # Search results 1
        cursor.execute("SELECT * FROM books WHERE Author LIKE (?)",('%'+keyword+'%',)) # Query 1
        search_results_author = cursor.fetchall() # Search results 1
        # Display the results
        if len(search_results_title)+len(search_results_author) == 0: 
            print('No results found.')
        else:
            print('Search results:')
            print(search_results_title+search_results_author)
        continue

    # ------------------------------------------------------------------------------------------------
    #  [0] EXIT (Complete)
    # ------------------------------------------------------------------------------------------------

    elif selection == '0':
        # Close database
        ebookstore.close()
        print("Thank you for using the ebookstore application!")
        print("- END OF PROGRAM -")
        break
