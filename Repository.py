from Dao import _Logistics, _Suppliers, _Clinics, _Vaccines
from Dto import Logistic, Supplier, Clinic, Vaccine
import sqlite3
import atexit


def print_table(list_of_elements):
    for element in list_of_elements:
        print(element)


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self._logistics = _Logistics(self._conn)
        self._suppliers = _Suppliers(self._conn)
        self._clinics = _Clinics(self._conn)
        self._vaccines = _Vaccines(self._conn)
        self._next_vaccine_index = 1

    def close(self):
        self._next_vaccine_index = 1
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        DROP TABLE IF EXISTS 'logistics';
        DROP TABLE IF EXISTS 'suppliers';
        DROP TABLE IF EXISTS 'clinics';
        DROP TABLE IF EXISTS 'vaccines';
        """)
        self._conn.executescript("""
        CREATE TABLE logistics (
            id INTEGER PRIMARY KEY,
            name STRING NOT NULL,
            count_sent INTEGER NOT NULL,
            count_received INTEGER NOT NULL
        );
        
        CREATE TABLE suppliers (
            id INTEGER PRIMARY KEY,
            name STRING NOT NULL,
            logistic INTEGER REFERENCES logistics(id)
        );
        
        CREATE TABLE clinics (
            id INTEGER PRIMARY KEY,
            location STRING NOT NULL,
            demand INTEGER NOT NULL,
            logistic INTEGER REFERENCES logistics(id)
        );
        
        CREATE TABLE vaccines (
            id INTEGER PRIMARY KEY,
            date DATE NOT NULL,
            supplier INTEGER REFERENCES suppliers(id),
            quantity INTEGER NOT NULL
        );
        """)

    def print_all(self):
        print("vaccines")
        print_table(self._conn.execute("SELECT * FROM vaccines"))
        print("suppliers")
        print_table(self._conn.execute("SELECT * FROM suppliers"))
        print("clinics")
        print_table(self._conn.execute("SELECT * FROM clinics"))
        print("logistics")
        print_table(self._conn.execute("SELECT * FROM logistics"))

    def config_decode(self, config):
        is_first_line = True
        with open(config, 'r') as input_file:
            for line in input_file:
                text_line = line.split(",")
                if is_first_line:
                    vaccines_length = int(text_line[0])
                    suppliers_length = int(text_line[1])
                    clinics_length = int(text_line[2])
                    logistics_length = int(text_line[3])
                    is_first_line = False
                elif vaccines_length > 0:
                    temp = Vaccine(text_line[0], text_line[1], text_line[2], text_line[3])
                    self._vaccines.insert(temp)
                    vaccines_length = vaccines_length - 1
                    self._next_vaccine_index = self._next_vaccine_index + 1
                elif suppliers_length > 0:
                    temp = Supplier(text_line[0], text_line[1], text_line[2])
                    self._suppliers.insert(temp)
                    suppliers_length = suppliers_length - 1
                elif clinics_length > 0:
                    temp = Clinic(text_line[0], text_line[1], text_line[2], text_line[3])
                    self._clinics.insert(temp)
                    clinics_length = clinics_length - 1
                else:
                    temp = Logistic(text_line[0], text_line[1], text_line[2], text_line[3])
                    self._logistics.insert(temp)
                    logistics_length = logistics_length - 1

    def return_logistics(self):
        return self._logistics

    def return_suppliers(self):
        return self._suppliers

    def return_clinics(self):
        return self._clinics

    def return_vaccines(self):
        return self._vaccines

    def return_next_vaccine_index(self):
        return self._next_vaccine_index


# the repository singleton
repo = _Repository()
atexit.register(repo.close)
