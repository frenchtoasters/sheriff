import os
import requests
from behave import given, when, then
import json

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

@given('a valid recipient payload')
def step_impl(context):
    context.payload = {
        "discord_id": "bdd12345",
        "email": "bddtest@example.com"
    }

@when('I GET "{path}"')
def step_impl(context, path):
    url = f"{BASE_URL}{path}"
    response = requests.get(url)
    context.response = response

    if response.status_code >= 400:
        print(f"GET {url} failed with status {response.status_code}")
        print(f"Response body: {response.text}")

@when('I POST "{path}" with the payload')
def step_impl(context, path):
    url = f"{BASE_URL}{path}"
    response = requests.post(url, json=context.payload)
    context.response = response

    if response.status_code >= 400:
        print(f"POST {url} failed with status {response.status_code}")
        print(f"Response body: {response.text}")

@then('the response status code should be {status_code:d}')
def step_impl(context, status_code):
    assert context.response.status_code == status_code, f"Expected {status_code}, got {context.response.status_code}"

@then('the response should contain "{key}"')
def step_impl(context, key):
    try:
        json_data = context.response.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {context.response.text}"

    assert key in json_data, f"Key '{key}' not in response. Full response: {json_data}"

@then('the response JSON should be')
def step_impl(context):
    expected = json.loads(context.text)
    actual = context.response.json()
    assert actual == expected, f"Expected {expected}, got {actual}"

