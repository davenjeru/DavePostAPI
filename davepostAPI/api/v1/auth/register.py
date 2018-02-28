from flask_restplus import Resource
from flask_restplus.namespace import Namespace

auth_ns = Namespace('auth')


class Register(Resource):
    @auth_ns.response(201, 'user created successfully')
    @auth_ns.response(415, 'request data not in json format')
    @auth_ns.response(400, 'bad request')
    def post(self):
        """
        User registration

        1. Email address should be syntactically valid.
        2. Password should have a minimum of 12 characters and a maximum of 80 characters
        3. Password should have no spaces
        4. Password should have at least one number, uppercase and lowercase letter.
        5. Password should have at least one of these special characters !@#$%^;*()_+}{:'?/.,

        """
        pass
