import re

def validate_cns(cns):

    cns = str(cns)

    if not re.match(r'^\d+$', cns):
        return False

    if len(cns.strip()) != 15:
        return False

    if cns.startswith(('1', '2')):
        pis = cns[:11]
        soma = (int(pis[0]) * 15) + (int(pis[1]) * 14) + (int(pis[2]) * 13) + (int(pis[3]) * 12) + \
               (int(pis[4]) * 11) + (int(pis[5]) * 10) + (int(pis[6]) * 9) + (int(pis[7]) * 8) + \
               (int(pis[8]) * 7) + (int(pis[9]) * 6) + (int(pis[10]) * 5)

        resto = soma % 11
        dv = 11 - resto if resto != 0 else 0

        if dv == 10:
            soma = (int(pis[0]) * 15) + (int(pis[1]) * 14) + (int(pis[2]) * 13) + (int(pis[3]) * 12) + \
                   (int(pis[4]) * 11) + (int(pis[5]) * 10) + (int(pis[6]) * 9) + (int(pis[7]) * 8) + \
                   (int(pis[8]) * 7) + (int(pis[9]) * 6) + (int(pis[10]) * 5) + 2

            resto = soma % 11
            dv = 11 - resto

        resultado = pis + "001" + str(int(dv))
        if cns != resultado:
            return False

    elif cns.startswith(('7', '8', '9')):
        soma = (int(cns[0]) * 15) + (int(cns[1]) * 14) + (int(cns[2]) * 13) + (int(cns[3]) * 12) + \
               (int(cns[4]) * 11) + (int(cns[5]) * 10) + (int(cns[6]) * 9) + (int(cns[7]) * 8) + \
               (int(cns[8]) * 7) + (int(cns[9]) * 6) + (int(cns[10]) * 5) + (int(cns[11]) * 4) + \
               (int(cns[12]) * 3) + (int(cns[13]) * 2) + (int(cns[14]) * 1)

        resto = soma % 11
        if resto != 0:
            return False

    else:
        return False

    return True