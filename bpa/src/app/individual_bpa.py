from src.api.medical_care_api import list as medical_care

from src.utils.validate_cns import validate_cns
from src.utils.format_date import format_date
from src.utils.format_date import format_date_month
from src.utils.format_date import date_month_format
from src.utils.format_date import format_date_br
from src.utils.format_date import calculate_age
from src.utils.accents import remove_accents

from src.api.service_units_api import list_current as service_units
from src.api.login_api import login_api
from src.utils.validate_cep import validate_cep
from src.utils.tab_file import line_mount
from src.api.medical_care_api import update_path

import tempfile
import random
import string
import boto3
import os

def main(IdBpaIndividual):

    s3 = boto3.client('s3')

    tmp_dir = tempfile.gettempdir()

    login = login_api()
    access_token = login.get('access_token', None)

    body = mount_body(access_token, IdBpaIndividual)
    bpa_data = body.get('bpa_data')

    competence = bpa_data.get('competence')
    month, year = competence.split('/')
    month = month.upper()

    date_month = date_month_format(bpa_data.get('competence'))

    unit = bpa_data.get('unit')
    unit = unit.upper()
    unit = unit.replace(' ', '')

    header = mount_header({
        'competence': bpa_data.get('competence'), 
        'body_lines': body.get('total'), 
        'sheets_total': body.get('sheets_total'), 
        'control_field': body.get('control_field'), 
        'organ': bpa_data.get('organ_name'),
        'organ_acronym':'310400',
        'cgc_cpf': bpa_data.get('organ_cnpj'),
        'secretary_name': bpa_data.get('organ_secretary_name'),
        'version': bpa_data.get('version'),
    })

    length = 10
    allowed_characters = string.ascii_letters + string.digits
    file_name = ''.join(random.choice(allowed_characters) for _ in range(length))

    file_path = f"bpa_individua/{IdBpaIndividual}/PAMVS{unit}{date_month}.{month}"
    file_tmp = os.path.join(tmp_dir, file_name)

    with open(file_tmp, 'w') as file:
        file.write(header)
        file.write(body.get('data'))

    s3.upload_file(file_tmp, os.getenv('AWS_BUCKET'), file_path)

    s3.put_object_acl(
        ACL='public-read',
        Bucket=os.getenv('AWS_BUCKET'),
        Key=file_path
    )

    update_path(access_token, IdBpaIndividual, {
        "path": file_path,
    })

    os.remove(file_tmp)
    

def mount_header(data):

    return line_mount({
        'number': 1,
        'length': 127,
        'data': [
            {'length': 2, 'text': '01'},
            {'length': 5, 'text': '#BPA#'},
            {'length': 6, 'text': format_date_month(data.get('competence'))},
            {'length': 6, 'text': data.get('body_lines')+1, 'complete': '0', 'position': 'left'},
            {'length': 6, 'text': data.get('sheets_total'), 'complete': '0', 'position': 'left'},
            {'length': 4, 'text': data.get('control_field'), 'complete': '0', 'position': 'left'},
            {'length': 30, 'text': remove_accents(data.get('organ')), 'complete': ' ', 'position': 'right'},
            {'length': 6, 'text': remove_accents(data.get('organ_acronym')), 'complete': ' ', 'position': 'right'},
            {'length': 14, 'text': data.get('cgc_cpf')}, #CGC/CPF do prestador ou do órgão público
            {'length': 40, 'text': remove_accents(data.get('secretary_name')), 'complete': ' ', 'position': 'right'}, # Nome do órgão de saúde destino do arquivo
            {'length': 1, 'text': 'M'},
            {'length': 10, 'text': data.get('version')}
        ]
    })

def mount_body(access_token, IdBpaIndividual):

    i = 0
    body = ''
    count=0
    number_sheet=0
    number_sheet_line=0
    while True:
        i += 1

        medical_care_data = medical_care(access_token, IdBpaIndividual, {}, i)
        bpa_data = medical_care_data.get('bpa')
        medical_care_data = medical_care_data.get('appointments')
        total = medical_care_data.get('total', 0)

        if total > 0:
            data = medical_care_data.get('data', [])
            doctor_cns_current = None
            for val in data:

                if validate_cns(val.get('doctor_cns')) == True and validate_cns(val.get('patient_cns')) == True:
                    count+=1
                    number_sheet_line+=1

                    competence = format_date_month(bpa_data.get('competence'))

                    date_procedure = format_date(val.get('created_at'), "%Y-%m-%d")
                    date_procedure = date_procedure.replace('-', "")

                    patient_sex = val.get('patient_sex')
                    patient_sex = patient_sex.upper()

                    patient_date_birth = format_date(val.get('patient_date_birth'), "%Y-%m-%d")
                    patient_date_birth = patient_date_birth.replace('-', "")

                    breed = val.get('patient_breed')
                    breed_down = '01'
                    if breed == 'n':
                        breed_down = '02'
                    elif breed == 'p':
                        breed_down = '03'
                    elif breed == 'a':
                        breed_down = '04'
                    elif breed == 'i':
                        breed_down = '09'

                    patient_zip_code = str(val.get('patient_zip_code', '38180081'))
            
                    if validate_cep(patient_zip_code) == False:
                        patient_zip_code = '38180081'
            
                    street_code = patient_zip_code[-3:]

                    if doctor_cns_current != val.get('doctor_cns'):
                        number_sheet+=1
                        number_sheet_line=1

                    if number_sheet_line > 20:
                        number_sheet+=1
                        number_sheet_line=1

                    doctor_cns_current = val.get('doctor_cns')

                    body += line_mount({
                        'number': count+1,
                        'length': 339,
                        'data': [
                            {'length': 2, 'text': '03'}, # default
                            {'length': 7, 'text': bpa_data.get('code'), 'complete': '0', 'position': 'left'}, # cnes
                            {'length': 6, 'text': competence}, # competencia
                            {'length': 15, 'text': val.get('doctor_cns')}, # cns doctor
                            {'length': 6, 'text': val.get('doctor_cbo')}, # cbo
                            {'length': 8, 'text': date_procedure}, # date procedure
                            {'length': 3, 'text': number_sheet, 'complete': '0', 'position': 'left'}, # numero folha
                            {'length': 2, 'text': number_sheet_line, 'complete': '0', 'position': 'left'}, # numero registro folha
                            {'length': 10, 'text': val.get('code_procedure')}, # numero do procedimento
                            {'length': 15, 'text': val.get('patient_cns')}, # cns paciente
                            {'length': 1, 'text': val.get('patient_sex').upper()}, # sexo paciente
                            {'length': 6, 'text': '310400'}, # CODE Municipio IBGE
                            {'length': 4, 'text': val.get('cid_10', 'Z00')}, # CID 10
                            {'length': 3, 'text': calculate_age(val.get('patient_date_birth')), 'complete': '0', 'position': 'left'}, # Idade paciente
                            {'length': 6, 'text': '000001'}, # QUANTIDADE DE PROCEDIMENTO
                            {'length': 2, 'text': '02'}, # CARATER DO ATENDIMENTO
                            {'length': 13, 'text': '             '}, # NUMERO DA AUTORIZAÇÂO
                            {'length': 3, 'text': 'BPA'}, # ORIGEM
                            {'length': 30, 'text': remove_accents(val.get('patient_name', '')), 'complete': ' ', 'position': 'right'}, # NOME PACIENTE
                            {'length': 8, 'text': patient_date_birth}, # DATA DE NACIMENTO
                            {'length': 2, 'text': breed_down}, # RAÇA COR
                            {'length': 4, 'text': '    '}, # ETINIA
                            {'length': 3, 'text': '010'}, # NACIONALIDADE
                            {'length': 3, 'text': '   '}, # CODIGO DO SERVIÇO
                            {'length': 3, 'text': '   '}, # CODIGO DA CLASSIFICAÇÃO
                            {'length': 8, 'text': '        '}, # CODIGO DA Sequencia da Equipe
                            {'length': 4, 'text': '    '}, # CODIGO DA Area da Equipe
                            {'length': 14, 'text': '              '},# Código do CNPJ, conforme cadastro na Receita Federal da empresa que realizou a manutenção ou adaptação da OPM
                            {'length': 8, 'text': patient_zip_code}, # CEP PACIENTE
                            {'length': 3, 'text': street_code},
                            {'length': 30, 'text': remove_accents(val.get('patient_address', 'VAZIO')), 'complete': ' ', 'position': 'right'}, # PACIENTE ADDRESS
                            {'length': 10, 'text': remove_accents(val.get('patient_complement', '')), 'complete': ' ', 'position': 'right'}, # PACIENTE ADDRESS COMPLEMENTO
                            {'length': 5, 'text': val.get('patient_number', 'SN'), 'complete': ' ', 'position': 'right'}, # PACIENTE NUMBER
                            {'length': 30, 'text': remove_accents(val.get('patient_district', '')), 'complete': ' ', 'position': 'right'}, # PACIENTE District
                            {'length': 11, 'text': '', 'complete': ' ', 'position': 'right'}, # PACIENTE PHONE
                            {'length': 40, 'text': '', 'complete': ' ', 'position': 'right'}, # PACIENTE EMAIL
                            {'length': 10, 'text': '', 'complete': ' ', 'position': 'right'}, # Indentificação nacional de equipes
                        ]
                    })
        
        if medical_care_data.get('next_page_url') is None:
            break

    return {'data': body, 'total':count, 'bpa_data':bpa_data, 'sheets_total':50, 'control_field': calculate_control_field([{"code": 3010100072, "quantity": count}])}

def calculate_control_field(procedures):
    sum_of_remainders = 0

    for proc in procedures:

        code_sum = (int(proc["code"]) * int(proc["quantity"])) + int(proc["quantity"])
        remainder = code_sum % 1111
        sum_of_remainders += remainder


    control_field = sum_of_remainders + 1111
    
    return control_field

