from Vendor import Item

def run_uc1(pos):
    print('\n*** UC1: Clock In ***')
    tc = pos.open_time_clock()
    emp_id = input('Enter your Employee ID to clock in: ')
    if emp_id:
        tc.clock_in(int(emp_id))

def run_uc2(pos):
    print('\n*** UC2: Clock Out ***')
    tc = pos.open_time_clock()
    emp_id = input('Enter your Employee ID to clock out: ')
    if emp_id:
        tc.clock_out(int(emp_id))

def run_uc3(pos):
    print('\n*** UC3: Add Vendor ***')
    vendors = pos.open_vendors()
    vendors.add()

def run_uc4(pos):
    print('\n*** UC4: Update Vendor ***')
    vendors = pos.open_vendors()
    vendors.update()

def run_uc5(pos):
    print('\n*** UC5: Remove Vendor ***')
    vendors = pos.open_vendors()
    vendors.remove()

def run_uc6(pos):
    print('\n*** UC6: Create Order ***')
    orders = pos.open_orders()
    orders.new()

def run_uc7(pos):
    print('\n*** UC7: Update Order ***')
    orders = pos.open_orders()
    orders.update()

def run_uc8(pos):
    print('\n*** UC8: Cancel Order ***')
    orders = pos.open_orders()
    orders.cancel()

def run_uc9(pos):
    print('\n*** UC9: Add to Inventory ***')
    inventory = pos.open_inventory()
    inventory.add()

def run_uc10(pos):
    print('\n*** UC10: Update Inventory ***')
    inventory = pos.open_inventory()
    inventory.update()

def run_uc11(pos):
    print('\n*** UC11: Purchase Item ***')
    register = pos.open_register()
    register.checkout()

def run_uc12(pos):
    print('\n*** UC12: Return Item ***')
    register = pos.open_register()
    register.return_item()