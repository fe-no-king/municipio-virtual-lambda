from unidecode import unidecode

def remove_accents(text):
    
    if text is not None:
        return unidecode(text)