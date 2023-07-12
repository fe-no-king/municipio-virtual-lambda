import json

from src.main import main

def lambda_handler(event, context):

    main({'IdServiceUnits': event.get('IdServiceUnits'), 'IdBpaIndividual': event.get('IdBpaIndividual'), 'code': event.get('code'), 'competence': event.get('competence')})
