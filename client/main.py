import time
import os
import requests
from requests.exceptions import RequestException
import const
import json 
import base64


def command_checker(cmd, args):

    if cmd == "ingreso":
        if not args or len(args) != 2:
            print('Ingresa los argumentos: [Nro. de Cuenta] [Valor de la transaccion]')
            return
        ingreso(args[0],args[1])

    elif cmd == "transacciones":
        if not args or len(args) != 1:
            print("Ingresa los argumentos: [Nro. de Cuenta] ")
            return
        show(args[0])
    
    elif cmd == "eliminar":
        if not args or len(args) != 1:
            print("Ingresa los argumentos: [Nro. de Cuenta] ")
            return
        delete(args[0])
    else:
        print("El comando: "+cmd+" no está disponible")

def ingreso(key, value):
    
    try:
        
        data = json.dumps({ 'key': key, 'value': value })

        r = requests.post(
            f'{const.IP_SERVER}:{const.PORT}/transaccion/crear',
            data=data,
            headers={ 'content-type': 'application/json' }
        )


        if ('error' in json.loads(r.text)):
            raise ConnectionAbortedError
        
        print("Elemento ingresado a la DB")
    
    
    except Exception as err:
        print(f'{err}')


def delete(key):
    try:
        
        data = json.dumps({ 'key': key })
        r = requests.post(
            f'{const.IP_SERVER}:{const.PORT}/transaccion/borrar',
            data=data,
            headers={ 'content-type': 'application/json' }
        )

        if ('error' in json.loads(r.text)):
            raise ConnectionAbortedError
        
        print("Elemento eliminado")
            
    except Exception as err:
        print(f'{err}')

def show(key):
    try:
        r = requests.get(f'{const.IP_SERVER}:{const.PORT}/transacciones/consultar?key={key}')
        data = json.loads(r.text)['data']
            
        if 'error' in data:
            raise ConnectionAbortedError

        if len(data)==0:
            print("Este registro no existe en la BD")
        else:
            print(data)
    
    except Exception as err:
        print(f'{err}')


def main():

    user_input = ""

    try:
        while True:
            pwd = '[ConsolaDeComandos/TET/P1]'
            shell_input = " ".join(input(pwd + ' # ').split())
            user_input = []
            start = 0
            inQuotes = False
            for i in range(len(shell_input)):
                if shell_input[i] == '"' or shell_input[i] == "'":
                    inQuotes = not inQuotes

                if (shell_input[i] == ' ' or i == len(shell_input) - 1) and not inQuotes:
                    end = i + 1 if i == len(shell_input) - 1 else i
                    user_input.append(shell_input[start:end])
                    start = i + 1
                    inQuotes = False
            
            command = user_input[0]
            args = user_input[1:] if len(user_input) > 1 else []
            args = [arg.replace("'", "").replace('"', "") for arg in args]

            command_checker(command, args)
            
    except KeyboardInterrupt:
        print('\n\n[ConsolaDeComandose/TET/P1] # Saliendo...\n')

if __name__ == '__main__':
    main()
