from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)

# --------------- Modelos para la base de datos ---------------------


class TemperatureModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float(3, 1), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Temperature: {self.value} -> {self.date}"


class GasModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float(3, 1), nullable=False)
    date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Methane: {self.value} -> {self.date}"

# --------------- ------------------------------ ---------------------


db.create_all()


temp_put_args = reqparse.RequestParser()
temp_put_args.add_argument("value", type=float, help="Temperature value is required", required=True)

resource_fields = {
    "id": fields.Integer,
    "value": fields.Float,
    "date": fields.DateTime
}


class Temperature(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = TemperatureModel.query.all()

        if not result:
            abort(404, message="Could not find any data")

        return result[-1], 200

    @marshal_with(resource_fields)
    def put(self):
        args = temp_put_args.parse_args()

        temp = TemperatureModel(value=args['value'], date=datetime.datetime.now())
        db.session.add(temp)
        db.session.commit()

        return temp, 200


gas_put_args = reqparse.RequestParser()
gas_put_args.add_argument("value", type=float, help="Temperature value is required", required=True)
gas_put_args.add_argument("date", type=str, help="Date is required", required=True)


class Methane(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result = GasModel.query.all()

        if not result:
            abort(404, message="Could not find any data")

        return result[-1], 200

    @marshal_with(resource_fields)
    def put(self):
        args = gas_put_args.parse_args()

        gas = GasModel(value=args['value'], date=datetime.datetime.now())
        db.session.add(gas)
        db.session.commit()

        return gas, 200


api.add_resource(Temperature, "/temperature")
api.add_resource(Methane, "/methane")


if __name__ == '__main__':
    app.run(debug=True)
