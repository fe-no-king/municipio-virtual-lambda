import requests
import os

def login_api():
    login = requests.post(f"{os.getenv('ENDPOINT_API_MV')}/login", json={"username": os.getenv('USERNAME_MV'),"password": os.getenv('PASSWORD')})

    if login.status_code != 200:
        print("Login inválido:", login.status_code)
        exit()

    return login.json()