import datetime
import string

posts_list = []


class PostTransactionError(BaseException):
    def __init__(self, msg):
        self.msg = msg


class Post(object):
    id = 1

    def __init__(self, user, title: str, body: str):
        self.id = Post.id
        self.user_id = user.id

        try:
            self.__validate_post_details('title', title)
            self.__validate_post_details('body', body)
        except AssertionError as a:
            raise PostTransactionError(a.args[0])

        for post in posts_list:
            if post.title == title and post.body == body:
                raise PostTransactionError('similar post exists')

        self.title = title
        self.body = body
        self.created_on = datetime.datetime.now()
        self.last_modified = None
        self.__save()

    @staticmethod
    def __validate_post_details(name: str, item: str):
        """
            Used to validate title or body depending on the context given
            :param name: the context of validation
            :param item: item to be validated

        """
        max_length, min_length = None, None

        if name == 'title':
            max_length = 70
            min_length = 10
        elif name == 'body':
            max_length = 500
            min_length = 40
        if len(item) > max_length:
            raise AssertionError('{0} too long. Max of {1} characters allowed'.format(name, max_length))
        if len(item) < min_length:
            raise AssertionError('{0} too short. Min of {1} characters allowed'.format(name, min_length))

        if item[0] not in list(string.ascii_letters) + list(string.digits) + ['\'', '\"', '(']:
            raise AssertionError('please enter a valid {}'.format(name))

        if str(item[-1]) not in list(string.ascii_letters) + list(string.digits) + list('\'\").?!'):
            raise AssertionError('please enter a valid {}'.format(name))

        item_words = item.split(' ')

        for word in item_words:
            if not word:
                raise AssertionError('Please check the spacing on your {}'.format(name))

        for word in item_words:
            if word.count('.') > 3:
                raise AssertionError('please check the punctuation in your {}'.format(name))

            char_list = list(word)
            for i in range(len(char_list) - 1):
                if char_list[i] in string.punctuation and char_list[i] != '.':
                    if char_list[i] in ['!', '?', '.'] and char_list[i + 1] in ['\'', '\"']:
                        continue
                    if char_list[i + 1] in string.punctuation and char_list[i] != '.':
                        raise AssertionError('please check the punctuation in your {}'.format(name))

    def __save(self):
        Post.id += 1
        posts_list.append(self)

    def update(self, user, name: str, new_item: str):
        if user.id != self.user_id:
            raise PostTransactionError('this post does not belong to the selected user')

        if name == 'title':
            self.__validate_post_details(name, new_item)
            if self.title == new_item:
                raise PostTransactionError('{0} given matches the previous {0}'.format(name))
        elif name == 'body':
            self.__validate_post_details(name, new_item)
            if self.body == new_item:
                raise PostTransactionError('{0} given matches the previous {0}'.format(name))

        for post in posts_list:
            if name == 'title' and post.title == new_item or name == 'body' and post.body == new_item:
                raise PostTransactionError('similar {} exists'.format(name))

        self.title = new_item if name == 'title' else self.title
        self.body = new_item if name == 'body' else self.body

        self.last_modified = datetime.datetime.now()
        return self

    def delete(self, user):
        if user.id != self.user_id:
            raise PostTransactionError('this post does not belong to the selected user')

        posts_list.remove(self)
        del self
        return True

    @property
    def serialize(self):
        return dict(title=self.title, body=self.body, created_on=str(self.created_on),
                    last_modified=str(self.last_modified))

    @property
    def __name__(self):
        return self.__class__.__name__
