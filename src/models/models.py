from sqlalchemy import ForeignKey, Column, String, Integer, CHAR, BigInteger, Float, DateTime, Boolean
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column('id', Integer, primary_key=True)
    telegram_id = Column('telegram_id', BigInteger, nullable=False)
    username = Column('username', String, nullable=False)
    
    orders = relationship("Order", backref='owner')

    
    def __init__(self, username, tg_id):
        self.username = username
        self.telegram_id = tg_id
        
    def __repr__(self):
        return f"T_ID: {self.telegram_id} ;\nName: {self.username}"
    
    
class Product(Base):
    __tablename__ = 'products'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String, nullable=False)
    description = Column('description', String, nullable=False)
    price = Column('price', Float, nullable=False)
    isSelling = Column('isSelling', Boolean, nullable=False)
    orders = relationship("Order", backref='product')

    
    def __init__(self, name, description, price, isSelling):
        self.name = name
        self.description = description
        self.price = price
        self.isSelling = isSelling
        
        
    def __repr__(self):
        return f"ID: {self.id};\nName: {self.name};\nDescription: {self.description}\nPrice: {self.price}"
    

    
class Order(Base):
    __tablename__ = 'orders'
    id = Column('id', Integer, primary_key=True)
    
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    client_id = Column( Integer, ForeignKey('users.id'),nullable=False)
    created_at = Column('created_at', DateTime, default=datetime.datetime.utcnow)

        
    def __repr__(self):
        return f"ID: {self.id}"