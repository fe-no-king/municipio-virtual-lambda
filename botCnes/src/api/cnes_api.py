import requests
import os

from utils.format_date import format_date

def list(code, competence):

    id_cnes = f"310400{code}"
    competence = format_date(competence, '%Y-%m')
    competence = competence.replace("-", "")

    cnes = response = requests.get(f'https://cnes.datasus.gov.br/services/estabelecimentos-profissionais/{id_cnes}?competencia={competence}', headers={
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'cnes.datasus.gov.br',
        'Pragma': 'no-cache',
        'Referer': 'https://cnes.datasus.gov.br/pages/profissionais/consulta.jsp',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"'
    })

    return cnes.json()
