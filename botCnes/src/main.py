from dotenv import load_dotenv
import os

from api.login_api import login_api
from api.bpa_doctors_list_api import list as bpa_doctors_list_api
from api.bpa_doctors_list_api import update as update_doctors
from api.bpa_doctors_list_api import update_end
from api.cnes_api import list as cnes_api

from utils.validate_cns import validate_cns

# Load environment variables from the .env file
load_dotenv()

# Main function
def main(body):

    # Perform API login
    login = login_api()

    code = body.get('code')
    IdBpaIndividual = body.get('IdBpaIndividual')
    IdServiceUnits = body.get('IdServiceUnits')
    competence = body.get('competence')

    # token
    access_token = login.get('access_token', None)

    update_end(access_token, IdBpaIndividual, {
        "status": 'i'
    })

    try:
        cnes_data_json = cnes_api(code, competence)
        
        i = 0
        while True:
            i += 1
            
            # Perform API user not cnes 
            user_data = bpa_doctors_list_api(access_token, IdBpaIndividual, i)

            if user_data.get('total', 0) > 0:

                data = user_data.get('data', [])

                for val in data:
                    
                    IdUsersResponsible = val.get('IdUsersResponsible', None)
                    cns = val.get('cns', None)
                    total = val.get('total', 0)
                    
                    cbo = val.get('code', 0)
                    cbo_cnes = None
                    cnes = 'n'

                    if validate_cns(cns) == True:
                        
                        res_find_cnes = [item for item in cnes_data_json if item.get('cns') == cns]

                        if res_find_cnes:
                            for val_cnes in res_find_cnes:
                                cnes = 'y'
                                cbo_cnes = val_cnes.get('cbo')

                                if(cbo == val_cnes.get('cbo')):
                                    cbo_cnes = val_cnes.get('cbo')
                                    break

                    res = update_doctors(access_token, IdBpaIndividual, {
                        "IdServiceUnits": IdServiceUnits,
                        "IdUsersResponsible": IdUsersResponsible,
                        "code_cbo": cbo,
                        "code_cbo_cnes": cbo_cnes,
                        "cnes": cnes,
                        "total": total,
                    })
                        
            if user_data.get('next_page_url', None) is None:
                break

        update_end(access_token, IdBpaIndividual, {
            "status": 'a'
        })
        
    except Exception as e:
    
        update_end(access_token, IdBpaIndividual, {
            "status": 'e'
        })


main({'IdServiceUnits': 3, 'IdBpaIndividual': 5, 'code': '2165643', 'competence': '05-2023'})
