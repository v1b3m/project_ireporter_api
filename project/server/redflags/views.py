from db import DatabaseConnection

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from flasgger import swag_from

from project.server.auth.helpers import token_required, admin_required
from project.server.redflags.helpers import (validate_add_redflag_data,
                                             validate_edit_comment_data,
                                             validate_edit_location_data,
                                             validate_edit_status_data)

redflags_blueprint = Blueprint('redflags', __name__)

db_name = DatabaseConnection()


class GetRedflagsAPI(MethodView):
    """
    Redflag and Intervention resource
    """
    @token_required
    @swag_from('../docs/get_redflag.yml')
    def get(self):
        """
        get red-flags
        """
        red_flags = db_name.get_redflags()

        if not red_flags:
            return jsonify({
                'error': 'There are no redflags',
                'status': 404
            })

        responseObject = ({
            "status": 200,
            "data": [dict(redflag) for redflag in red_flags]
        })
        return jsonify(responseObject), 200


class GetSpecificRedflagAPI(MethodView):
    """
    Get a specific red-flag
    """
    @token_required
    @swag_from('../docs/get_specific_redflag.yml')
    def get(self, flag_id):
        redflag = db_name.get_incident(flag_id)
        if redflag:
            return jsonify({
                "status": 200,
                "data": [dict(redflag)]
            })

        # this code will run if the red-flag doesn't exist
        return jsonify({
            'error': "The redflag doesn't exist",
            'status': 404
        })


class CreateRedflagsAPI(MethodView):
    """
    Create redflags here
    """
    @token_required
    @swag_from('../docs/add_redflag.yml')
    def post(self):
        """
        add a redflag
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
        if validate_add_redflag_data(data):
            return jsonify({"error": 400,
                            "message": validate_add_redflag_data(data)
                            }), 400

        # return if request has no missing data
        incident_id = db_name.create_incident(created_by=data['created_by'], type=data['type'],
                                              location=data['location'], comment=data['comment'],
                                              videos="a.mp4", images="a.jpg")
        return jsonify({"status": 201,
                        "data": [{
                            "id": incident_id,
                            "message": "Created red-flag record"
                        }]
                        }), 201


class DeleteRedflagsAPI(MethodView):
    """
    Delete a redflag
    """
    @token_required
    @swag_from('../docs/delete_flag.yml')
    def delete(self, flag_id):
        """ This will delete a red-flag specified by id """
        # check if the record exists and delete the record
        red_flag = db_name.get_incident(flag_id)
        if red_flag:
            db_name.delete_incident(flag_id)
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


class PatchRedflagLocationAPI(MethodView):
    """
    Patch a redflag location
    """
    @token_required
    @swag_from('../docs/patch_flag_location.yml')
    def patch(self, flag_id):
        # check if request has no json data in its body
        if not request.is_json:
            return jsonify({
                "error": 'Please provide a location',
                "status": 400
            })
        data = request.get_json()

        # check for location in missing data
        if 'location' not in data:
            return jsonify({
                'error': "Location data not found",
                "status": 400
            }), 400

        # validate the data
        if validate_edit_location_data(data):
            return jsonify({"error": 400,
                            "message": validate_edit_location_data(data)
                            }), 400

        # check if record exists
        red_flag = db_name.get_incident(flag_id)
        if red_flag:
            db_name.edit_incident_location(flag_id, data['location'])
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


class PatchRedflagCommentAPI(MethodView):
    """
    Patch a redflag location
    """
    @token_required
    @swag_from('../docs/patch_flag_comment.yml')
    def patch(self, flag_id):
        # check if request has no json data in its body
        if not request.is_json:
            return jsonify({
                "error": 'Please provide a comment',
                "status": 400
            })
        data = request.get_json()

        # check for location in missing data
        if 'comment' not in data:
            return jsonify({
                'error': "Comment data not found",
                "status": 400
            }), 400

        # validate the data
        if validate_edit_comment_data(data):
            return jsonify({"error": 400,
                            "message": validate_edit_comment_data(data)
                            }), 400

        # check if record exists
        red_flag = db_name.get_incident(flag_id)
        if red_flag:
            db_name.edit_incident_comment(flag_id, data['comment'])
            return jsonify({
                "status": 201,
                "data": [{
                    "id": flag_id,
                    "message": "Updated red-flag record's comment"
                }]
            })

        # this code will run if the red-flag doesn't exist
        return jsonify({
            "error": 400,
            "message": "Sorry, the red-flag record doesn't exist."
        })


class WelcomeAPI(MethodView):
    """
    Welcome API
    """

    def get(self):
        """ This route will return the message "Hello, World" """
        return "Hello, World!"


class UpdateStatusAPI(MethodView):
    """
    Patch a redflag status
    """
    @admin_required
    @swag_from('../docs/edit_flag_status.yml')
    def patch(self, flag_id):
        # check if request has no json data in its body
        if not request.is_json:
            return jsonify({
                "error": 'Please provide a status',
                "status": 400
            })
        data = request.get_json()

        # check for location in missing data
        if 'status' not in data:
            return jsonify({
                'error': "Status data not found",
                "status": 400
            }), 400

        # validate the data
        if validate_edit_status_data(data):
            return jsonify({"error": 400,
                            "message": validate_edit_status_data(data)
                            }), 400

        # check if record exists
        red_flag = db_name.get_incident(flag_id)
        if red_flag:
            db_name.update_incident_status(flag_id, data['status'])
            return jsonify({
                "status": 201,
                "data": [{
                    "id": flag_id,
                    "message": "​Updated red-flag record status"
                }]
            })

        # this code will run if the red-flag doesn't exist
        return jsonify({
            "error": 400,
            "message": "Red-flag record doesn't exist."
        })


# define the API resources
get_redflags_view = GetRedflagsAPI.as_view('get_redflags_api')
get_specific_redflag_view = GetSpecificRedflagAPI.as_view(
    'get_specific_redflag_api')
add_redflags_view = CreateRedflagsAPI.as_view('create_redflags_api')
delete_redflags_view = DeleteRedflagsAPI.as_view('delete_redflags_api')
edit_redflag_location_view = PatchRedflagLocationAPI.as_view(
    'patch_redflag_location_api')
edit_redflag_comment_view = PatchRedflagCommentAPI.as_view(
    'patch_redflag_comment_api')
welome_view = WelcomeAPI.as_view('welcome_api')
update_redflag_status = UpdateStatusAPI.as_view('update_status_api')

# add rules for API endpoints
redflags_blueprint.add_url_rule(
    '/',
    view_func=welome_view,
    methods=['GET']
)
redflags_blueprint.add_url_rule(
    '/api/v2/red-flags',
    view_func=get_redflags_view,
    methods=['GET']
)
redflags_blueprint.add_url_rule(
    '/api/v2/red-flags/<int:flag_id>',
    view_func=get_specific_redflag_view,
    methods=['GET']
)
redflags_blueprint.add_url_rule(
    '/api/v2/red-flags',
    view_func=add_redflags_view,
    methods=['POST']
)
redflags_blueprint.add_url_rule(
    '/api/v2/red-flags/<int:flag_id>',
    view_func=delete_redflags_view,
    methods=['DELETE']
)
redflags_blueprint.add_url_rule(
    '/api/v2/red-flags/<int:flag_id>/location',
    view_func=edit_redflag_location_view,
    methods=['PATCH']
)
redflags_blueprint.add_url_rule(
    '/api/v2/red-flags/<int:flag_id>/comment',
    view_func=edit_redflag_comment_view,
    methods=['PATCH']
)
redflags_blueprint.add_url_rule(
    '/api/v2/red-flags/<int:flag_id>/status',
    view_func=update_redflag_status,
    methods=['PATCH']
)
