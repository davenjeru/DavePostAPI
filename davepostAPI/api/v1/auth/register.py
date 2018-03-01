from flask import url_for
from flask_restplus import Resource, fields
from flask_restplus.namespace import Namespace

from davepostAPI.models import User, UserTransactionError
from .boilerplate import get_validated_payload, extract_from_payload, generate_auth_output, \
    PayloadExtractionError

auth_ns = Namespace('auth')

# Model definition of what to expect from the request data
definition = dict(email=fields.String(title='Your email address', required=True, example='myemail@company.com'),
                  password=fields.String(title='Your password', required=True,
                                         example='password.Pa55word'),
                  confirm_password=fields.String(title='Confirm your password', required=True,
                                                 example='password.Pa55word'),
                  security_question=fields.String(title='Your security question', required=True,
                                                  example='What is your favourite company?'),
                  security_answer=fields.String(title='Your security answer', required=True,
                                                example='company'))

user_registration_model = auth_ns.model('user_registration_model', definition)


class Register(Resource):
    @auth_ns.expect(user_registration_model)
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
        6. Your security question should start with a 'Wh' or an 'Are' clause
        7. There should be no punctuations in your security question
        (apart from a compulsory question mark '?' at the end) and answer

        """
        payload = None

        # This is a short cut for setting all these values to None with minimal code
        email, password, confirm_password, security_question, security_answer = tuple('    '.split(' '))

        try:
            payload = get_validated_payload(self)
        except PayloadExtractionError as e:
            auth_ns.abort(e.abort_code, e.msg)

        list_of_names = ['email', 'password', 'confirm_password', 'security_question', 'security_answer']
        try:
            email, password, confirm_password, security_question, \
            security_answer = extract_from_payload(payload, list_of_names)
        except PayloadExtractionError as e:
            auth_ns.abort(e.abort_code, e.msg)

        if password != confirm_password:
            auth_ns.abort(400, 'passwords do not match')

        created_user = None
        try:
            created_user = User(email, password, security_question, security_answer)
        except UserTransactionError as e:
            auth_ns.abort(e.abort_code, e.msg)

        output = generate_auth_output(self, created_user)
        response = self.api.make_response(output, 201)
        response.headers['location'] = url_for(self.api.endpoint('users_single_user'), user_id=created_user.id)

        return response
