from db import DatabaseConnection

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server.redflags.helpers import (validate_add_redflag_data,
                                            validate_edit_comment_data,
                                            validate_edit_location_data)

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

# define the API resources
get_interventions_view = GetInterventionsAPI.as_view('get_interventions_api')

# add rules for API endpoints
interventions_blueprint.add_url_rule(
    '/api/v1/interventions',
    view_func=get_interventions_view,
    methods=['GET']
)