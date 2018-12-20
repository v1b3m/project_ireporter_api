from api import app
from flask import jsonify, request, json

redflags = [{
            "id": 1,
            "createdOn" : "2018-21-23 21:15",
            "createdBy" : "Benjamin",
            "type" : "red-flag",
            "location" : {"lat":"0.96","long":"1.23"},
            "status" : "Pending",
            "Images" : ["me.jpg"],
            "Videos": ['ben.mp4'],
            "comment": "I am the greatest" },
            {
            "id": 2,
            "createdOn" : "2014-21-23 21:15",
            "createdBy" : "Breezy",
            "type" : "red-flag",
            "location" : {"lat":"0.96","long":"1.23"},
            "status" : "Approved",
            "Images" : ["me.jpg"],
            "Videos": ['ben.mp4'],
            "comment": "I am the bestest" }
            ]

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/api/v1/red-flags',)
def get_all_redflags():
    red_flags = redflags

    if len(red_flags) < 1:
        return jsonify({'message': 'There are no redflags'}), 400
    return jsonify({"status": 200,
                    "data": red_flags})

@app.route('/api/v1/red-flags/<int:id>')
def get_specific_redflag(id):
    redflag = None
    for item in redflags:
        if item["id"] == id:
            redflag = item
    if redflag is None: 
        return jsonify({'message': "The redflag doesn't exist"}), 404    
    return jsonify({"status": 200,
                    "data": redflag})

@app.route('/api/v1/red-flags', methods=['POST'])
def add_redflag_record():
    data = request.get_json()
    print(data)

    try:
        if data is None:
            raise TypeError('Data cannot be empty')
        if type(data['id']) is not int:
            raise ValueError('id should be an integer')
        redflags.append(data)
    except ValueError as e:
        print(e)
        return jsonify({'message': 'Id should be an integer'}), 400
    return jsonify({"status": 201,
                    "data": [{
                        "id" : data['id'],
                        "message": 'Created redflag record'
                    }]})

@app.route('/api/v1/red-flags/<int:id>', methods=['DELETE'])
def delete_red_flag(id):
    for item in redflags:
        if item["id"] == id:
            redflags.remove(item)
    return jsonify({"status": 204,
                    "data": [{
                        "id" : id,
                        "message": 'redflag record has been deleted'
                    }]})

@app.route('/api/v1/red-flags/<int:id>/location', methods=['PATCH'])
def edit_red_flag_location(id):
    data = request.get_json()
    print(data)
    
    for item in redflags:
        if item['id'] == id:
            item['location'] = data['location']
    
    return jsonify({"status": 204,
                    "data": [{
                        "id" : id,
                        "message": "Updated red-flag record's location"
                    }]})

@app.route('/api/v1/red-flags/<int:id>/comment', methods=['PATCH'])
def edit_red_flag_comment(id):
    data = request.get_json()
    print(data)

    for item in redflags:
        if item['id'] == id:
            item['comment'] = data['comment']
    
    return jsonify({"status": 204,
                    "data": [{
                        "id" : id,
                        "message": "Updated red-flag record's comment"
                    }]})
