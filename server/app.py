# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route("/earthquakes/<int:id>")
def getEarthquake(id):
    res = Earthquake.query.filter_by(id=id).first()
    if res:
        return make_response(jsonify(res.to_dict()), 200)
    return make_response({'message':f'Earthquake {id} not found.'}, 404)

@app.route("/earthquakes/magnitude/<float:magnitude>")
def getEarthQueakeByMagnitude(magnitude):
    res = Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()
    r = {
        'count':len(res),
        'quakes': [q.to_dict() for q in res]
    }
    return make_response(jsonify(r), 200)
if __name__ == '__main__':
    app.run(port=5556, debug=True)
