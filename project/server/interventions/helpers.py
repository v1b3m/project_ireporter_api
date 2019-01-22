""" This script will contain all helper functions """

def validate_add_intervention_data(data):
    """ This function will be used to
        validate input_data """
    try:
        if not isinstance(data['location'], str):
            raise TypeError("location must be a string")
        if not isinstance(data['type'], str):
            raise TypeError("type must be a string")
        if not isinstance(data['comment'], str):
            raise TypeError("comment must be a string")
        if not isinstance(data['created_by'], int):
            raise TypeError("created_by must be an integer")
    except TypeError as error:
        return str(error)
    return None