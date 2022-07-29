# pylint: disable=invalid-name
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

from http.server import HTTPServer
from PokemonHTTPRequestHandler import PokemonHTTPRequestHandler

def main():
    ip = "0.0.0.0"
    port = 8080

    listen = (ip, port)

    server = HTTPServer(listen, PokemonHTTPRequestHandler)

    print(f"Listening on {ip}:{port}")

    server.serve_forever()

# Only start the server is the script is run as the main file
if __name__ == "__main__":
    main()
