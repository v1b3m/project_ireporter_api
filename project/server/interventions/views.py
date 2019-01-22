from db import DatabaseConnection

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server.interventions.helpers import (validate_add_intervention_data)

interventions_blueprint = Blueprint('interventions', __name__)

db_name = DatabaseConnection()

class GetInterventionsAPI(MethodView):
    """
    Intervention resource
    """

    def get(self):
        """
        get red-flags
        """
        interventions = db_name.get_interventions()

        if not interventions:
            return jsonify({
            'error': 'There are no interventions',
            'status': 404
        })

        responseObject = ({
            "status": 200,
            "data": [dict(intervention) for intervention in interventions]
        })
        return jsonify(responseObject), 200

class GetSpecificInterventionAPI(MethodView):
    """
    Get a specific intervention
    """
    def get(self, intervention_id):
        intervention = db_name.get_incident(intervention_id)
        if intervention:
            return jsonify({
                "status": 200,
                "data": [dict(intervention)]
            })
        
        # this code will run if the red-flag doesn't exist
        return jsonify({
            'error': "The intervention doesn't exist",
            'status': 404
        })

class CreateInterventionsAPI(MethodView):
    """
    Create interventions here
    """

    def post(self):
        """
        add an intervention
        """
        # check for empty request
        if not request.is_json:
            return jsonify({
                'error': 'Request Cannot Be Empty',
                'status': 400
            }), 400

        data = request.get_json()

        # check for missing data in request
        if ('created_by' not in data or 'type' not in data or
                'comment' not in data or 'location' not in data):
            return jsonify({
                'status': 400,
                'error': 'Some Information is missing from the request'
            }), 400

        # validate the input data
        if validate_add_intervention_data(data):
            return jsonify({"error": 400,
                            "message": validate_add_intervention_data(data)
                            }), 400

        # return if request has no missing data
        incident_id = db_name.create_incident(created_by=data['created_by'], type=data['type'],
                            location=data['location'], comment=data['comment'],
                            videos="a.mp4", images="a.jpg")
        return jsonify({"status": 201,
                        "data": [{
                            "id": incident_id,
                            "message": "Created intervention record"
                        }]
                        }), 201

class DeleteInterventionsAPI(MethodView):
    """
    Delete a redflag
    """
    def delete(self, intervention_id):
        """ This will delete a red-flag specified by id """
        # check if the record exists and delete the record
        red_flag = db_name.get_incident(intervention_id)
        if red_flag:
            db_name.delete_incident(intervention_id)
            return jsonify({"status": 204,
                            "data": [{
                                "id": intervention_id,
                                "message": 'intervention record has been deleted'
                            }]
                            })
        # will run if the record doesn't exist
        return jsonify({
            "status": 204,
            "message": "Oops, looks like the record doesn't exist."
        })


# define the API resources
get_interventions_view = GetInterventionsAPI.as_view('get_interventions_api')
get_specific_intervention_view = GetSpecificInterventionAPI.as_view('get_specific_intervention_api')
add_interventions_view = CreateInterventionsAPI.as_view('create_interventions_api')
delete_interventions_view = DeleteInterventionsAPI.as_view('delete_interventions_api')

# add rules for API endpoints
interventions_blueprint.add_url_rule(
    '/api/v1/interventions',
    view_func=get_interventions_view,
    methods=['GET']
)
interventions_blueprint.add_url_rule(
    '/api/v1/interventions/<int:intervention_id>',
    view_func=get_specific_intervention_view,
    methods=['GET']
)
interventions_blueprint.add_url_rule(
    '/api/v1/interventions',
    view_func=add_interventions_view,
    methods=['POST']
)
interventions_blueprint.add_url_rule(
    '/api/v1/interventions/<int:intervention_id>',
    view_func=delete_interventions_view,
    methods=['DELETE']
)