from flask import url_for, request
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from davepostAPI.models import User


class PayloadExtractionError(BaseException):
    def __init__(self, msg: str, abort_code: int):
        self.msg = msg
        self.abort_code = abort_code


def get_validated_payload(resource: Resource):
    """
    Checks whether the request data is in JSON raising an error if not
    Evaluates the request data to a dict literal if it is a string or bytes object
    :param resource:
    :return: validated payload
    :rtype: dict
    """
    if request.content_type != 'application/json':
        raise PayloadExtractionError('request data should be in json format', 415)
    try:
        payload = eval(resource.api.payload) if type(resource.api.payload) == str else resource.api.payload
    except BadRequest:
        payload = eval(request.data) if bool(request.data) else None

    if payload is None:
        raise PayloadExtractionError('no data was found in the request', 400)
    return payload


def extract_from_payload(payload: dict, list_of_contexts: list):
    """
    Extracts items from the given dictionary raising an error if the item could not be found
    :param payload:
    :param list_of_contexts:
    :return: tuple of the items that were extracted
    """
    return_list = []
    for name in list_of_contexts:
        if payload.get(name) is None:
            raise PayloadExtractionError('missing \'{}\' parameter'.format(name), 400)
        return_list.append(payload.get(name))

    return tuple(return_list)


def generate_auth_output(resource, user):
    """
    Generates output specific to the auth namespace
    :param resource: The resource that called this function
    :param user: The user whose output should be generated
    :return: The output dictionary specific to the resource that called this function
    :rtype: dict
    """
    api = resource.api
    output_dict = dict(user=safe_user_output(resource, user))

    if api.url_for(resource) == url_for(api.endpoint('auth_register')):
        output_dict['message'] = 'user registered successfully'
    elif api.url_for(resource) == url_for(api.endpoint('auth_login')):
        output_dict['message'] = 'user logged in successfully'
    elif api.url_for(resource) == url_for(api.endpoint('auth_logout')):
        output_dict['message'] = 'user logged out successfully'

    return output_dict


def safe_user_output(resource: Resource, user: User):
    """
    Creates a dictionary of a User's details
    :param resource:
    :param user:
    :return: dict
    """
    api = resource.api
    user_dict = user.serialize
    user_dict['url'] = url_for(api.endpoint('users_single_user'), user_id=user.id)
    return user_dict
