from http.server import BaseHTTPRequestHandler, HTTPServer
from game import Game
from action import Action
import json


class server():
    game = None

    class RequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            global game
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            print(data)
        
            action = data.get('action')
            if(action == 'launch'):
                print(data.get('players'))
                game = Game(data.get('players'))

            if(action == "action"):
                player_id = data.get("player_id")
                acts = data.get('acts')
                for act in acts:
                    name = acts.get("name")
                    kwargs = act.get("kwargs")
                    gameAction = Action(name, **kwargs)
                    game.Call(gameAction)

            
            if(action == 'print'):
                game.print()
                
                    
            

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = {'success': True}
            self.wfile.write(json.dumps(response).encode('utf-8'))

    def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print(f"Serveur démarré sur le port {port}")
        httpd.serve_forever()

server.run()