# Create your views here.
from datetime import datetime, date

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from sqlalchemy import func, true, false

from .Database.data_table import *
from .Database.modify_db import db_session

from .helper import fetch_delivery_time_team, fetch_price_of_order_id


class InventoryViewSet(viewsets.ViewSet):

    @action(methods=['get'], detail=False, url_path='inventory')
    def get_inventory_details(self, request):

        with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:
            x = db.query(WarehouseInventory).filter(
                WarehouseInventory.available != 0).all()

            data_to_return = [
                {
                    "category": getattr(data, WarehouseInventory.category.name),
                    "model_number": getattr(data, WarehouseInventory.model_number.name),
                    "available": getattr(data, WarehouseInventory.available.name),
                    "price": getattr(data, WarehouseInventory.price.name)

                }
                for data in x
            ]

        return Response(
            # template_name=template_name,
            data={"data": data_to_return},
            status=status.HTTP_200_OK,

        )

    @action(methods=['get'], detail=False, url_path='orders')
    def get_order_details(self, request):

        with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:
            x = db.query(OrderDetails).filter(
                func.date(OrderDetails.order_time) == date.today()).all()

        if len(x) == 0:
            return Response(
                # template_name=template_name,
                data={"status": 'There was no order for today'},
                status=status.HTTP_200_OK,

            )

        else:
            data_to_return = [
                {
                    "id": getattr(data1, OrderDetails.id.name),
                    "order no": getattr(data1, OrderDetails.order_no.name),
                    "estimated time": getattr(data1, OrderDetails.estimated_time.name),
                    "Order Status": getattr(data1, OrderDetails.status.name ),
                    'Total Price': fetch_price_of_order_id(getattr(data1, OrderDetails.id.name)),

                }
                for data1 in x
            ]

            return Response(
                # template_name=template_name,
                data={"data": data_to_return},
                status=status.HTTP_200_OK,

            )

    @action(methods=['post', 'get'], detail=False, url_path='placeOrder')
    def place_order(self, request):

        with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:

            records = db.query(OrderDetails.id).all()
            if records:

                last_date = getattr(db.query(OrderDetails.order_time).order_by(OrderDetails.id.desc()).first(),
                                    OrderDetails.order_time.name)

                if str(last_date)[:10] == str(datetime.now())[:10]:
                    previous_order_id = getattr(
                        db.query(OrderDetails.order_no).order_by(OrderDetails.id.desc()).first(),
                        OrderDetails.order_no.name)

                    order_number = str(datetime.now().date()).replace("-", "") + "_" + str(
                        int(previous_order_id.split("_")[-1]) + 1)

                else:
                    order_number = str(datetime.now().date()).replace("-", "") + "_1"

            else:
                last_id = 0
                order_number = str(datetime.now().date()).replace("-", "") + "_" + str(last_id + 1)

            print(request.data)
            customer_name = request.data.get('customer_name')
            address = request.data.get('address')
            distance = request.data.get('distance')
            items = request.data.get('items')

        status_dict = {}

        order_status = "order not placed"

        for dictInd in items:
            with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:
                exists = db.query(WarehouseInventory.id, WarehouseInventory.available).filter(
                    WarehouseInventory.model_number == dictInd.get('item'),
                    WarehouseInventory.available >= dictInd.get('quantity')).first()

                if exists:
                    status_dict[dictInd.get('item')] = True

                    warehouse_pk = getattr(exists, WarehouseInventory.id.name)
                    warehouse_quantity = getattr(exists, WarehouseInventory.available.name)

                    db.query(WarehouseInventory).filter(WarehouseInventory.id == warehouse_pk).update(
                        {
                            WarehouseInventory.available.name: warehouse_quantity - dictInd.get('quantity')
                        }
                    )

                    db.commit()

                else:
                    status_dict[dictInd.get('item')] = False

        if any(status_dict.values()):
            order_status = "order placed"

            team_selected, eta = fetch_delivery_time_team(datetime.now(), distance)

            with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:

                order_detail_entry = OrderDetails(order_no=order_number,
                                                  customer_name=customer_name,
                                                  customer_address=address,
                                                  distance=distance,
                                                  status=true(),
                                                  delivery_team=team_selected,
                                                  estimated_time=eta)

                db.add(order_detail_entry)

                db.commit()

                item_table_foreign_key = order_detail_entry.id

            item_list = request.data.get('items')

            for item in item_list:
                with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:
                    x = db.query(WarehouseInventory).filter(
                        WarehouseInventory.model_number == item.get('item')).first()

                with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:
                    db.add(ItemTable(
                        order_id=item_table_foreign_key,
                        item_model_number=item.get('item'),
                        item_quantity=item.get('quantity'),
                        item_price=getattr(x, WarehouseInventory.price.name),
                        item_status=status_dict.get(item.get('item'))
                    ))

                    db.commit()

            return Response(

                data={"order_no": order_number, "order_status": order_status},
                status=status.HTTP_200_OK,

            )

        else:

            with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:

                order_detail_entry = OrderDetails(order_no=order_number,
                                                  customer_name=customer_name,
                                                  customer_address=address,
                                                  distance=distance,
                                                  status=false(),
                                                  estimated_time=None)

                db.add(order_detail_entry)

                db.commit()

            return Response(

                data={"status": "Items not available"},
                status=status.HTTP_200_OK,

            )
