#!flask/bin/python
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request, render_template
import pickle
import numpy as np
import json
app = Flask(__name__)

model = pickle.load(open("car.pkl", "rb"))

with open('data.json', 'r') as openfile:
    api = json.load(openfile)

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api/tasks', methods=['POST'])
def predict():
    features = [int(x) for x in request.form.values()]
    final_features = [np.array(features)]
    prediction = model.predict(final_features)
    output = int(prediction[0])
    

    data = {
        'id': api[-1]['id'] + 1,
        'year': request.form.get("year"),
        'km_driven': request.form.get("km_driven"),
        'fuel': request.form.get("fuel"),
        'transmission': request.form.get("transmission"),
        'mileage': request.form.get("mileage"),
        'engine': request.form.get("engine"),
        'max_power': request.form.get("max_power"),
        'seats': request.form.get("seats"),
        'predict': output
    }
    print("data")
    api.append(data)
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(api, f, indent=4)
    return jsonify({'predict': output})
@app.route('/api/<int:data_id>', methods=['GET'])
def get_data(data_id):
    task = [data for data in api if data['id'] == data_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'data': api[data_id]})

@app.route('/api/all', methods=['GET'])
def all():
    return jsonify({'api': api})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run()