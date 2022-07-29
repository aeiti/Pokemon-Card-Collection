"""
main.py
Adam Manning (C) 2022
"""

from http.server import HTTPServer
from PokemonHTTPRequestHandler import PokemonHTTPRequestHandler

def main():
    """
    Program's main function
    """

    ip_address = "0.0.0.0"
    port_num = 8080

    listen = (ip_address, port_num)

    server = HTTPServer(listen, PokemonHTTPRequestHandler)

    print(f"Listening on {ip_address}:{port_num}")

    server.serve_forever()

# Only start the server is the script is run as the main file
if __name__ == "__main__":
    main()
