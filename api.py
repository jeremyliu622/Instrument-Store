"""
ACIT 2515 Object Oriented Programming - Assignment 4
April 10, 2020
Jeffrey Law A00864331 Set 2A
Jeremy Liu A01070289 Set 2A
    This is a class representing a RESTful API.
"""
from flask import Flask, jsonify, request, make_response
from models.instrument_store import InstrumentStore




app = Flask(__name__)

store = InstrumentStore("Tim's Musical Emporium")


@app.route("/validate", methods=["GET", "POST", "PUT", "DELETE"])
def validate_setup():
    return jsonify(
        {
            "method": request.method,
            "Content-Type header": request.headers.get("Content-Type"),
            "data": request.data.decode(),
        }
    )


@app.route("/store/instrument", methods=["POST"])
def add_instrument():
    """ Manage the POST request for adding a new instrument """
    data = request.json
    try:
        store.add(data)
        return make_response("Instrument was successfully added", 200)
    except ValueError as e:
        message = str(e)
        return make_response(message, 400)
    except KeyError as e:
        message = str(e) + ' key is missing from the Instrument JSON request.'
        return make_response(message, 400)


@app.route("/store/instrument/<string:_type>/<int:_id>", methods=["PUT"])
def update_instrument(_id, _type):
    """ Manage the PUT request for updating an instrument object in the InstrumentStore"""
    data = request.json
    print(data)
    try:
        store.update_instrument_state(_type, _id, data)
        return make_response("Instrument was successfully updated", 200)
    except ValueError as e:
        message = str(e)
        return make_response(message, 404)
    except KeyError as e:
        message = str(e) + ' key is missing from the Instrument JSON request.'
        return make_response(message, 400)


@app.route("/store/instrument/<string:_type>/<int:_id>", methods=["DELETE"])
def delete_instrument(_id, _type):
    """ Manage the DELETE request for deleting an instrument object from the InstrumentStore """
    try:
        store.remove_instrument_by_id(_id, _type)
        return make_response("Instrument has been deleted.", 200)
    except ValueError as e:
        message = str(e)
        return make_response(message, 404)


@app.route("/store/instrument/<string:_type>/<int:_id>", methods=["GET"])
def get_instrument(_id, _type):
    """ Get the instrument object given an ID """
    try:
        print(jsonify(store.get(_id, _type)))
        return jsonify(store.get(_id, _type))
    except ValueError as e:
        message = str(e)
        return make_response(message, 404)


@app.route("/store/instrument/all", methods=["GET"])
def list_all_instruments():
    """ Return as a response, a list of all instruments in JSON format """
    instrument_list = []
    for instrument in store.get_all():
        instrument['manufacture_date'] = str(instrument['manufacture_date'])
        instrument['price'] = float(instrument['price'])
        instrument_list.append(instrument)
    return jsonify(instrument_list)


@app.route("/store/instrument/all/<string:instruments_type>", methods=["GET"])
def list_by_type(instruments_type):
    """ Return as a response, a list of a given type in JSON format """
    instruments_list = []
    try:
        for instrument in store.get_all_by_type(instruments_type):
            instrument['manufacture_date'] = str(instrument['manufacture_date'])
            instrument['price'] = float(instrument['price'])
            instruments_list.append(instrument)
        return jsonify(instruments_list)
    except ValueError as e:
        message = str(e)
        return make_response(message, 400)


@app.route("/store/instrument/stats", methods=["GET"])
def get_store_stats():
    return jsonify(store.get_stats())


if __name__ == '__main__':
    app.run()
