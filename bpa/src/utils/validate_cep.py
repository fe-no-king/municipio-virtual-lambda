def validate_cep(cep):

    if cep is None or not isinstance(cep, str):
        return False

    if len(cep) != 8:
        return False

    if not cep.isdigit():
        return False

    first_digit = int(cep[0])
    second_digit = int(cep[1])
    third_digit = int(cep[2])

    if first_digit == 0:
        return False

    if second_digit < 0 or second_digit > 9:
        return False

    if third_digit == 0 or third_digit == 1:
        return False

    return True