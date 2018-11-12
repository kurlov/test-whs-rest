from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.orm import relationship

from app import db


class SKU(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True,index=True)
    storages = relationship("Storage", back_populates="sku")
    order_lines = relationship("OrderLine", back_populates="sku")


class Storage(db.Model):
    id = Column(Integer, primary_key=True)
    stock = Column(Integer)
    sku_id = Column(Integer, ForeignKey('SKU.id'))
    sku = relationship('SKU', backref='storage', lazy=True)


class Order(db.Model):
    id = Column(Integer, primary_key=True)
    customer = Column(String(255), index=True)
    normalized = Column(String(255), index=True)

    @staticmethod
    def search(customer):
        """
        Method for searching orders by customer name

        First, try to search by input string, if nothing found, then
        Search for normalized version customer names

        :param customer: str
        :return: Order
        """
        pattern = "%{}%".format(customer)
        order = Order.query.filter(Order.customer.ilike(pattern)).first()
        if not order:
            order = Order.query.filter(Order.normalized.ilike(pattern)).first()
        return order


class OrderLine(db.Model):
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    sku_id = Column(Integer, ForeignKey('SKU.id'))
    sku = relationship('SKU', backref='order_line', lazy=True)
