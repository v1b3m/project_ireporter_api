from db import DatabaseConnection

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from flasgger import swag_from

from project.server.auth.helpers import token_required, admin_required,current_identity
from project.server.validation.validators import (missing_data,
                                                  string_data, wrong_status_data, valid_create_data)

redflags_blueprint = Blueprint('redflags', __name__, url_prefix='/api/v2')

db_name = DatabaseConnection()


class GetRedflagsAPI(MethodView):
    """Redflag and Intervention resource"""
    @token_required
    @swag_from('../docs/get_redflag.yml')
    def get(self):
        """get red-flags"""
        red_flags = db_name.get_incidents('red-flag')

        if not red_flags:
            return jsonify({
                'error': 'There are no redflags',
                'status': 404
            }), 404

        responseObject = ({
            "status": 200,
            "data": [dict(redflag) for redflag in red_flags]
        })
        return jsonify(responseObject), 200


class GetSpecificRedflagAPI(MethodView):
    """Get a specific red-flag"""
    @token_required
    @swag_from('../docs/get_specific_redflag.yml')
    def get(self, flag_id):
        redflag = db_name.get_incident(flag_id)
        if redflag:
            return jsonify({
                "status": 200,
                "data": [dict(redflag)]
            }), 200

        # this code will run if the red-flag doesn't exist
        return jsonify({
            'error': "The redflag doesn't exist",
            'status': 404
        }), 404


class CreateRedflagsAPI(MethodView):
    """Create redflags here"""
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
        error = None
        if valid_create_data(data):
            error = valid_create_data(data)

        # validate the input data
        if error:
            return jsonify({"status": 400,
                            "error": error
                            }), 400

        # return if request has no missing data
        incident_id = db_name.create_incident(created_by=current_identity(), type=data['type'],
                                              location=data['location'], comment=data['comment'],
                                              videos="a.mp4", images="a.jpg")
        return jsonify({"status": 201,
                        "data": [{"id": incident_id,
                                  "message": "Created red-flag record"
                                  }]}), 201


class DeleteRedflagsAPI(MethodView):
    """Delete a redflag"""
    @token_required
    @swag_from('../docs/delete_flag.yml')
    def delete(self, flag_id):
        """ This will delete a red-flag specified by id """

        # check if the record exists and delete the record
        red_flag = db_name.get_incident(flag_id)
        if red_flag:
            my_item = db_name.created_by(flag_id, current_identity())
            if my_item:
                db_name.delete_incident(flag_id, current_identity())
                return jsonify({"status": 200,
                                "data": [{"id": flag_id,
                                          "message": 'redflag record has been deleted'
                                          }]}), 200
            else:
                return jsonify({
                    "status": 400,
                    "error": "You don't have the rights to delete this incident."
                    }), 400
        # will run if the record doesn't exist
        return jsonify({"status": 404,
                        "message": "Oops, looks like the record doesn't exist."
                        }), 404


class PatchRedflagLocationAPI(MethodView):
    """Patch a redflag location"""
    @token_required
    @swag_from('../docs/patch_flag_location.yml')
    def patch(self, flag_id):
        # check for empty request
        if not request.is_json:
            return jsonify({
                'error': 'Request Cannot Be Empty',
                'status': 400
            }), 400

        # check if request has no json data in its body
        data = request.get_json()

        # check for errors in data
        error = None
        if missing_data(data, 'location'):
            error = missing_data(data,'location')

        # return the error message
        if error:
            return jsonify({"status": 400,
                            "error": error
                            }), 400

        # check if record exists
        red_flag = db_name.get_incident(flag_id)
        if red_flag:
            my_item = db_name.created_by(flag_id, current_identity())
            if my_item:
                db_name.edit_incident(flag_id, 'location', data['location'])
                return jsonify({
                    "status": 201,
                    "data": [{"id": flag_id,
                              "message": "Updated red-flag record's location"
                              }]}), 201
            else:
                return jsonify({
                    "status": 400,
                    "error": "You don't have the rights to edit this incident."
                    }), 400

        # this code will run if the red-flag doesn't exist
        return jsonify({"error": 404,
                        "message": "Sorry, the red-flag record doesn't exist."
                        }), 404


class PatchRedflagCommentAPI(MethodView):
    """Patch a redflag comment"""
    @token_required
    @swag_from('../docs/patch_flag_comment.yml')
    def patch(self, flag_id):
        # check if request has no json data in its body
        if not request.is_json:
            return jsonify({
                "error": 'Please provide a comment',
                "status": 400
            }), 400
        data = request.get_json()

        # check for errors in data
        error = None
        if missing_data(data, 'comment'):
            error = missing_data(data,'comment')

        # return the error
        if error:
            return jsonify({
                'error': error,
                "status": 400
            }), 400

        # check if record exists
        red_flag = db_name.get_incident(flag_id)
        if red_flag:
            my_item = db_name.created_by(flag_id, current_identity())
            if my_item:
                db_name.edit_incident(flag_id, 'comment', data['comment'])
                return jsonify({
                    "status": 201,
                    "data": [{"id": flag_id,
                              "message": "Updated red-flag record's comment"
                              }]}), 201
            else:
                return jsonify({
                    "status": 400,
                    "error": "You don't have the rights to edit this incident."
                }), 400

        # this code will run if the red-flag doesn't exist
        return jsonify({"error": 404,
                        "message": "Sorry, the red-flag record doesn't exist."
                        }), 404

class UpdateStatusAPI(MethodView):
    """Patch a redflag status"""
    @admin_required
    @swag_from('../docs/edit_flag_status.yml')
    def patch(self, flag_id):
        # check if request has no json data in its body
        if not request.is_json:
            return jsonify({
                "error": 'Please provide a status',
                "status": 400
            }), 400
        data = request.get_json()

        # check for location in missing data
        error = None
        if wrong_status_data(data):
            error = wrong_status_data(data)
        if error:
            return jsonify({"status": 400,
                            "error": error
                            }), 400

        # check if record exists
        red_flag = db_name.get_incident(flag_id)
        if red_flag:
            db_name.edit_incident(flag_id, 'status', data['status'])
            return jsonify({
                "status": 201,
                "data": [{"id": flag_id,
                          "message": "Updated red-flag record status"
                          }]}), 201

        # this code will run if the red-flag doesn't exist
        return jsonify({"error": 404,
                        "message": "Red-flag record doesn't exist."
                        }), 404


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
update_redflag_status = UpdateStatusAPI.as_view('update_status_api')

# add rules for API endpoints
redflags_blueprint.add_url_rule(
    '/red-flags',
    view_func=get_redflags_view,
    methods=['GET']
)
redflags_blueprint.add_url_rule(
    '/red-flags/<int:flag_id>',
    view_func=get_specific_redflag_view,
    methods=['GET']
)
redflags_blueprint.add_url_rule(
    '/red-flags',
    view_func=add_redflags_view,
    methods=['POST']
)
redflags_blueprint.add_url_rule(
    '/red-flags/<int:flag_id>',
    view_func=delete_redflags_view,
    methods=['DELETE']
)
redflags_blueprint.add_url_rule(
    '/red-flags/<int:flag_id>/location',
    view_func=edit_redflag_location_view,
    methods=['PATCH']
)
redflags_blueprint.add_url_rule(
    '/red-flags/<int:flag_id>/comment',
    view_func=edit_redflag_comment_view,
    methods=['PATCH']
)
redflags_blueprint.add_url_rule(
    '/red-flags/<int:flag_id>/status',
    view_func=update_redflag_status,
    methods=['PATCH']
)
