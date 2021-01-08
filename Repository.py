from Dao import _Logistics
from Dao import _Suppliers
from Dao import _Clinics
from Dao import _Vaccines
import sqlite3
import atexit


class _Repository:
    def __init__(self, database_sars_cov_2):
        self._conn = sqlite3.connect(database_sars_cov_2)
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


repo = _Repository()
atexit.register(repo._close)
