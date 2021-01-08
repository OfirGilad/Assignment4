import sqlite3
import os
import atexit
import sys

is_database_exist = os.path.isfile('database.db')
database_SARS_CoV_2 = sqlite3.connect('database.db')
database_cursor = database_SARS_CoV_2.cursor()


def tables_creation():
    with database_SARS_CoV_2:
        if not is_database_exist:
            database_cursor.execute("""CREATE TABLE logistics
                                    (id INTEGER PRIMARY KEY,
                                    name STRING NOT NULL,
                                    count_sent INTEGER NOT NULL,
                                    count_received INTEGER NOT NULL)""")
            database_cursor.execute("""CREATE TABLE suppliers
                                    (id INTEGER PRIMARY KEY,
                                    name STRING NOT NULL,
                                    logistic INTEGER REFERENCES logistics(id))""")
            database_cursor.execute("""CREATE TABLE clinics
                                    (id INTEGER PRIMARY KEY,
                                    location STRING NOT NULL,
                                    demand INTEGER NOT NULL,
                                    logistic INTEGER REFERENCES logistics(id))""")
            database_cursor.execute("""CREATE TABLE vaccines
                                    (id INTEGER PRIMARY KEY,
                                    date DATE NOT NULL,
                                    supplier INTEGER REFERENCES suppliers(id),
                                    quantity INTEGER NOT NULL)""")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
