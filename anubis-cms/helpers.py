import os
import re
import platform

def clean_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def read_text(long_min=0, long_max=100, msg=None):
    if msg:
        print(msg)

    while True:
        text = input("> ")

        if len(text) >= long_min and len(text) <= long_max:
            return text
        else:
            print("DNI no valido, debe tener 8 numeros y 1 letra al final. Ejemplo: 12345678Z")

def dni_validate(dni, list_clients):
    # 8 numeros y 1 letra
    # 12345678Z
    if not re.match('[0-9]{8}[A-Z]$', dni): 
        print("DNI no valido, debe tener 8 numeros y 1 letra al final. Ejemplo: 12345678Z")
        return False
    
    for client in list_clients:
        if client.dni == dni:
            print("DNI ya existente")
            return False

    return True

