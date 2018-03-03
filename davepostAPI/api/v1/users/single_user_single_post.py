from flask import redirect
from flask_login import current_user, login_required
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from davepostAPI.api.v1.boilerplate import check_id_availability, PayloadExtractionError, get_validated_payload, \
    extract_from_payload, generate_post_output
from davepostAPI.api.v1.posts import SinglePost
from davepostAPI.api.v1.users.single_user_all_posts import post_model
from davepostAPI.models import users_list, User, posts_list, Post, PostTransactionError

users_ns = Namespace('users')


class SingleUserSinglePost(Resource):
    def get(self, user_id: int, post_id: int):
        """
        View a single post from a specific user
        """
        try:
            check_id_availability(user_id, users_list, str(User.__name__))
            check_id_availability(post_id, posts_list, str(Post.__name__))
        except PayloadExtractionError as e:
            users_ns.abort(e.abort_code, e.msg)

        for post in posts_list:
            if post.user_id == user_id and post.id == post_id:
                return redirect(self.api.url_for(SinglePost, post_id=post_id))
        else:
            users_ns.abort(400, 'the requested user does not own this post')

    @login_required
    @users_ns.expect(post_model)
    @users_ns.response(200, 'Post modified successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def patch(self, user_id: int, post_id: int):
        """
        Modify a post

        1. User should be logged in.
        2. Your title should have between 10 and 70 characters
        3. Your body should have between 40 and 500 characters
        4. Duplicate posts will not be created
        """

        if current_user.id != user_id:
            users_ns.abort(403)

        title, body, this_post, payload = None, None, None, None
        try:
            check_id_availability(user_id, users_list, str(User.__name__))
            this_post = check_id_availability(post_id, posts_list, str(Post.__name__))
            payload = get_validated_payload(self)
        except PayloadExtractionError as e:
            users_ns.abort(e.abort_code, e.msg)

        try:
            title = extract_from_payload(payload, ['title'])
            title = title[0]
        except PayloadExtractionError:
            pass

        try:
            body = extract_from_payload(payload, ['body'])
            body = body[0]
        except PayloadExtractionError:
            pass

        try:
            if title:
                this_post = current_user.update_post('title', title, this_post)
            if body:
                this_post = current_user.update_post('body', body, this_post)
        except PostTransactionError as e:
            users_ns.abort(e.abort_code, e.msg)

        response = self.api.make_response(generate_post_output(self, this_post, str(self.patch.__name__)), 200)
        response.headers['location'] = self.api.url_for(SingleUserSinglePost, user_id=user_id, post_id=post_id)

        return response

    @users_ns.response(204, 'Post deleted successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def delete(self, user_id: int, post_id: int):
        """
        Delete a post

        1. User needs to be logged in
        2. This deletes the post whose ID is specified on the url
        3. This process is irreversible
        """
        pass
