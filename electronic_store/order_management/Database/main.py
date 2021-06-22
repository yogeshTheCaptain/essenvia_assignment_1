from data_table import *
from modify_db import db_session

with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:
    x = db.query(OrderTable).all()  #.filter(WarehouseInventory.category == "")

    # print(type(x))
    # print(x)
    # for i in x:
    #     print(getattr(i,OrderTable.order_time.name))
