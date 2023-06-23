from unidecode import unidecode

def remove_accents(text):
    return unidecode(text)