import configparser
import json
import random
import string

import requests

URL = 'http://127.0.0.1:8000'

domains = [
    "hotmail.com",
    "gmail.com",
    "aol.com",
    "mail.com",
    "mail.kz",
    "yahoo.com"
]
letters = string.ascii_lowercase[:12]


def get_random_domain(domains):
    return random.choice(domains)


def get_random_name(letters, length):
    return ''.join(random.choice(letters) for i in range(length))


def generate_random_email(length):
    return get_random_name(letters, length) + '@' + get_random_domain(domains)


def generate_random_username(length):
    return get_random_name(letters, length)


def generate_content():
    return ' '.join([get_random_name(letters, 8) for i in range(100)])


def create_user(username, email, password):
    url = "{url}/v1/user/signup/".format(url=URL)
    response = requests.post(
        url,
        data={'username': username, 'email': email, 'password': password}
    )
    return response.status_code == 201


def get_token(username, password):
    url = "{url}/v1/user/login/".format(url=URL)
    response = requests.post(
        url,
        data={'username': username, 'password': password}
    )
    if response.status_code == 200:
        return response.json()['token']


def create_post(content, token):
    url = "{url}/v1/post/".format(url=URL)
    response = requests.post(
        url,
        data={'content': content},
        headers={'Authorization': 'Bearer ' + token}
    )
    if response.status_code == 201:
        data = json.loads(response.text)
        return data['id']


def like_post(post_id, token):
    url = "{url}/v1/post/{post}/like/".format(url=URL, post=post_id)
    response = requests.get(url, headers={
        'Authorization': 'Bearer ' + token
    })
    return response.status_code == 201


def unlike_post(post_id, token):
    url = "{url}/v1/post/{post}/unlike/".format(url=URL, post=post_id)
    response = requests.get(url, headers={
        'Authorization': 'Bearer ' + token
    })
    return response.status_code == 201


number_of_users = 0
max_posts_per_user = 0
max_likes_per_user = 0
configfile = 'bot_configuration.txt'

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(configfile)

    number_of_users = config.getint('DEFAULT', 'number_of_users')
    max_posts_per_user = config.getint('DEFAULT', 'max_posts_per_user')
    max_likes_per_user = config.getint('DEFAULT', 'max_likes_per_user')

    password = 'aNe9Q!ih#*'

    usernames = [generate_random_username(7) for i in range(number_of_users)]

    [create_user(u, generate_random_email(7), password) for u in usernames]
    tokens = [get_token(username, password) for username in usernames]
    posts = []

    for token in tokens:
        if token:
            post_count = random.randint(0, max_posts_per_user)
            user_posts = [
                create_post(generate_content(), token)
                for i in range(post_count)
            ]
            posts.extend(user_posts)

    for token in tokens:
        likes_count = random.randint(0, max_likes_per_user)
        for i in range(likes_count):
            post_id = random.choice(posts)
            like_post(post_id, token)
