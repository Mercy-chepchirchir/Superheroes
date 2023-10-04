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

class HeroByID(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            hero_dict={
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers":[
                    {
                        "id": hero_power.power.id,
                        "name": hero_power.power.name,
                        "description": hero_power.power.description,
                    }
                    for hero_power in hero.powers
                ]
            }
            return make_response(jsonify(hero_dict), 200)
        else:
            return make_response(jsonify({"error": "Hero not found"}), 404)

api.add_resource(HeroByID, '/heroes/<int:id>')

class HeroByID(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            hero_dict={
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers":[
                    {
                        "id": hero_power.power.id,
                        "name": hero_power.power.name,
                        "description": hero_power.power.description,
                    }
                    for hero_power in hero.powers
                ]
            }
            return make_response(jsonify(hero_dict), 200)
        else:
            return make_response(jsonify({"error": "Hero not found"}), 404)

api.add_resource(HeroByID, '/heroes/<int:id>')

class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        power_list = []
        for power in powers:
            power_dict = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            power_list.append(power_dict)
        return make_response(jsonify(power_list), 200)

api.add_resource(Powers, '/powers')

class HeroByID(Resource):
    def get(self, id):
        hero = Hero.query.filter_by(id=id).first()
        if hero:
            hero_dict={
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers":[
                    {
                        "id": hero_power.power.id,
                        "name": hero_power.power.name,
                        "description": hero_power.power.description,
                    }
                    for hero_power in hero.powers
                ]
            }
            return make_response(jsonify(hero_dict), 200)
        else:
            return make_response(jsonify({"error": "Hero not found"}), 404)

api.add_resource(HeroByID, '/heroes/<int:id>')

class Powers(Resource):
    def get(self):
        powers = Power.query.all()
        power_list = []
        for power in powers:
            power_dict = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            power_list.append(power_dict)
        return make_response(jsonify(power_list), 200)

api.add_resource(Powers, '/powers')

class PowerByID(Resource):
    def get(self, id):
        power = Power.query.filter_by(id=id).first()
        if power:
            power_dict={
                "id": power.id,
                "name": power.name,
                "description": power.description,
                
            }
            return make_response(jsonify(power_dict), 200)
        else:
            return make_response(jsonify({"error": "Power not found"}), 404)
        
    def patch(self,id):
        power = Power.query.filter_by(id=id).first()
        data = request.get_json()
        if power:
            for attr in data:
                   setattr(power, attr, data[attr])
            
            db.session.add(power)
            db.session.commit()
            power_dict={
                "id": power.id,
                "name": power.name,
                "description": power.description,
                
            }
            return make_response(power_dict, 200)
        else:
            return make_response(jsonify({"error": "Power not found"}), 404)

api.add_resource(PowerByID, '/powers/<int:id>')
class Hero_Powers(Resource):
    def post(self):
        data = request.get_json()

       # Validate that the required fields(strength,power_id and hero_id) are present in the request
        required_fields = ["strength", "power_id", "hero_id"]
        if not all(key in data for key in required_fields):
            return make_response(jsonify({"errors": ["Validation errors"]}), 400)

        