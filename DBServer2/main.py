from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import const
import os.path
import json

def to_string(dict):
    return str(dict).replace("'", '"')

def response(server, code, response):
    server.send_response(code)
    server.send_header("content-type", "application/json")
    server.end_headers()
    server.wfile.write(bytes(to_string(response), 'utf-8'))  

def get_path(server):
    url = urlparse(server.path)
    path = url.path
    path = path[:-1] if path[-1] == '/' else path
    return path

class DB(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)

        for k in query.keys():
            query[k] = query[k][0]

        if path == '':
            res = { "response": { "code": 200, "message": "Conectado" } }
            response(self, 200, res)

        elif path == '/transacciones/consultar':
            if len(query) < 1 or not ('key' in query):
                res = { "error": { "code": 400, "message": "No existe key en la petición" } }
                response(self,400,res)
                return

            f = open('./DBServer2/database.txt','r')
            database = json.load(f)
            values = [d['value'] for d in database if d['key'] == query['key']]
            res = {"data":values}
            response(self,200,res)

        else:
            res = { "error": { "code": 404, "message": "Recurso no encontrado" } }
            response(self, 404, res)

    def do_POST(self):
        path = get_path(self)
        print(os.path)
        if path == '/transaccion/crear':
            length = int(self.headers.get('content-length'))
            field_data = self.rfile.read(length)

            try:
                entry = json.loads(field_data.decode('utf-8'))
            except:
                res = { "error": { "code": 400, "message": "Esto no es un JSON" } }
                response(self, 400, res)
                return
            
            if not os.path.exists('./DBServer2/database.txt'):
                f = open('./DBServer2/database.txt','x')
                f.write('[]')
                f.close()

            f = open('./DBServer2/database.txt','r')
            data = json.load(f)
            
            if isinstance(entry,list):
                data.append([e for e in entry])
            else:
                data.append(entry)

            f = open('./DBServer2/database.txt','w')
            json.dump(data,f)
            f.close()

            res = { "data": data }
            response(self, 201, res)

        elif path == "/transaccion/borrar":
            
            print("entra")
            length = int(self.headers.get('content-length'))
            field_data = self.rfile.read(length)
            try:
                entry = json.loads(field_data.decode('utf-8'))
            except:
                res = { "error": { "code": 404, "message": "Esto no es un JSON" } }
                response(self, 404, res)
                return

            f = open('./DBServer2/database.txt', 'r')
            database = json.load(f)
            deleted = [d for d in database if d['key'] == entry['key']]
            data = [d for d in database if d['key'] != entry['key']]
            
            f = open('./DBServer2/database.txt', 'w')
            json.dump(data, f)
            f.close()

            if len(deleted) == 0:
                res = { "error": { "code": 404, "message": "Llave no encontrada" } }
                response(self, 404, res)
                return

            res = { "data": deleted }
            response(self, 200, res)

        else:
            res = { "error": { "code": 404, "message": "Recurso no encontrado" } }
            response(self, 404, res)

if __name__ == "__main__":
    webServer = HTTPServer((const.IP_SERVER, const.PORT), DB)
    print("Servidor iniciado en: http://%s:%s" % (const.IP_SERVER, const.PORT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Deteniendo DB2")
