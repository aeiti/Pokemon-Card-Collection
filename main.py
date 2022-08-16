"""
main.py
Adam Manning (C) 2022
"""
# Needed to import Logger correctly
import sys
sys.path.append("Logger")

# import Logger.logger as log

from http.server import HTTPServer
from PokemonHTTPRequestHandler import PokemonHTTPRequestHandler

from Logger.logger import Logger

def main():
    """
    Program's main function
    """

    log = Logger()

    log.info("Logger started")

    ip_address = "0.0.0.0"
    port_num = 8080

    log.debug(f"IP Address: {ip_address}")
    log.debug(f"Port #: {port_num}")

    listen = (ip_address, port_num)
    server = HTTPServer(listen, PokemonHTTPRequestHandler)

    log.info(f"Listening on {ip_address}:{port_num}")
    print(f"Listening on {ip_address}:{port_num}")

    server.serve_forever()

# Only start the server is the script is run as the main file
if __name__ == "__main__":
    main()
