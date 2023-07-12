import json

from src.main import main

def lambda_handler(event, context):

    main(event.get('IdBpaIndividual'))
