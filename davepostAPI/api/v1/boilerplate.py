from flask import url_for, request
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from davepostAPI.models import User, Post


class PayloadExtractionError(BaseException):
    def __init__(self, msg: str, abort_code: int = 400):
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


def check_id_availability(the_id: int, a_list: list, context: str):
    """
    Checks for the availability of an item's ID in a given list
    :param the_id: the ID to be checked
    :param a_list: the list from where to check from
    :param context: used for displaying the error message
    :return: the item if found, abort otherwise
    """
    for an_item in a_list:
        if an_item.id == the_id:
            return an_item
    else:
        raise PayloadExtractionError('{0} not found!'.format(context))


def safe_post_output(resource: Resource, post: Post):
    """
    Creates a dictionary of Post details
    :param resource:
    :param post:
    :return: dict
    """
    api = resource.api
    post_dict = post.serialize
    post_dict['post_url'] = url_for(api.endpoint('users_single_user_single_post'), user_id=post.user_id,
                                    post_id=post.id)
    post_dict['author_url'] = url_for(api.endpoint('users_single_user'), user_id=post.user_id)
    return post_dict


def generate_post_output(resource: Resource, post: Post, method: str):
    """
    Generates output specific to the users namespace
    :param resource: The resource that called this function
    :param post: The user whose output should be generated
    :param method: The HTTP method
    :return: The output dictionary specific to the resource that called this function
    :rtype: dict
    """
    output_dict = dict(post=safe_post_output(resource, post))

    if resource.endpoint == 'users_single_user_all_posts':
        if method == 'post':
            output_dict['message'] = 'post created successfully'
    elif resource.endpoint == 'users_single_user_single_post':
        if method == 'patch':
            output_dict['message'] = 'post modified successfully'

    return output_dict
