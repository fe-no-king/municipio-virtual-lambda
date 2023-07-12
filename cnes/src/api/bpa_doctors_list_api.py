import requests
import base64
import os

from src.utils.base64_encode import base64_encode

def list(access_token, IdBpaIndividual, page=1):

    response = requests.get(f"{os.getenv('ENDPOINT_API_MV')}/bpa/doctors-list/{IdBpaIndividual}?page={page}", None, headers={'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'})
    if response.status_code != 200:
        print("1Invalid token:", response.status_code)
        exit()

    return response.json()

def update(access_token, IdBpaIndividual, data):

    response = requests.post(f"{os.getenv('ENDPOINT_API_MV')}/bpa/doctors-update/{IdBpaIndividual}", json=data, headers={'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'})
    if response.status_code != 200:
        print("2Invalid token:", response.text)

    return response.json()

def update_end(access_token, IdBpaIndividual, data):

    response = requests.post(f"{os.getenv('ENDPOINT_API_MV')}/bpa/update-final/{IdBpaIndividual}", json=data, headers={'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'})
    if response.status_code != 200:
        print("3Invalid token:", response.text)

    return response.json()