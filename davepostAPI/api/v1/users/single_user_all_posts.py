from flask import url_for
from flask_login import login_required, current_user
from flask_restplus import Resource, fields
from flask_restplus.namespace import Namespace

from davepostAPI.api.v1.boilerplate import check_id_availability, PayloadExtractionError, extract_from_payload, \
    get_validated_payload, generate_post_output
from davepostAPI.models import users_list, User, posts_list, PostTransactionError

users_ns = Namespace('users')
post_model = users_ns.model('post_model', {
    'title': fields.String(title='The title of your post', required=True,
                           example='My Post Title'),
    'body': fields.String(title='The body of your post', required=True,
                          example='Something interesting for people to read.')
})


class SingleUserAllPosts(Resource):
    @users_ns.response(200, "Success")
    @users_ns.response(400, "Post not found. Invalid 'post_id' provided")
    def get(self, user_id: int):
        """
        View all posts from a single user
        """
        this_user = None
        try:
            this_user = check_id_availability(user_id, users_list, str(User.__name__))
        except PayloadExtractionError as e:
            users_ns.abort(e.abort_code, e.msg)
        my_posts_list = this_user.get_my_posts()
        my_posts_list_output = []
        for a_post in my_posts_list:
            my_posts_list_output.append(a_post.serialize)
        return dict(posts=my_posts_list_output)

    @login_required
    @users_ns.expect(post_model)
    @users_ns.response(201, 'Post created successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def post(self, user_id: int):
        """
        Add a post

        1. User must be logged in to create a post
        2. Your title should have between 10 and 70 characters
        3. Your body should have between 40 and 500 characters
        4. Duplicate posts will not be created

        """
        try:
            check_id_availability(user_id, users_list, str(User.__name__))
        except PayloadExtractionError as e:
            users_ns.abort(e.abort_code, e.msg)

        if current_user.id != user_id:
            users_ns.abort(403)

        title, body = None, None

        try:
            payload = get_validated_payload(self)
            list_of_names = ['title', 'body']
            title, body = extract_from_payload(payload, list_of_names)
        except PayloadExtractionError as e:
            users_ns.abort(e.abort_code, e.msg)

        for a_post in posts_list:
            if a_post.title == title and a_post.body == body:
                users_ns.abort(400, 'post already exists')

        post = None
        try:
            post = current_user.create_post(title, body)
        except PostTransactionError as e:
            users_ns.add_model(e.abort_code, e.msg)
        output = generate_post_output(self, post, 'post')
        response = self.api.make_response(output, 201)
        response.headers['location'] = url_for(self.api.endpoint('users_single_user_single_post'),
                                               user_id=post.user_id, post_id=post.id)
        return response

    @login_required
    @users_ns.response(204, 'Post deleted successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def delete(self, user_id: int):
        """
        Batch delete all user's posts

        1. User must be logged in to delete all their posts
        2. This deletes all posts that a user has created
        3. This process os of course irreversible
        """
        check_id_availability(user_id, users_list, str(User.__name__))

        if current_user.id != user_id:
            users_ns.abort(403)

        my_posts_list = current_user.get_my_posts()

        for a_post in my_posts_list:
            try:
                current_user.delete_post(a_post)
            except PostTransactionError as e:
                users_ns.abort(e.abort_code, e.msg)

        return None, 204
