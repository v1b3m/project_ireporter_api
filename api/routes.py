from api import app
from flask import jsonify, request, json
from api.models import User, Incident

redflags = []

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/api/v1/red-flags',)
def get_all_redflags():
    red_flags_as_dicts = [redflag.to_dict() for redflag in redflags]

    if len(red_flags_as_dicts) < 1:
        return jsonify({'message': 'There are no redflags',
                        'status': 400})
    return jsonify({"status": 200,
                    "data": red_flags_as_dicts})

@app.route('/api/v1/red-flags/<int:id>')
def get_specific_redflag(id):
    redflag = None
    for item in redflags:
        if item._id == id:
            redflag = item.to_dict()
    if redflag is None: 
        return jsonify({'message': "The redflag doesn't exist",
                        'status': 404})   
    return jsonify({"status": 200,
                    "data": redflag})

@app.route('/api/v1/red-flags', methods=['POST'])
def add_redflag_record():
    if not request.is_json:
        return jsonify({'error': 'Request Cannot Be Empty'}), 404

    data = request.get_json()
    print(data)

    if 'createdBy' not in data or 'type' not in data or 'comment' not in data or 'location' not in data or 'status' not in data:
        return jsonify({'status': 400, 'error': 'Some Information is missing from the request'}), 400
    incident = Incident(data['createdBy'], data['type'], data['location'], data['status'], data['comment'])
    redflags.append(incident)
    return jsonify({"status": 200, "data": [{"id": incident._id, "message": "Created red-flag record"}]}), 200

@app.route('/api/v1/red-flags/<int:id>', methods=['DELETE'])
def delete_red_flag(id):
    x = None
    for item in redflags:
        if item._id == id:
            x = item
            redflags.remove(item)
    if x is None:
        return jsonify({"status": 204,
                        "message": "Oops, looks like the record doesn't exist."})
    return jsonify({"status": 204,
                    "data": [{
                        "id" : id,
                        "message": 'redflag record has been deleted'
                    }]})

@app.route('/api/v1/red-flags/<int:id>/location', methods=['PATCH'])
def edit_red_flag_location(id):
    x = None
    if not request.is_json:
        return jsonify({"error": 'Please provide a location'})
    data = request.get_json()
    print(data)
    
    for flag in redflags:
        if flag._id == id:
            x = flag
            flag.location = data['location']
    if x is None:
        return jsonify({"status": 400,
                        "message": "Are you are magician? Cause the record just disappeared from our database."})
    return jsonify({"status": 204,
                    "data": [{
                        "id" : id,
                        "message": "Updated red-flag record's location"
                    }]})

@app.route('/api/v1/red-flags/<int:id>/comment', methods=['PATCH'])
def patch_red_flag_comment(id):
    x = None
    reds = redflags
    response = request.get_json()

    for item in reds:
        if item._id == id:
            x = item
            item.comment = response['comment']
    
    if x is None:
        return jsonify({"Status": 400,
                        "message": "Sorry, the record doesn't exist"})
    
    return jsonify({"status": 204,
                    "data": [{
                        "id" : id,
                        "message": "Updated red-flag record's comment"
                    }]})
