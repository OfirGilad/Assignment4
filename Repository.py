from Dao import _Logistics
from Dao import _Suppliers
from Dao import _Clinics
from Dao import _Vaccines
from Dto import Logistic
from Dto import Supplier
from Dto import Clinic
from Dto import Vaccine
import sqlite3


class _Repository:
    def __init__(self, database_sars_cov_2_conn):
        self._conn = sqlite3.connect(database_sars_cov_2_conn)
        self._logistics = _Logistics(self._conn)
        self._suppliers = _Suppliers(self._conn)
        self._clinics = _Clinics(self._conn)
        self._vaccines = _Vaccines(self._conn)
        self._next_vaccine_index = 1

    def close(self):
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

    def print_all(self):
        print("vaccines")
        self.print_table(self._conn.execute("SELECT * FROM vaccines"))
        print("suppliers")
        self.print_table(self._conn.execute("SELECT * FROM suppliers"))
        print("clinics")
        self.print_table(self._conn.execute("SELECT * FROM clinics"))
        print("logistics")
        self.print_table(self._conn.execute("SELECT * FROM logistics"))

    def print_table(self, list_of_elements):
        for element in list_of_elements:
            print(element)

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
        length = len(order_line[2])
        date = order_line[2][0:length - 1]
        supplier = self._suppliers.find_by_name(name)
        vaccine_to_insert = Vaccine(self._next_vaccine_index, date, supplier.id, amount)
        self._next_vaccine_index = self._next_vaccine_index + 1
        self._vaccines.insert(vaccine_to_insert)
        logistic = self._logistics.find(supplier.logistic)
        new_count_received = logistic.count_received + amount
        self._logistics.update_count_received(logistic.count_received, new_count_received, logistic.id)
        self.print_to_output(output)

    def send_shipment_order(self, order_line, output):
        location = order_line[0]
        amount = int(order_line[1])
        clinic = self._clinics.find_by_location(location)
        new_demand = clinic.demand - amount
        self._clinics.update_demand(clinic.demand, new_demand, clinic.id)
        logistic = self._logistics.find(clinic.logistic)
        new_count_sent = logistic.count_sent + amount
        self._logistics.update_count_sent(logistic.count_sent, new_count_sent, logistic.id)
        supplier = self._suppliers.find_by_logistic(logistic.id)
        while amount > 0:
            next_vaccine = self._vaccines.find_by_supplier_id(supplier.id)
            if amount >= next_vaccine.quantity:
                self._vaccines.delete(next_vaccine.id, next_vaccine.quantity)
            else:
                new_quantity = next_vaccine.quantity - amount
                self._vaccines.update_quantity(next_vaccine.id, next_vaccine.quantity, new_quantity)
            amount = amount - next_vaccine.quantity
        self.print_to_output(output)

    def print_to_output(self, output):
        with open(output, "a") as output_file:
            output_file.write(str(self._vaccines.total_inventory) + ",")
            output_file.write(str(self._clinics.total_demand) + ",")
            output_file.write(str(self._logistics.total_received) + ",")
            output_file.write(str(self._logistics.total_sent) + "\n")
