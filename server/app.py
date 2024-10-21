#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Define the Plants resource (GET all plants, POST create a new plant)
class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

    def post(self):
        if not request.json or not all(k in request.json for k in ('name', 'image', 'price')):
            return make_response(jsonify({"error": "Missing required fields"}), 400)

        new_plant = Plant(
            name=request.json['name'],
            image=request.json['image'],
            price=request.json['price']
        )
        db.session.add(new_plant)
        db.session.commit()

        return jsonify(new_plant.to_dict()), 201

# Define the PlantByID resource (GET a plant by its ID)
class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if plant is None:
            return make_response(jsonify({"error": "Plant not found"}), 404)
        return jsonify(plant.to_dict())

# Add resource routing
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
