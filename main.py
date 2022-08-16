"""
main.py
Adam Manning (C) 2022
"""
# Needed to import Logger correctly
import sys
sys.path.append("Logger")

import Logger.logger as log

from http.server import HTTPServer
from PokemonHTTPRequestHandler import PokemonHTTPRequestHandler

def main():
    """
    Program's main function
    """

    log.enable_logs()
    log.open_logs()

    log.log_info("Logger started")

    ip_address = "0.0.0.0"
    port_num = 8080

    log.log_debug(f"IP Address: {ip_address}")
    log.log_debug(f"Port #: {port_num}")

    listen = (ip_address, port_num)
    server = HTTPServer(listen, PokemonHTTPRequestHandler)

    log.log_info(f"Listening on {ip_address}:{port_num}")
    print(f"Listening on {ip_address}:{port_num}")

    server.serve_forever()

# Only start the server is the script is run as the main file
if __name__ == "__main__":
    main()
