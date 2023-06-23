import requests
import os

def list(access_token):

    response = requests.get(f"{os.getenv('ENDPOINT_API_MV')}/service-units-current", None, headers={'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'})

    if response.status_code != 200:
        print("Invalid token:", response.status_code)
        exit()

    return response.json()

def list_current(access_token, IdServiceUnits):

    response = requests.get(f"{os.getenv('ENDPOINT_API_MV')}/service-units-current/{IdServiceUnits}", None, headers={'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'})

    if response.status_code != 200:
        print("Invalid token:", response.status_code)
        exit()

    return response.json()