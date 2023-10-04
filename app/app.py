#!/usr/bin/env python3
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound

from models import db,Hero,Power,Hero_powers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)
# create a response for landing page

class Home(Resource):
    def get(self):
        response_message = {
            "message": "WELCOME TO THE SUPER HEROES API."
        }
        return make_response(response_message, 200)


api.add_resource(Home, '/')

class Heroes(Resource):
    def get(self):
        heroes = []
        for hero  in Hero.query.all():
            hero_dict={
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
            }
            heroes.append(hero_dict)
        return make_response(jsonify(heroes), 200)
api.add_resource(Heroes, '/heroes')

