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