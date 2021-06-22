# team_selected , eta = fetch_delivery_time_team()

from sqlalchemy import func, true, false
from .Database.data_table import *
from .Database.modify_db import db_session
import random
import datetime


def fetch_price_of_order_id(order_id):
    with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:
        x = db.query(ItemTable).filter(
            ItemTable.id == order_id).all()
        total_price = 0
        for data in x:
            if getattr(data, ItemTable.item_status.name) == "true":
                total_price += getattr(data, ItemTable.item_price.name) * getattr(data, ItemTable.item_quantity.name)

    return total_price


def fetch_delivery_time_team(order_time, distance):
    with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:
        records = db.query(OrderDetails.delivery_team).filter(OrderDetails.delivery_team != None).all()

    if not records:
        team_selected = random.choice(["A", "B"])

        if distance < 5:
            eta = order_time + datetime.timedelta(minutes=40)
        else:
            eta = order_time + datetime.timedelta(minutes=60)

    elif len(records) == 1:
        if records[0][0] == "A":
            team_selected = "B"
        else:
            team_selected = "A"

        if distance < 5:
            eta = order_time + datetime.timedelta(minutes=40)
        else:
            eta = order_time + datetime.timedelta(minutes=60)

    else:

        with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:
            time_a_records = db.query(TeamTable.estimated_time).filter(TeamTable.team == "A").first()
            time_b_records = db.query(TeamTable.estimated_time).filter(TeamTable.team == "B").first()

            team_a_time = getattr(time_a_records, TeamTable.estimated_time.name)
            team_b_time = getattr(time_b_records, TeamTable.estimated_time.name)

            if team_a_time < datetime.datetime.now() and team_b_time < datetime.datetime.now():

                if team_a_time < team_b_time:
                    team_selected = "A"
                else:
                    team_selected = "B"

                if distance < 5:
                    eta = order_time + datetime.timedelta(minutes=40)
                else:
                    eta = order_time + datetime.timedelta(minutes=60)

            elif team_a_time > datetime.datetime.now() and team_b_time > datetime.datetime.now():

                if team_a_time < team_b_time:
                    team_selected = "A"

                    if distance < 5:
                        eta = team_a_time + datetime.timedelta(minutes=40)
                    else:
                        eta = team_a_time + datetime.timedelta(minutes=60)

                else:
                    team_selected = "B"

                    if distance < 5:
                        eta = team_b_time + datetime.timedelta(minutes=40)
                    else:
                        eta = team_b_time + datetime.timedelta(minutes=60)

            else:

                if team_a_time < datetime.datetime.now():
                    team_selected = "A"
                elif team_b_time < datetime.datetime.now():
                    team_selected = "B"

                if distance < 5:
                    eta = order_time + datetime.timedelta(minutes=40)
                else:
                    eta = order_time + datetime.timedelta(minutes=60)

    if distance < 5:
        total_eta = eta + datetime.timedelta(minutes=20)
    else:
        total_eta = eta + datetime.timedelta(minutes=40)

    with db_session("postgresql://postgres:123@localhost:5432/postgres") as db:

        db.query(TeamTable).filter(TeamTable.team == team_selected).update(
            {
                TeamTable.estimated_time.name: total_eta
            }
        )

        db.commit()

    return team_selected, eta
