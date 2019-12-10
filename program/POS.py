from DB import DB
from TimeClock import TimeClock
from Vendors import Vendors
from Employees import Employees
from Employee import Employee
from Orders import Orders
from Inventory import Inventory, InventoryItem
from Vendor import Item, Vendor
from Register import Register
from Account import Account
from driver \
    import run_uc1, run_uc2, run_uc3, \
           run_uc4, run_uc5, run_uc6, \
           run_uc7, run_uc8, run_uc9, \
           run_uc10, run_uc11, run_uc12


class POS:

    def __init__(self):
        self.db = DB()
        self.__employees = Employees(self)
        self.__vendors = Vendors(self)
        self.__time_clock = TimeClock(self)
        self.__orders = Orders(self)
        self.__inventory = Inventory(self)
        self.__register = Register(self)
        self.account = Account()

    def open_time_clock(self, print_employees=True):
        if print_employees:
            self.__employees.print_all()
        return self.__time_clock

    def open_employees(self):
        return self.__employees

    def open_vendors(self):
        return self.__vendors

    def open_orders(self):
        return self.__orders

    def open_inventory(self):
        return self.__inventory

    def open_register(self):
        return self.__register

    @staticmethod
    def get_cls(requested_cls):
        if requested_cls == 'Item':
            return Item
        elif requested_cls == 'Vendor':
            return Vendor
        elif requested_cls == 'InventoryItem':
            return InventoryItem


def create_new_employee(pos):
    name = input('Congratulations! You\'ve been hired. What is your name? ')
    # name = 'Colin Knebl'
    if name:
        emp = Employee(name)
        pos.open_employees().add(emp)

if __name__ == '__main__':
    pos = POS()

    create_new_employee(pos)
    
    # clock in some of the other employees
    tc = pos.open_time_clock(print_employees=False)
    tc.clock_in(1, confirm=False)
    tc.clock_in(3, confirm=False)
    tc.clock_in(4, confirm=False)

    
    run_uc1(pos)
    run_uc2(pos)
    run_uc3(pos)
    run_uc4(pos)
    run_uc5(pos)
    run_uc6(pos)
    run_uc7(pos)
    run_uc8(pos)
    run_uc9(pos)
    run_uc10(pos)
    run_uc11(pos)
    run_uc12(pos)