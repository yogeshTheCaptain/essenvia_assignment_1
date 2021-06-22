from datetime import datetime

from sqlalchemy import Column, Integer, String, VARCHAR, FLOAT, ForeignKey, TIMESTAMP
from sqlalchemy import create_engine, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WarehouseInventory(Base):
    __tablename__ = "warehouse_inventory"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(VARCHAR, nullable=False)
    model_number = Column(VARCHAR, nullable=False)
    price = Column(FLOAT, nullable=False)
    available = Column(Integer, nullable=False)

class OrderDetails(Base):
    __tablename__ = "order_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_no = Column(String, nullable=False)
    customer_name = Column(VARCHAR, nullable=False)
    customer_address = Column(VARCHAR, nullable=False)
    distance = Column(FLOAT, nullable=False)
    delivery_team = Column(String)
    order_time = Column(TIMESTAMP, default=datetime.now
                        , nullable=False)
    estimated_time = Column(TIMESTAMP)
    status = Column(String, nullable=False)

class ItemTable(Base):
    __tablename__ = "item_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("order_details.id"))
    item_model_number = Column(VARCHAR, nullable=False)
    item_quantity = Column(Integer, nullable=False)
    item_price = Column(FLOAT, nullable=False)
    item_status = Column(String, nullable=False)

class TeamTable(Base):
    __tablename__ = "team_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    team = Column(String)
    estimated_time = Column(TIMESTAMP)

engine = create_engine('postgresql://postgres:123@localhost:5432/postgres')
Base.metadata.create_all(engine)
