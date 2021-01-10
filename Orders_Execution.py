from Repository import repo
from Dto import Vaccine


class _OrderExecution:
    def __init__(self, orders, output):
        open(output, 'w').close()
        self._orders = orders
        self._output = output
        self._logistics = repo.return_logistics()
        self._suppliers = repo.return_suppliers()
        self._clinics = repo.return_clinics()
        self._vaccines = repo.return_vaccines()
        self._next_vaccine_index = repo.return_next_vaccine_index()

    def execute_orders(self):
        with open(self._orders, 'r') as input_file:
            for line in input_file:
                text_line = line.split(",")
                if len(text_line) == 3:
                    self.receive_shipment_order(text_line)
                else:
                    self.send_shipment_order(text_line)

    def receive_shipment_order(self, order_line):
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
        self.print_to_output()

    def send_shipment_order(self, order_line):
        location = order_line[0]
        amount = int(order_line[1])
        clinic = self._clinics.find_by_location(location)
        new_demand = clinic.demand - amount
        self._clinics.update_demand(clinic.demand, new_demand, clinic.id)
        logistic = self._logistics.find(clinic.logistic)
        new_count_sent = logistic.count_sent + amount
        self._logistics.update_count_sent(logistic.count_sent, new_count_sent, logistic.id)
        while amount > 0:
            next_vaccine = self._vaccines.find_next_vaccine()
            if amount >= next_vaccine.quantity:
                self._vaccines.delete(next_vaccine.id, next_vaccine.quantity)
            else:
                new_quantity = next_vaccine.quantity - amount
                self._vaccines.update_quantity(next_vaccine.id, next_vaccine.quantity, new_quantity)
            amount = amount - next_vaccine.quantity
        self.print_to_output()

    def print_to_output(self):
        with open(self._output, 'a') as output_file:
            output_file.write(str(self._vaccines.total_inventory) + ",")
            output_file.write(str(self._clinics.total_demand) + ",")
            output_file.write(str(self._logistics.total_received) + ",")
            output_file.write(str(self._logistics.total_sent) + "\n")
