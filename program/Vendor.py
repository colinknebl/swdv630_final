from sqlalchemy import Table, ForeignKey, Column, Integer, String, Float, orm, Boolean
from DB import DB
from datetime import date
from Inventory import InventoryItem

class Item(DB.Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Float)
    color = Column(String)

    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    vendor = orm.relationship('Vendor', back_populates='items')

    inventory_items = orm.relationship('InventoryItem', order_by=InventoryItem.id, back_populates='item')

    def __init__(self, name, price, color):
        self.name = name
        self.price = price
        self.color = color

    def __repr__(self):
        return 'Item<%r, %r, %r>' % (self.name, self.price, self.color)

    def set_price(self, new_price):
        self.price = new_price

    def set_color(self, new_color):
        self.color = new_color

    def set_name(self, new_name):
        self.name = new_name


class Order(DB.Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    requested_deliver_date = Column(String)
    is_active = Column(Boolean)

    item_id = Column(Integer)
    quantity = Column(Integer)

    vendor_id = Column(Integer, ForeignKey('vendors.id'))
    vendor = orm.relationship('Vendor', back_populates='orders')

    def __get_item(self):
        return self.vendor.get_item(self.item_id)

    item = property(__get_item, None, None)

    def __calc_price(self):
        return self.quantity * self.item.price

    price = property(__calc_price)

    def __init__(self, date_obj, order_details):
        self.requested_deliver_date = date(
            date_obj['year'],
            date_obj['month'],
            date_obj['day']
        )
        self.is_active = True
        self.item_id = order_details[0]
        self.quantity = order_details[1]


    def __repr__(self):
        return 'Order<%r, %r, %r, %r>' % (self.requested_deliver_date, self.item, self.quantity, self.is_active)

    def set_quantity(self, new_quantity):
        self.quantity = new_quantity

    def cancel(self):
        self.is_active = False
        db = DB()
        db.delete(self)
        db.commit()


class Vendor(DB.Base):
    __tablename__ = 'vendors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)

    items = orm.relationship('Item', order_by=Item.id, back_populates='vendor')
    orders = orm.relationship('Order', order_by=Order.id, back_populates='vendor')
    inventory_items = orm.relationship('InventoryItem', order_by=InventoryItem.id, back_populates='vendor')

    def __init__(self, name, address, items=[]):
        self.name = name
        self.address = address
        self.items = items

    def __repr__(self):
        return 'Vendor<%r>' % (self.name)

    def add_item(self, item):
        self.items.append(item)

    def print_items(self):
        """Prints all items"""

        # print heading
        print('{0:20} | {1:>20} | {2:>20} | {3:>20}'.format('Item ID', 'Item Name', 'Item Price', 'Item Color'))

        # print each item
        for item in self.items:
            print('{0:<20} | {1:>20} | {2:>20} | {3:>20}'.format(item.id, item.name, item.price, item.color))

    def update_name(self, new_name):
        self.name = new_name

    def get_item(self, item_id):
        target = None
        for item in self.items:
            if item.id == item_id:
                target = item
                break
        return target

    def create_order(self, year=None, month=None, day=None, item=None):
        order = Order({
            "year": year,
            "month": month,
            "day": day
        }, item)
        self.orders.append(order)
    
    def get_active_orders(self):
        active_orders = []
        for order in self.orders:
            if order.is_active:
                active_orders.append(order)
        return active_orders

