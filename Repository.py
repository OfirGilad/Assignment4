import sqlite3


class Repository:
    def __init__(self,db_name):
        self._conn = sqlite3.connect(db_name)
        #TODO: add DAOs

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        database_cursor = self._conn.cursor()
        with self._conn:
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