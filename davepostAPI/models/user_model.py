import re
import string

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .post_model import Post, posts_list

users_list = []


class UserTransactionError(BaseException):
    """
    This is the exception raised if there is an error when creating a user
    """

    def __init__(self, msg, abort_code=400):
        self.msg = msg
        self.abort_code = abort_code


class User(UserMixin, object):
    """
    This is the user class.
    Defines a user and all actions that can be done by it.
    """

    id = 1

    def __init__(self, email: str, password: str, security_question: str, security_answer: str):
        try:
            self._validate_user_details('email', email)
            self._validate_user_details('password', password)
            self._validate_user_details('security question', security_question)
            self._validate_user_details('security answer', security_answer)
        except AssertionError as a:
            raise UserTransactionError(a.args[0])

        for user in users_list:
            if user.email == email:
                raise UserTransactionError('a user with similar email exists')

        self.email = email
        self.password_hash = generate_password_hash(password)
        self.id = User.id
        self.security_question = security_question
        self.security_answer = generate_password_hash(security_answer)
        self.__save()

    def __save(self):
        """
        Stores user in the users list
        """
        User.id += 1
        users_list.append(self)

    def get_id(self):
        """
        Returns unicode user ID for use by Flask-Login
        """
        return chr(self.id)

    def authenticate(self, password: str):
        """
        :param password: The password to be checked
        :return: True if the password is correct, False otherwise
        :rtype: bool
        """
        return check_password_hash(self.password_hash, password)

    def reset_password(self, security_question: str, security_answer: str, new_password: str):
        """
        Enables user to reset password
        :param security_question: The security question that the user chose
        :param security_answer: The answer to the above question
        :param new_password: The new password to be set
        """
        if self.security_question == security_question:
            if check_password_hash(self.security_answer, security_answer):
                try:
                    self._validate_user_details('password', new_password)
                    self.password_hash = generate_password_hash(new_password)
                except AssertionError as a:
                    raise UserTransactionError(a.args[0])
            else:
                raise UserTransactionError('wrong security answer')
        else:
            raise UserTransactionError('wrong security question!')

    def create_post(self, title: str, body: str):
        """
        User can create a post
        :param title:
        :param body:
        :return: the created post
        :rtype: Post
        """
        my_post = Post(self, title, body)
        return my_post

    def update_post(self, name: str, item: str, post: Post):
        """
        User can update their post
        :param name: Context of the update
        :param item: Item to be patched
        :param post: The post to be updated
        :return: The updated post
        """
        return post.update(self, name, item)

    def delete_post(self, post):
        """
        User can delete a post
        :param post: Post to be deleted
        :return:
        """
        return post.delete(self)

    @staticmethod
    def _validate_user_details(name: str, item: str):
        """
        Validates input depending on the given context
        :param name: context of validation
        :param item: item to be validated
        """

        def validate_security_question_or_answer(context: str, validation_item: str):
            max_length, min_length = None, None
            if context == 'security question':
                max_length = 50
                min_length = 10

                if validation_item[0] not in list('WwAa'):
                    raise AssertionError('{} must start with a \'Wh\' or a \'Are\' question'.format(context))

                if validation_item[-1] != '?':
                    raise AssertionError('{} must end with a question mark \'?\''.format(context))

                for char in list(validation_item[:-1]):
                    if char in string.punctuation:
                        raise AssertionError('{} must not contain any punctuations mid sentence'.format(context))

            if context == 'security answer':
                max_length = 20
                min_length = 5

                if len(validation_item) < 5:
                    raise AssertionError('{} is too short. Min of 5 characters'.format(context))
                if len(validation_item) > 20:
                    raise AssertionError('{} too long. Max of 20 characters'.format(context))

                for char in list(validation_item):
                    if char in string.punctuation:
                        raise AssertionError('{} must not contain any punctuations'.format(context))

            if len(validation_item) < min_length:
                raise AssertionError('{0} is too short. Min of {1} characters'.format(context, min_length))
            if len(validation_item) > max_length:
                raise AssertionError('{0} too long. Max of {1} characters'.format(context, max_length))

            for word in validation_item.split(' '):
                if not word:
                    raise AssertionError('Please check the spacing on your {}'.format(context))

        email_pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        password_pattern = re.compile(
            r"(?=^.{12,80}$)(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^;*()_+}{:'?/.,])(?!.*\s).*$")

        if not item:
            raise AssertionError('missing \"{0}\" parameter'.format(name))

        if name == 'email':
            if not bool(email_pattern.match(item)):
                raise AssertionError('email address syntax is invalid')
        elif name == 'password':
            if not bool(password_pattern.match(item)):
                raise AssertionError('password syntax is invalid')
        elif name == 'security question' or name == 'security answer':
            validate_security_question_or_answer(name, item)

    def get_my_posts(self):
        my_posts = []
        for post in posts_list:
            if post.user_id == self.id:
                my_posts.append(post)

        return my_posts

    @property
    def my_post_count(self):
        return len(self.get_my_posts())

    @property
    def serialize(self):
        return {'email': self.email}

    @property
    def __name__(self):
        return self.__class__.__name__
