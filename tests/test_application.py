import pytest
import requests
import json

# тест на создание пользователя и проверку успешного создания
def test_create_user():
    user = {"name": "Fred", "address": "Moscow25", "coffee_id":"1", "has_sale": "1"}
    url = "http://localhost/add_user"
    r = requests.post(url, data=user)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == 201

def test_find_user_by_country():
    example_user = json.dumps({"name": "Fred", "address": "Moscow25", "coffee_id":"1", "has_sale": "1"})
    url = "http://localhost/users_by_country"
    country = json.dumps({"country": "Moscow25"})
    r = requests.get(url, country)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    user = json.loads(r.data)
    assert example_user == user