import unittest

from davepostAPI.models.post_model import Post, PostTransactionError, posts_list
from davepostAPI.models.user_model import User, UserTransactionError, users_list


class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        users_list.clear()
        posts_list.clear()
        self.u = User('email@company.com', 'password.Pa55word', 'What is your favourite company?', 'company')
        self.p = self.u.create_post('My post title.', 'Something interesting for people to read')

    def tearDown(self):
        users_list.clear()
        posts_list.clear()

    def test_create_user_pass(self):
        self.assertEqual('email@company.com', self.u.email)
        self.assertTrue(self.u.authenticate('password.Pa55word'))

    def test_create_user_fail(self):
        try:
            User('email@com', 'password.Pa55word', 'What is your favourite company?', 'company')
        except UserTransactionError as e:
            self.assertEqual('email address syntax is invalid', e.msg)
        finally:
            self.assertRaises(UserTransactionError)

        try:
            User('email@company.com', 'password', 'What is your favourite company?', 'company')
        except UserTransactionError as e:
            self.assertEqual('password syntax is invalid', e.msg)
        finally:
            self.assertRaises(UserTransactionError)

        try:
            u = User('email@company.com', 'password.Pa55word', 'question', 'company')
        except UserTransactionError as e:
            self.assertEqual('security question must start with a \'Wh\' or a \'Are\' question', e.msg)
        finally:
            self.assertRaises(UserTransactionError)

    def test_user_reset_password(self):
        self.u.reset_password('What is your favourite company?', 'company', 'another.Pa55word')
        self.assertTrue(self.u.authenticate('another.Pa55word'))

    def test_user_creates_post_pass(self):
        self.assertIsInstance(self.p, Post)
        self.assertEqual('My post title.', self.p.title)
        self.assertEqual('Something interesting for people to read', self.p.body)

    def test_user_creates_post_fail(self):
        try:
            self.u.create_post('My post', 'Something interesting for people to read.')
        except PostTransactionError as e:
            self.assertEqual('title too short. Min of 10 characters allowed', e.msg)

        try:
            self.u.create_post('My post    p pp', 'Something interesting for people to read.')
        except PostTransactionError as e:
            self.assertEqual('Please check the spacing on your title', e.msg)

        try:
            self.u.create_post('My post..\'.\';.\'.;\'.', 'Something interesting for people to read.')
        except PostTransactionError as e:
            self.assertEqual('please check the punctuation in your title', e.msg)

    def test_user_updates_post_pass(self):
        self.u.update_post('title', 'My new post title', self.p)
        self.assertEqual('My new post title', self.p.title)

    def test_user_updates_post_fail(self):
        try:
            self.u.update_post('title', 'My post title.', self.p)
        except PostTransactionError as e:
            self.assertEqual('title given matches the previous title', e.msg)

        try:
            self.u.update_post('body', 'Something interesting for people to read', self.p)
        except PostTransactionError as e:
            self.assertEqual('body given matches the previous body', e.msg)

    def test_my_post_count(self):
        self.assertEqual(1, self.u.my_post_count)

    def test_user_deletes_post(self):
        self.u.delete_post(self.p)
        self.assertEqual([], self.u.get_my_posts())

    def test_serialize(self):
        self.assertEqual(dict(email='email@company.com'), self.u.serialize)
        self.assertDictContainsSubset(dict(title='My post title.'), self.p.serialize)


if __name__ == '__main__':
    unittest.main()
