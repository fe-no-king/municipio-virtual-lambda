import requests
import os

def list(access_token, IdBpaIndividual, data, page=1):

    response = requests.post(f"{os.getenv('ENDPOINT_API_MV')}/medical-care-bpa/{IdBpaIndividual}?page={page}", json=data, headers={'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'})

    if response.status_code != 200:
        print("Invalid token:", response.status_code)
        exit()

    return response.json()

def update_path(access_token, IdBpaIndividual, data):

    response = requests.post(f"{os.getenv('ENDPOINT_API_MV')}/bpa/update-file-path/{IdBpaIndividual}", json=data, headers={'Authorization': f'Bearer {access_token}','Content-Type': 'application/json'})
    if response.status_code != 200:
        print("4Invalid token file:", response.text)

    return response.json()