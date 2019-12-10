from sqlalchemy import Table, ForeignKey, Column, Integer, String, Float, orm, Boolean
from DB import DB


class InventoryItem(DB.Base):

    __tablename__ = 'inventory_items'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)

    item_id = Column(Integer, ForeignKey('items.id'))
    item = orm.relationship('Item', back_populates='inventory_items')

    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    vendor = orm.relationship('Vendor', back_populates='inventory_items')

    def __get_price(self):
        return self.item.price

    price = property(__get_price, None, None)

    def __get_name(self):
        return self.item.name
    
    name = property(__get_name, None, None)

    def __init__(self, quantity, item):
        self.quantity = quantity
        self.item = item
        self.vendor = item.vendor

    def set_quantity(self, quantity):
        if quantity == 0:
            db = DB()
            db.delete(self)
        else:
            self.quantity = quantity


class Inventory:

    def __init__(self, pos):
        self.pos = pos

    def __add_item_to_inventory(self, quantity, item):
        item = InventoryItem(quantity, item)
        self.pos.db.commit()

    def add(self):
        self.__print_all_items()

        item_id = input('Enter item ID to add to inventory: ')
        if item_id: 
            Item = self.pos.get_cls('Item')
            item = self.pos.db.query(Item, 'id={}'.format(item_id))

            quantity = int(input('Enter quantity: '))
            self.__add_item_to_inventory(quantity, item)

    def update(self, item_id=None, quantity=None, print_inventory=True):
        if print_inventory:
            self.print()

        if item_id == None:
            item_id = int(input('Enter inventory item ID to update: '))

        item = self.pos.db.query(InventoryItem, 'id={}'.format(item_id))
        if item:
            if quantity == None:
                quantity = int(input('Enter new quantity: '))
            
            item.set_quantity(quantity)
            self.pos.db.commit()


    def __print_all_items(self):
        """Prints all items"""
        items = self.pos.db.query_all(self.pos.get_cls('Item'))

        print('\nItems Carried')
        # print heading
        print('{0:20} | {1:>20} | {2:>20} | {3:>20}'.format('Item ID', 'Vendor', 'Item Name', 'Item Price'))

        # print each vendor
        for item in items:
            print('{0:<20} | {1:>20} | {2:>20} | {3:>20}'.format(item.id, item.vendor.name, item.name, item.price))

    def print(self):
        """Prints all items in inventory"""
        inventory_items = self.pos.db.query_all(InventoryItem)

        print('\nCurrent Inventory:')
        # print heading
        print('{0:20} | {1:>20} | {2:>20} | {3:>20}'.format('Inventory Item ID', 'Vendor', 'Item Name', 'Quantity'))

        # print each vendor
        for inventory_item in inventory_items:
            print('{0:<20} | {1:>20} | {2:>20} | {3:>20}'.format(inventory_item.id, inventory_item.item.vendor.name, inventory_item.item.name, inventory_item.quantity))
