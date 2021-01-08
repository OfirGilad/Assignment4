from Dao import _Logistics
from Dao import _Suppliers
from Dao import _Clinics
from Dao import _Vaccines
from Dto import Logistic
from Dto import Supplier
from Dto import Clinic
from Dto import Vaccine
import sqlite3
import atexit


class _Repository:
    def __init__(self, database_sars_cov_2_conn):
        self._conn = sqlite3.connect(database_sars_cov_2_conn )
        self.logistics = _Logistics(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.vaccines = _Vaccines(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
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
#        self._conn.execute("""
#        CREATE TABLE logistics (
#            id INTEGER PRIMARY KEY,
#            name STRING NOT NULL,
#            count_sent INTEGER NOT NULL,
#            count_received INTEGER NOT NULL
#        )""")
#        self._conn.execute("""
#        CREATE TABLE suppliers (
#            id INTEGER PRIMARY KEY,
#            name STRING NOT NULL,
#            logistic INTEGER REFERENCES logistics(id)
#        )""")
#        self._conn.execute("""
#        CREATE TABLE clinics (
#            id INTEGER PRIMARY KEY,
#            location STRING NOT NULL,
#            demand INTEGER NOT NULL,
#            logistic INTEGER REFERENCES logistics(id)
#        )""")
#        self._conn.execute("""
#        CREATE TABLE vaccines (
#            id INTEGER PRIMARY KEY,
#            date DATE NOT NULL,
#            supplier INTEGER REFERENCES suppliers(id),
#            quantity INTEGER NOT NULL
#        )""")

    def config_decode(self, config):
        is_first_line = True
        with open(config) as input_file:
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
                    self.vaccines.insert(temp)
                    vaccines_length = vaccines_length - 1
                elif suppliers_length > 0:
                    temp = Supplier(text_line[0], text_line[1], text_line[2])
                    self.suppliers.insert(temp)
                    suppliers_length = suppliers_length - 1
                elif clinics_length > 0:
                    temp = Clinic(text_line[0], text_line[1], text_line[2], text_line[3])
                    self.clinics.insert(temp)
                    clinics_length = clinics_length - 1
                else:
                    temp = Logistic(text_line[0], text_line[1], text_line[2], text_line[3])
                    self.logistics.insert(temp)
                    logistics_length = logistics_length - 1
