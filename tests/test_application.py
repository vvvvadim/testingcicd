import pytest
import requests
import json

# тест на создание пользователя и проверку успешного создания
def test_create_user():
    user = json.dumps({"name": "Fred", "address":{ "country": "Moscow25" }, "coffee_id":"1", "has_sale": "1"})
    url = "http://localhost:8000/add_user"
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=user)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    assert r.status_code == 201

def test_find_user_by_country():
    example_user = json.dumps({"name": "Fred", "address":{ "country": "Moscow25" }, "coffee_id":"1", "has_sale": "1"})
    url = "http://localhost:8000/users_by_country"
    country = json.dumps({"country": "Moscow25"})
    headers = {'Content-Type': 'application/json'}
    r = requests.get(url,headers=headers ,data=country)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print('ERROR: %s' % e)
    user = r.json()
    assert example_user == user[0]