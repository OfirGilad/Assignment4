from Dto import Vaccine
from Dto import Supplier
from Dto import Clinic
from Dto import Logistic


class _Vaccines:
    def __init__(self, conn):
        self._conn = conn
        self._total_inventory = 0

    def insert(self, vaccine):
        self._total_inventory = self._total_inventory + int(vaccine.quantity)
        
        self._conn.execute("""
            INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
            """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, date, supplier, quantity FROM vaccines WHERE id = ?
            """, [vaccine_id])

        return Vaccine(*c.fetchone())

    def update_quantity(self, vaccine_quantity_old_value, vaccine_quantity_new_value, vaccine_id):
        quantity_to_add = vaccine_quantity_new_value - vaccine_quantity_old_value
        self._total_inventory = self._total_inventory + quantity_to_add

        c = self._conn.cursor()
        c.execute("""
            UPDATE vaccines SET quantity = (?) WHERE id = (?)
            """, [vaccine_quantity_new_value, vaccine_id])

    def find_by_supplier_id(self, vaccine_supplier):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, date, supplier, quantity FROM vaccines WHERE supplier = ?
            """, [vaccine_supplier])

        return Vaccine(*c.fetchone())
    
    def delete(self, vaccine_id, vaccine_quantity):
        self._total_inventory = self._total_inventory - vaccine_quantity
        
        self._conn.execute("""
                    DELETE FROM vaccines WHERE id = (?)
                    """, [vaccine_id])

    @property
    def total_inventory(self):
        return self._total_inventory


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
            INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
            """, [supplier.id, supplier.name, supplier.logistic])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, logistic FROM suppliers WHERE id = ?
            """, [supplier_id])

        return Supplier(*c.fetchone())

    def find_by_name(self, supplier_name):
        c = self._conn.cursor()
        c.execute("""
                    SELECT id, name, logistic FROM suppliers WHERE name = ?
                    """, [supplier_name])

        return Supplier(*c.fetchone())

    def find_by_logistic(self, supplier_logistic):
        c = self._conn.cursor()
        c.execute("""
                    SELECT id, name, logistic FROM suppliers WHERE logistic = ?
                    """, [supplier_logistic])

        return Supplier(*c.fetchone())


class _Clinics:
    def __init__(self, conn):
        self._conn = conn
        self._total_demand = 0

    def insert(self, clinic):
        self._total_demand = self._total_demand + int(clinic.demand)

        self._conn.execute("""
            INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
            """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find(self, clinic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, location, demand, logistic FROM clinics WHERE id = ?
            """, [clinic_id])

        return Clinic(*c.fetchone())

    def find_by_location(self, clinic_location):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, location, demand, logistic FROM clinics WHERE location = ? 
            """, [clinic_location])

        return Clinic(*c.fetchone())

    def update_demand(self, clinic_demand_old_value, clinic_demand_new_value, clinic_id):
        demand_to_add = clinic_demand_new_value - clinic_demand_old_value
        self._total_demand = self._total_demand + demand_to_add

        c = self._conn.cursor()
        c.execute("""
            UPDATE clinics SET demand = (?) WHERE id = (?)
            """, [clinic_demand_new_value, clinic_id])

    @property
    def total_demand(self):
        return self._total_demand


class _Logistics:
    def __init__(self, conn):
        self._conn = conn
        self._total_sent = 0
        self._total_received = 0

    def insert(self, logistic):
        self._total_sent = self._total_sent + int(logistic.count_sent)
        self._total_received = self._total_received + int(logistic.count_received)

        self._conn.execute("""
            INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
            """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, count_sent, count_received FROM logistics WHERE id = ?
            """, [logistic_id])

        return Logistic(*c.fetchone())

    def update_count_sent(self, logistic_count_sent_old_value, logistic_count_sent_new_value, logistic_id):
        count_to_add = logistic_count_sent_new_value - logistic_count_sent_old_value
        self._total_sent = self._total_sent + count_to_add

        c = self._conn.cursor()
        c.execute("""
            UPDATE logistics SET count_sent = (?) WHERE id = (?)
            """, [logistic_count_sent_new_value, logistic_id])

    def update_count_received(self, logistic_count_received_old_value, logistic_count_received_new_value, logistic_id):
        count_to_add = logistic_count_received_new_value - logistic_count_received_old_value
        self._total_received = self._total_received + count_to_add

        c = self._conn.cursor()
        c.execute("""
            UPDATE logistics SET count_received = (?) WHERE id = (?)
            """, [logistic_count_received_new_value, logistic_id])

    @property
    def total_sent(self):
        return self._total_sent

    @property
    def total_received(self):
        return self._total_received
