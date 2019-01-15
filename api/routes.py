from api import app
from flask import jsonify, request, json
from api.models import User, Incident

redflags = {}

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/api/v1/red-flags',)
def get_all_redflags():
    red_flags_as_dicts = [dict(redflag) for redflag in redflags.values()]

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

@app.route('/api/v1/red-flags/<int:id>')
def get_specific_redflag(id):
	# first check if it exists and then return it
	if id in redflags:
		return jsonify({
                    "status": 200,
                    "data": [dict(redflags[id])]
                    })

	# this code will run if the red-flag doesn't exist					
	return jsonify({
                    'error': "The redflag doesn't exist",
                    'status': 404
                    })   

@app.route('/api/v1/red-flags', methods=['POST'])
def add_redflag_record():
	# check for empty request
    if not request.is_json:
        return jsonify({
                        'error': 'Request Cannot Be Empty',
                        'status': 400
                        }), 400

    data = request.get_json()

    # check for missing data in request
    if ('createdBy' not in data or 'type' not in data or 'comment' not in data or 
        'location' not in data or 'status' not in data):
        return jsonify({
                        'status': 400, 
                        'error': 'Some Information is missing from the request'
                        }), 400

	# return if request has no missing data
    incident = Incident(createdBy = data['createdBy'], type = data['type'], location = data['location'], 
                        status = data['status'], comment = data['comment'])
    redflags[incident.id] = incident
    return jsonify({"status": 201, 
                    "data": [{
                            "id": incident.id, 
                            "message": "Created red-flag record"
                            }]
                    }), 201

@app.route('/api/v1/red-flags/<int:id>', methods=['DELETE'])
def delete_red_flag(id):
	# check if the record exists and delete the record
	if id in redflags:
		del redflags[id]
		return jsonify({"status": 204,
                    "data": [{
                            "id" : id,
                            "message": 'redflag record has been deleted'
                             }]
                    })
	# will run if the record doesn't exist
	return jsonify({
                        "status": 204,
                        "message": "Oops, looks like the record doesn't exist."
                        })

@app.route('/api/v1/red-flags/<int:id>/location', methods=['PATCH'])
def edit_red_flag_location(id):
	# check if request has no json data in its body
	if not request.is_json:
		return jsonify({
			"error": 'Please provide a location',
			"status": 400
			})
	data = request.get_json()
	
	# check if record exists	
	if id in redflags:
		redflags[id].location = data['location']
		return jsonify({
                    	"status": 201,
                    	"data": [{
							"id" : id,
                            "message": "Updated red-flag record's location"
                            }]
                    	})

	# this code will run if the red-flag doesn't exist
	return jsonify({
                    "error": 400,
                    "message": 
                    "Are you are magician? Cause the record just disappeared from our database."
                    })

@app.route('/api/v1/red-flags/<int:id>/comment', methods=['PATCH'])
def patch_red_flag_comment(id):
	if not request.is_json:
		return jsonify({
			"error": 'Please provide a comment.',
			"status": 400
			})
	response = request.get_json()

	# check if record exists and patch it
	if id in redflags:
		redflags[id].comment = response['comment']
		return jsonify({"status": 204,
                    	"data": [{
                        	"id" : id,
                            "message": "Updated red-flag record's comment"
                            }]
						})
	# this code will run if red-flag doesn't exist
	return jsonify({
					"error": 400,
                    "message": "Sorry, the record doesn't exist"
                    })