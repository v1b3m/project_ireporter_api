""" This script will contain all helper functions """


def validate_add_redflag_data(data):
    """ This function will be used to
        validate input_data """
    try:
        if(
            not data['location']
            or not isinstance(data['location'], str)
            or data['location'].isspace()
        ):
            raise TypeError("location must be a string")
        if (
            not data['type']
            or not isinstance(data['type'], str)
            or data['type'].isspace()
        ):
            raise TypeError("type must be a string")
        if (
            not data['comment']
            or not isinstance(data['comment'], str)
            or data['comment'].isspace()
        ):
            raise TypeError("comment must be a string")
        if not isinstance(data['created_by'], int):
            raise TypeError("created_by must be an integer")
        if data['type'] not in ['red-flag', 'intervention']:
            raise ValueError("types can only be `red-flag` or `intervention`")
    except (TypeError, ValueError) as error:
        return str(error)
    return None


def validate_edit_location_data(data):
    """ This function will validate the data
        used to edit a location """
    try:
        if not isinstance(data['location'], str):
            raise TypeError('location must be a string')
    except TypeError as error:
        return str(error)
    return None


def validate_edit_comment_data(data):
    """ This function will validate the data
        used to edit a comment """
    try:
        if not isinstance(data['comment'], str):
            raise TypeError("comment must be a string")
    except TypeError as error:
        return str(error)
    return None


def validate_edit_status_data(data):
    """ This function will validate the data
        used to edit a status """
    try:
        if not isinstance(data['status'], str):
            raise TypeError('status must be a string')
        if data['status'] not in ['​under investigation', 'rejected', 'resolved']:
            raise ValueError(
                "status can only be `​under investigation`,`rejected` or `resolved` ")
    except (TypeError, ValueError) as error:
        return str(error)
    return None
