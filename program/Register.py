from datetime import date
from Person import Person
from Inventory import InventoryItem


class Transaction:

    def __repr__(self):
        return 'Transaction<%r>' % (self.total)

    def __get_total(self):
        total = 0
        for item in self.items:
            total += item.price
        return total

    total = property(__get_total, None, None)

    def __init__(self):
        self.items = []
        self.customer = None
        self.payment_method = None

    def add_item(self, item):
        self.items.append(item)


class Register:

    def __init__(self, pos):
        self.pos = pos
    
    def checkout(self):
        transaction = Transaction()
        inventory = self.pos.open_inventory()
        inventory.print()

        InventoryItem = self.pos.get_cls('InventoryItem')

        shopping = True
        while shopping:
            item_id = input('Enter item ID to add to cart: ')
            item = self.pos.db.query(InventoryItem, 'id={}'.format(item_id))

            if item:
                transaction.add_item(item)
            shopping = input('Continue shopping? (y/n) ') == 'y'

        self.complete(transaction)

    def __update_inventory(self, transaction):
        inventory = self.pos.open_inventory()

        for item in transaction.items:
            inventory_item = self.pos.db.query(self.pos.get_cls('InventoryItem'), 'id={}'.format(item.id))
            quantity = inventory_item.quantity - 1
            inventory.update(item_id=item.id, quantity=quantity, print_inventory=False)
        
        inventory.print()

    def __get_customer_details(self, transaction):
        customer_name = input('Enter Customer name? ')
        transaction.customer = Person(customer_name)

    def __print_receipt(self, transaction):
        print('\n--------------------')
        print('Date: ', date.today())
        print('Customer: ', transaction.customer.name)

        items = []
        for item in transaction.items:
            if len(items) == 0:
                items.append([item, 1])
            else:
                for current in items:
                    if current[0].id == item.id:
                        current[1] = current[1] + 1
                    else:
                        items.append([item, 1])

        print('\nItems:')
        for item, quantity in items:
            print('{}, {} @ ${:.2f}'.format(item.name, quantity, item.price))


        print('\nTotal:   ${}'.format(transaction.total))
        print('--------------------')

    def complete(self, transaction):
        self.__update_inventory(transaction)
        self.__get_customer_details(transaction)
        self.__process_transaction(transaction)

        self.__print_receipt(transaction)

    def __process_transaction(self, transaction):
        self.pos.account.credit(transaction.total)
        transaction.customer.account.debit(transaction.total)

    def return_item(self):
        inventory = self.pos.open_inventory()
        Item = self.pos.get_cls('Item')

        inventory.print()

        return_item_id = int(input('Enter ID of item to return: '))
        item = self.pos.db.query(InventoryItem, 'id={}'.format(return_item_id))

        if item:
            return_quantity = int(input('Enter quantity to return: '))
            if return_quantity:
                item.quantity += return_quantity

    
        inventory.print()
