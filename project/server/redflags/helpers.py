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

def validate_edit_data(data, type):
    try:
        if type == 'location':
            if(
                not data['location']
                or not isinstance(data['location'], str)
                or data['location'].isspace()
            ):
                raise TypeError('location must be a string')
        elif type=='comment':
            if(
                not data['comment']
                or not isinstance(data['comment'], str)
                or data['comment'].isspace()
            ):
                raise TypeError("comment must be a string")
        elif type=='status':
            if(
                not data['status']
                or not isinstance(data['status'], str)
                or data['status'].isspace()
            ):
                raise TypeError('status must be a string')
            if data['status'] not in ['​under investigation', 'rejected', 'resolved']:
                raise ValueError(
                "status can only be `​under investigation`,`rejected` or `resolved` ")
    except (ValueError, TypeError) as e:
        return str(e)
    return None


