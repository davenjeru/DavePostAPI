# DavePostAPI [![Build Status](https://travis-ci.org/davenmathews/DavePostAPI.svg?branch=master)](https://travis-ci.org/davenmathews/DavePostAPI) [![Coverage Status](https://coveralls.io/repos/github/davenmathews/DavePostAPI/badge.svg?branch=master)](https://coveralls.io/github/davenmathews/DavePostAPI?branch=master) [![Maintainability](https://api.codeclimate.com/v1/badges/cfa462a966f1e327e582/maintainability)](https://codeclimate.com/github/davenmathews/DavePostAPI/maintainability)

## Motivation
Practice for API development and deployment using TDD

## Tech/Framework used
**Built with:**
1. Python 3.6
2. Flask

## To install and test this project:
#### Prerequisites:
1. Should have python 3.6 installed
2. Should have `pip`
3. Should have `virtualenv`

#### Set up:
1. Clone this repository.
2. Create a virtual environment for the project
    
    `virtualenv venv` 
    
    '**venv**' is the name of your folder. You can name it any way you please.
3. Install the requirements.txt

    `pip install -r requirements.txt`
4. Activate the virtual environment.

    `source venv/Scripts/activate`
    
    -There should be your virtual environment folder in parentheses
    
    `(venv)`
    
5.  Run **DavePostAPI.py**
    
    `python DavePostAPI.py`
    
5. Test the endpoints using Postman or using your browser at the endpoint /api/v1. This is where the documentation is located

#### Api endpoints
`POST api/v1/auth/register` User registration. Should register user if the email is not already in use

`POST api/v1/auth/login` User login. Should login if credentials given are valid

`GET api/v1/auth/logout` User logout.

`GET api/v1/posts` View all posts.

`GET api/v1/events/<int:post_id>` View details of a single post

`GET api/v1/users` View all users.

`GET api/v1/users/<int:user_id>` View a single user.

`GET api/v1/users/<int:user_id>/posts` View all posts that belong to a single user.

`POST api/v1/users/<int:user_id>/posts` User can add a post.

`DELETE api/v1/users/<int:user_id>/posts` User can batch delete all their posts.

`GET api/v1/users/<int:user_id>/posts/<int:post_id>` View single post via this user.

`PATCH api/v1/users/<int:user_id>/posts/<int:post_id>` User can modify this post.

`DELETE api/v1/users/<int:user_id>/posts/<int:post_id>` User can delete this post.
