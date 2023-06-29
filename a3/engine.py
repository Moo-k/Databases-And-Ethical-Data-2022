import time

from simple_db import SimpleDatabase


def print_selected(header, rows):
    # header is a list of column names, rows is a list of rows
    # in turn, each row is a list of column values
    # e.g., if header = ['student name', 'ID', 'mark']
    # join command below will result in "student name, ID, mark"
    print('_' * 30) # repeat symbol '_' 30 times, thus creating a printed 'line'
    print(', '.join(header))
    print('_' * 30)
    for row in rows:
        print(', '.join(row))
    print('_' * 30)


def run_engine():
    print("Welcome to our Database Management System!")
    db = SimpleDatabase()
    indexes = db.get_indexes()

    while True:
        command = input("Enter command: ")
        if not command.endswith(";"):
            print("Commands should end with ; symbol.")
            continue

        command = command[:-1]  # to remove ; from the end
        if command == "exit":
            print("Leaving, bye!")
            break

        elif command == "show tables":
            # modify this section, so that the command
            # also prints columns for which index was built
            # note that our DBMS only supports loading one table at a time
            table_name = db.get_table_name()
            if table_name is None:
                print("... no tables loaded ...")
            else:
                print(table_name)
                index_names = []
                for i in indexes:
                    index_names.append(indexes[i][0])
                print("Indexes columns: ", index_names)

        elif command.startswith("copy "):
            # e.g., copy my_table from 'file_name.csv'
            words = command.split() # breaks down command into words
            # words[0] should be copy, words[1] should be table name, etc.
            if len(words) != 4:
                # we expect a particular number of words in this command
                print("Incorrect command format")
                continue

            table_name = words[1]
            file_name = words[3][1:-1] # to remove ' around file name
            db.load_table(table_name, file_name)

        elif command.startswith("select * from "):
            # e.g., select * from my_table where name="Bob"
            command = command.replace("=", " = ") # ensure spaces around =
            words = command.split() # breaks down command into words
            if len(words) != 8:
                # we expect a particular number of words in this command
                print("Incorrect command format")
                continue

            table_name = words[3]
            column_name = words[5]
            column_value = words[7][1:-1] # to remove " around the value

            start = time.time()
            header, rows = db.select_rows(table_name, column_name, column_value)
            end = time.time()

            if len(header) == 0:
                print("... no such table ...")
            else:
                print_selected(header, rows)
                print("Time elapsed: ", round(1000*(end - start)), " ms")

        # add code for processing create index and drop index here ...
        elif command.startswith("create index on "):
            # eg create index on id
            words = command.split() # breaks down command into words
            if len(words) !=  4:
                # we expect a particular number of words in this command
                print("Incorrect command format")
                continue

            column_name = words[3] # name of column to create index on, eg id
            
            if column_name not in db.columns: # check if column exists in table
                print("Requested column not found, cannot index")

            for i in indexes: # check if column already has an index
                if column_name == indexes[i][0]:
                    print("Requested column already has index")
                    break

            b_tree = BTree.construct_b_tree(db.columns) # construct b-tree using selected column

            indexes.append(column_name,b_tree) # store indexed columns as a pair of the column name and the constructed b-tree

        elif command.startswith("drop index on "):
            # eg drop index on id
            words = command.split() # breaks down command into words
            if len(words) !=  4:
                # we expect a particular number of words in this command
                print("Incorrect command format")
                continue

            index_name = words[3] # eg id

            for i in indexes: # checks if requested index exists
                if indexes[i][0] == index_name: # if it does, delete it
                    del indexes[i]
                    print("Deleting index ", index_name);
                    break

            print("Requested index not found, cannot delete") # if requested index does not exist

        else:
            print("Unrecognized command!")

        print() # empty line after each command

# def search_index(column_name,column_value):
#     selected_rows = []
#     for i in indexes:
#         if column_name in indexes[i][0]: # if index exists
#             selected_rows = indexes[i][1].search_key(column_value)
#     return selected_rows

if __name__ == "__main__":
    run_engine()
