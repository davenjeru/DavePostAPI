from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from davepostAPI.api.v1.boilerplate import safe_user_output
from davepostAPI.models import users_list

users_ns = Namespace('users')


class AllUsers(Resource):
    def get(self):
        """
            View all users
        """
        users = []
        for user in users_list:
            users.append(safe_user_output(self, user))
        return dict(users=users)
