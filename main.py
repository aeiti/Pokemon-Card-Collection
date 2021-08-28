from http.server import HTTPServer
from PokemonHTTPRequestHandler import PokemonHTTPRequestHandler

def main():
    ip = "0.0.0.0"
    port = 8080

    listen = (ip, port)

    server = HTTPServer(listen, PokemonHTTPRequestHandler)

    print("Listening on {0}:{1}".format(ip, port))

    server.serve_forever()

# Only start the server is the script is run as the main file
if __name__ == "__main__":
    main()
