from Dao import _Logistics
from Dao import _Suppliers
from Dao import _Clinics
from Dao import _Vaccines
from Dto import Logistic
from Dto import Supplier
from Dto import Clinic
from Dto import Vaccine
from datetime import datetime
import sqlite3
import atexit


class _Repository:
    def __init__(self, database_sars_cov_2_conn):
        self._conn = sqlite3.connect(database_sars_cov_2_conn)
        self.logistics = _Logistics(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.vaccines = _Vaccines(self._conn)
        self.next_vaccine_index = 1

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
                    self.next_vaccine_index = self.next_vaccine_index + 1
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

    def execute_orders(self, orders, output):
        with open(orders) as input_file:
            for line in input_file:
                text_line = line.split(",")
                if len(text_line) == 3:
                    self.receive_shipment_order(text_line, output)
                else:
                    self.send_shipment_order(text_line, output)

    def receive_shipment_order(self, order_line, output):
        name = order_line[0]
        amount = int(order_line[1])
        date = datetime.strftime(order_line[2], '%Y-%m-%d')
        supplier = self.suppliers.find_by_name(name)
        vaccine_to_insert = Vaccine(self.next_vaccine_index, date, supplier.id, amount)
        self.vaccines.insert(vaccine_to_insert)
        logistic = self.logistics.find(supplier.logistic)
        new_count_received = logistic.count_received + amount
        self.logistics.update_count_received(new_count_received, logistic.id)

    def send_shipment_order(self, order_line, output):
        location = order_line[0]
        amount = int(order_line[1])
        clinic = self.clinics.find_by_location(location)
        new_demand = clinic.demand - amount
        self.clinics.update_demand(new_demand, clinic.id)
        logistic = self.logistics.find(clinic.logistic)
        new_count_sent = logistic.count_sent + amount
        self.logistics.update_count_sent(new_count_sent, logistic.id)
