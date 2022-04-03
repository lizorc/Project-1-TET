from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import const
import requests
import json

def to_string(dict):
    return str(dict).replace("'", '"')

def response(server, code, response):
    server.send_response(code)
    server.send_header("content-type", "application/json")
    server.end_headers()
    server.wfile.write(bytes(to_string(response), const.ENCODING_FORMAT))  

def get_path(server):
    url = urlparse(server.path)
    path = url.path
    path = path[:-1] if path[-1] == '/' else path
    return path


class MyServer(BaseHTTPRequestHandler):

    # Método que recibe las peticiones GET del cliente (client.py)
    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)

        for k in query.keys():
            query[k] = query[k][0]


        if (path == '/transacciones/consultar'):
            if not 'key' in query:
                res = { "error": { "code": 400, "message": "No se encontró la key en el valor ingresado" } }
                response(self, 400, res)
                return
            
            else:

                key = query['key']
                
                try:
                    #Se define la petición al servidor de base de datos
                    hashval = hash(key)
                    if (hashval % 2 == 0):
                        url = const.DB1[0]
                    else:
                        url = const.DB1[1]
                    
                    r = requests.get(f'{url}/transacciones/consultar?key={key}')

                    res = { "data": json.loads(r.text)['data'] }
                    response(self, 202, res) 

                except requests.exceptions.RequestException as e:
                    res = { "error": { "code": 500, "message": "Internal Error: DB Server Connection Refused" } }
                    response(self, 500, res)

    # Método que recibe las peticiones POST del cliente (client.py)
    def do_POST(self):

        path = get_path(self)
        
        # Proceso en caso de que alguien quiera ingresar un nuevo valor
        if path == '/transaccion/crear':

            length = int(self.headers.get('content-length'))
            field_data = self.rfile.read(length)

            try:
                body = json.loads(field_data.decode('utf-8'))
            except:
                res = { "error": { "code": 400, "message": "Lo enviado no es un JSON" } }
                response(self, 400, res)
                return
            
            if not 'key' in body:
                res = { "error": { "code": 400, "message": "No existe la llave en la petición" } }
                response(self, 400, res)
                return
            elif not 'value' in body:
                res = { "error": { "code": 400, "message": "No existe el valor en la petición" } }
                response(self, 400, res)
                return

            else:

                key = body['key']
                value = body['value']
                
                #Se define donde se va guardar el registro según su hash
                try:
                    hashval = hash(key)
                    if hashval % 2 == 0:
                        url = const.DB1[0]
                    else: 
                        url = const.DB1[1]
                    
                    data = json.dumps({'key':key, 'value':value})
                    r = requests.post(f'{url}/transaccion/crear',data=data,headers={'content-type':'application/json'})
                    res = { "status": { "code": 202, "message": "Accepted" } }
                    response(self, 202, res) 
                
                except requests.exceptions.RequestException as e:
                    res = { "error": { "code": 500, "message": "Internal Error: DB Server Connection Refused" } }
                    response(self, 500, res)
        
        # Proceso en caso de que alguien quiera borrar un registro
        elif path == "/transaccion/borrar":

            length = int(self.headers.get('content-length'))
            field_data = self.rfile.read(length)
            try:
                body = json.loads(field_data.decode('utf-8'))
            except:
                res = { "error": { "code": 400, "message": "Bad format for JSON" } }
                response(self, 400, res)
                return

            if not 'key' in body:
                res = { "error": { "code": 400, "message": "Missing [key] in body" } }
                response(self, 400, res)
                return
            
            else:

                key = body['key']
                try:

                    data = json.dumps({ 'key': key })

                    for ip in const.DB1:
                        r = requests.post(
                            f'{ip}/transaccion/borrar',
                            data=data,
                            headers={ 'content-type': 'application/json' }
                        )

                    res = { "status": { "code": 202, "message": "Accepted" } }
                    response(self, 202, res) 
                except requests.exceptions.RequestException as e:
                    res = { "error": { "code": 500, "message": "Internal Error: DB Server Connection Refused" } }
                    response(self, 500, res)       

        else:
            res = { "error": { "code": 404, "message": "Resource not found" } }
            response(self, 404, res)

if __name__ == "__main__":
    webServer = HTTPServer((const.IP_SERVER, const.PORT), MyServer)
    print("Servidor iniciado en:  http://%s:%s" % (const.IP_SERVER, const.PORT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Deteniendo servidor principal")
