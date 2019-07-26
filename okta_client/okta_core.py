import os

import requests
from pprint import pprint

key = os.environ["OKTA_AUTH"]
api_url = os.environ["OKTA_URL"]


def get_okta(url_extention):
    url = f"{api_url}{url_extention}"
    return requests.get(url, headers={'Accept': 'application/json', 'authorization': key})


def put_okta(url_extention):
    url = f"{api_url}{url_extention}"
    return requests.put(url, headers={'Accept': 'application/json', 'authorization': key})


def next_page(page_url):
    users = get_okta(page_url)
    users_header = users.headers
    links = users_header['Link']
    if 'next' in links:
        cursor = links.split('rel="self", <')[1].split('>;')[0]
        next_page_url = cursor.split(api_url)[1]
    else:
        next_page_url = None

    return users, next_page_url


def all_users():
    """All users excludes deactivated users"""
    first_page = get_okta("users")
    users_header = first_page.headers
    cursor = users_header['Link'].split('rel="self", <')[1].split('>;')[0]
    next_page_url = cursor.split(api_url)[1]

    users_data = first_page.json()
    pprint(users_data)

    next = True

    while next:
        get_next_page = next_page(next_page_url)
        users_data = get_next_page[0].json()
        pprint(users_data)
        next_page_url = get_next_page[1]
        if not next_page_url:
            next = False
            print("the end")

