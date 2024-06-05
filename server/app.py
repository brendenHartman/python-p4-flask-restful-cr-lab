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

class Plants(Resource):
    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(plants, 200)
    def post(self):
        new = Plant(
            name = request.get_json().get('name'),
            image = request.get_json().get('image'),
            price = request.get_json().get('price'),
        )

        db.session.add(new)
        db.session.commit()

        new = new.to_dict()

        return make_response(new,201)

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plan = Plant.query.filter_by(id=id).first().to_dict()
        print(plan)
        return make_response(plan, 200)
        
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
