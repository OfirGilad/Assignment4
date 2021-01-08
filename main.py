import sqlite3
import os
import atexit
import sys

from Repository import _Repository

# is_database_exist = os.path.isfile('database.db')
# database_sars_cov_2_conn = sqlite3.connect('database.db')
# database_cursor = database_sars_cov_2_conn.cursor()
#
#
# def tables_creation():
#     with database_sars_cov_2_conn:
#         if not is_database_exist:
#             database_cursor.execute("""CREATE TABLE vaccines
#                                     (id INTEGER PRIMARY KEY,
#                                     date DATE NOT NULL,
#                                     supplier INTEGER REFERENCES suppliers(id),
#                                     quantity INTEGER NOT NULL)""")
#             database_cursor.execute("""CREATE TABLE suppliers
#                                     (id INTEGER PRIMARY KEY,
#                                     name STRING NOT NULL,
#                                     logistic INTEGER REFERENCES logistics(id))""")
#             database_cursor.execute("""CREATE TABLE clinics
#                                     (id INTEGER PRIMARY KEY,
#                                     location STRING NOT NULL,
#                                     demand INTEGER NOT NULL,
#                                     logistic INTEGER REFERENCES logistics(id))""")
#             database_cursor.execute("""CREATE TABLE logistics
#                                     (id INTEGER PRIMARY KEY,
#                                     name STRING NOT NULL,
#                                     count_sent INTEGER NOT NULL,
#                                     count_received INTEGER NOT NULL)""")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def main(args):
    db_path = 'database.db'
    is_database_exist = os.path.isfile(db_path)
    config = args[1]
    orders = args[2]
    output = args[3]
    repo = _Repository(db_path)
    if not is_database_exist:
        repo.create_tables()
        repo.config_decode(config)
    repo.execute_orders(orders, output)


if __name__ == '__main__':
    print_hi('PyCharm')
#   main(system.argv)
