import time
from random import randint

import requests
from flask import Flask, jsonify, request
from models import Base, Coffee, User
from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import Session

app = Flask(__name__)
engine = create_engine(
    "postgresql+psycopg2://postgres:postgres@postgress:5432/postgres", echo=True
)


NAME_URL = "https://random-data-api.com/api/v2/users?size=10?response_type=json"
ADDRESS_URL = (
    "https://random-data-api.com/api/address/random_address?size=10?response_type=json"
)
COFFEE_URL = (
    "https://random-data-api.com/api/coffee/random_coffee?size=10?response_type=json"
)


def get_random_data():
    sess = requests.Session()
    names = sess.get(NAME_URL).json()
    time.sleep(2)
    address = sess.get(ADDRESS_URL).json()
    time.sleep(2)
    coffee = sess.get(COFFEE_URL).json()
    time.sleep(2)
    coffee_list = [
        Coffee(
            title=c["blend_name"],
            origin=c["origin"],
            intensifier=c["intensifier"],
            notes=c["notes"].split(", "),
        )
        for c in coffee
    ]
    users_list = []
    for num, u in enumerate(names):
        users_list.append(
            User(
                name=u["first_name"],
                has_sale=randint(0, 1),
                address=address[num],
                coffee_id=randint(1, 10),
            )
        )
    return coffee_list, users_list


@app.route("/")
def generate_data():
    with Session(engine) as session_db:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        coffee_list, users_list = get_random_data()
        session_db.add_all(coffee_list)
        session_db.add_all(users_list)
        session_db.commit()
    return "Random data is write to database", 200


@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    user = User(
        name=data["name"],
        address=data["address"],
        coffee_id=int(data["coffee_id"]),
        has_sale=int(data["has_sale"]),
    )
    with Session(engine) as session_db:
        session_db.add(user)
        session_db.commit()
        session_db.close()
        print("User added successfully")
    return jsonify({"message": "User added successfully"}), 201


@app.route("/search_coffee", methods=["GET"])
def coffee_by_name():
    data = request.json
    coffee_name = data["search"]
    print(coffee_name)
    with Session(engine) as session_db:
        coffees = (
            session_db.query(Coffee)
            .filter(Coffee.title.ilike(f"%{coffee_name}%"))
            .all()
        )
        session_db.close()
    return jsonify([coffee.to_json() for coffee in coffees]), 200


@app.route("/unique_notes")
def unique_notes():
    with Session(engine) as session_db:
        unique_notes = (
            session_db.query(func.unnest(Coffee.notes).label("note")).distinct().all()
        )
        session_db.close()
    data = dict()
    data["notes"] = [note.note for note in unique_notes]
    data["quantity_notes"] = len(unique_notes)
    return jsonify(data), 200


@app.route("/users_by_country", methods=["GET"])
def users_by_country():
    data = request.json
    country = data["country"]
    with Session(engine) as session_db:
        users = (
            session_db.query(User)
            .filter(text("address ->> 'country' = :country"))
            .params(country=country)
            .all()
        )
        session_db.close()
    return jsonify([user.to_json() for user in users]), 200
