""" All the routes that will be required by the api will
    be defined in this script """

from flask import jsonify, request
from api import app
from api.models import Incident

RED_FLAGS = {}

@app.route('/')
def index():
    """ This route will return the message "Hello, World" """
    return "Hello, World!"


@app.route('/api/v1/red-flags')
def get_all_redflags():
    """ This will return all available red-flags """
    red_flags_as_dicts = [dict(redflag) for redflag in RED_FLAGS.values()]

    # check if the list is empty
    if not red_flags_as_dicts:
        return jsonify({
            'error': 'There are no redflags',
            'status': 404
        })
        # if list isn't empty, this code will run
    return jsonify({
        "status": 200,
        "data": red_flags_as_dicts
    })


@app.route('/api/v1/red-flags/<int:flag_id>')
def get_specific_redflag(flag_id):
    """ This will return a red-flag specified by id """
    # first check if it exists and then return it
    if flag_id in RED_FLAGS:
        return jsonify({
            "status": 200,
            "data": [dict(RED_FLAGS[flag_id])]
        })

    # this code will run if the red-flag doesn't exist
    return jsonify({
        'error': "The redflag doesn't exist",
        'status': 404
    })


@app.route('/api/v1/red-flags', methods=['POST'])
def add_redflag_record():
    """ This will add a red-flag to the database """
    # check for empty request
    if not request.is_json:
        return jsonify({
            'error': 'Request Cannot Be Empty',
            'status': 400
        }), 400

    data = request.get_json()

    # check for missing data in request
    if ('created_by' not in data or 'type' not in data or
            'comment' not in data or 'location' not in data or
            'status' not in data):
        return jsonify({
            'status': 400,
            'error': 'Some Information is missing from the request'
        }), 400

    # return if request has no missing data
    incident = Incident(created_by=data['created_by'], type=data['type'],
                        location=data['location'], status=data['status'],
                        comment=data['comment'])
    RED_FLAGS[incident.flag_id] = incident
    return jsonify({"status": 201,
                    "data": [{
                        "id": incident.flag_id,
                        "message": "Created red-flag record"
                    }]
                    }), 201


@app.route('/api/v1/red-flags/<int:flag_id>', methods=['DELETE'])
def delete_red_flag(flag_id):
    """ This will delete a red-flag specified by id """
    # check if the record exists and delete the record
    if flag_id in RED_FLAGS:
        del RED_FLAGS[flag_id]
        return jsonify({"status": 204,
                        "data": [{
                            "id": flag_id,
                            "message": 'redflag record has been deleted'
                        }]
                        })
    # will run if the record doesn't exist
    return jsonify({
        "status": 204,
        "message": "Oops, looks like the record doesn't exist."
    })


@app.route('/api/v1/red-flags/<int:flag_id>/location', methods=['PATCH'])
def edit_red_flag_location(flag_id):
    """ This will edit the location of a red-flag given its id """
    # check if request has no json data in its body
    if not request.is_json:
        return jsonify({
            "error": 'Please provide a location',
            "status": 400
        })
    data = request.get_json()

    # check if record exists
    if flag_id in RED_FLAGS:
        RED_FLAGS[flag_id].location = data['location']
        return jsonify({
            "status": 201,
            "data": [{
                "id": flag_id,
                "message": "Updated red-flag record's location"
            }]
        })

    # this code will run if the red-flag doesn't exist
    return jsonify({
        "error": 400,
        "message": "Sorry, the red-flag record doesn't exist."
    })


@app.route('/api/v1/red-flags/<int:flag_id>/comment', methods=['PATCH'])
def patch_red_flag_comment(flag_id):
    """ This will edit the comment of a red-flag given the id """
    if not request.is_json:
        return jsonify({
            "error": 'Please provide a comment.',
            "status": 400
        })
    response = request.get_json()

    # check if record exists and patch it
    if flag_id in RED_FLAGS:
        RED_FLAGS[flag_id].comment = response['comment']
        return jsonify({"status": 204,
                        "data": [{
                            "id": flag_id,
                            "message": "Updated red-flag record's comment"
                        }]
                        })
    # this code will run if red-flag doesn't exist
    return jsonify({
        "error": 400,
        "message": "Sorry, the record doesn't exist"
    })
