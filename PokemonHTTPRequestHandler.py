"""
PokemonHTTPRequestHandler.py
Adam Manning (C) 2021
"""

from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

import json

import Logger.logger as log

from DBController import DBController


num_requests = 0

# Headers
HEADER_CONTENT_TYPE = "Content-Type"
HEADER_CORS = "Access-Control-Allow-Origin"

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_HTML = "text/html"

UTF8 = "utf-8"

ERR = "err/{0}.html"
ERR_404 = ERR.format(404)

OUTPUT_MODE = "verbose"

# String constants
STR_GET = "GET"
STR_POST = "POST"
STR_PUT = "PUT"
STR_DELETE = "DELETE"
STR_PATCH = "PATCH"
STR_COPY = "COPY"
STR_HEAD = "HEAD"
STR_OPTIONS = "OPTIONS"
STR_LINK = "LINK"
STR_UNLINK = "UNLINK"
STR_PURGE = "PURGE"
STR_LOCK = "LOCK"
STR_UNLOCK = "UNLOCK"
STR_PROPFIND = "PROPFIND"
STR_VIEW = "VIEW"

STR_REQ_RECIEVED = "{0} request recieved"

# Card keys
CARD_SPECIES_ID = "s_id"
CARD_NAME = "name"
CARD_TYPE_ID = "type"
CARD_HP = "hp"
CARD_ATK_NAME_1 = "atkName1"
CARD_ATK_NAME_2 = "atkName2"
CARD_ATK_TYPE_1 = "atkType1"
CARD_ATK_TYPE_2 = "atkType2"
CARD_RARITY = "rarity"

class PokemonHTTPRequestHandler(BaseHTTPRequestHandler):
    def verbosePrint(self, arg):
        if OUTPUT_MODE == "verbose":
            print(arg)

    def incRequestCount(self):
        log.log_debug("Increasing request count")
        # pylint: disable=global-statement
        global num_requests
        # pylint: enable=global-statement

        num_requests = num_requests + 1

        log.log_info(f"Current request count: {num_requests}")

    def requestStarted(self, requestType):
        log.log_debug(f"{requestType} request started")

        self.incRequestCount()

        print(f"START REQUEST NUMBER {num_requests}")
        self.showPath(requestType)

    def requestEnded(self):
        log.log_debug("Request ended")

        print(f"END REQUEST NUMBER {num_requests}")
        print()

    def showPath(self, requestType):
        log.log_debug("Showing path")

        print(f"{requestType} PATH: {self.path}")

    def extractCardIdFromPath(self):
        log.log_debug("Extracting card ID from path")

        split_path = self.path.split('/')

        if len(split_path) == 3:
            collection_path = split_path[1]
            element_path = split_path[2]

            if( collection_path == "cards" and \
                len(element_path) > 4 and \
                element_path[0:4] == "card" ):

                card_num = int(element_path[4:])

                return card_num
        return -1

    def readPageFromFile(self, filename):
        log.log_debug("Reading file from page: {filename}")

        with open(filename, encoding=UTF8) as f:
            for line in f:
                self.wfile.write(line)

    def enableCORS(self):
        log.log_debug("CORS enabled")

        self.send_header(HEADER_CORS, "*")

    def sendCode404(self):
        log.log_debug("Sending Code 404")

        self.send_response(404)
        self.end_headers()

    def sendPage404(self):
        log.log_debug("Sending Page 404")

        self.send_response(404)
        self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_HTML)
        self.readPageFromFile(ERR_404)

    def getCardFromDB(self):
        card_id = self.path.split("/")[2][4:]

        log.log_debug(f"Retreiving card {card_id} from database")

        db = DBController()

        if db.cardExists(card_id):
            log.log_debug(f"Card {card_id} found in database")
            card = db.getCard(card_id)

            self.send_response(200)
            self.enableCORS()
            self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_JSON)
            self.end_headers()

            json_card = json.dumps(card)

            self.wfile.write(bytes(json_card, UTF8))

        else:
            log.log_debug(f"Unable to find card {card_id} in database")

            self.send_response(404)
            self.enableCORS()
            self.end_headers()

    def getCardsFromDB(self):
        log.log_debug("Retrieving cards from database")

        db = DBController()

        cards = db.getCards()

        json_cards = json.dumps(cards)

        self.verbosePrint(json_cards)

        self.send_response(200)
        self.enableCORS()
        self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_JSON)
        self.end_headers()

        self.wfile.write(bytes(json_cards, UTF8))

    def getNamesFromDB(self):
        log.log_debug("Retrieving names from database")

        db = DBController()

        names = db.getNames()
        json_names = json.dumps(names)

        self.send_response(200)
        self.enableCORS()
        self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_JSON)
        self.end_headers()

        self.wfile.write(bytes(json_names, UTF8))

    def getRaritiesFromDB(self):
        log.log_debug("Retrieving rarities from database")

        db = DBController()

        rarities = db.getRarities()
        json_rarities = json.dumps(rarities)

        self.send_response(200)
        self.enableCORS()
        self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_JSON)
        self.end_headers()
        self.wfile.write(bytes(json_rarities, UTF8))

    def getTypesFromDB(self):
        log.log_debug("Retrieving types from database")

        db = DBController()

        types = db.getTypes()
        json_types = json.dumps(types)

        self.send_response(200)
        self.enableCORS()
        self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_JSON)
        self.end_headers()

        self.wfile.write(bytes(json_types, UTF8))

    def do_GET(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_GET))

        self.requestStarted(STR_GET)

        if self.path == "/cards":
            self.verbosePrint("Reading cards from DB")
            self.getCardsFromDB()

        elif self.path == "/names":
            self.verbosePrint("Reading names from DB")
            self.getNamesFromDB()

        elif self.path == "/rarities":
            self.verbosePrint("Reading rarities from DB")
            self.getRaritiesFromDB()

        elif self.path == "/types":
            self.verbosePrint("Reading types from DB")
            self.getTypesFromDB()

        elif self.path.split('/')[1] == "cards":
            self.verbosePrint("Reading a card from DB")
            self.getCardFromDB()

        else:
            self.sendCode404()

        self.requestEnded()

    def do_POST(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_POST))

        self.requestStarted(STR_POST)

        if self.path == "/cards":
            body_len = int(self.headers["Content-Length"])
            body = self.rfile.read(body_len).decode(UTF8)

            self.verbosePrint(body)

            parsed_body = parse_qs(body)
            self.verbosePrint(parsed_body)

            if not ( \
                CARD_SPECIES_ID in parsed_body or \
                CARD_NAME       in parsed_body or \
                CARD_TYPE_ID    in parsed_body or \
                CARD_HP         in parsed_body or \
                CARD_ATK_NAME_1 in parsed_body or \
                CARD_ATK_TYPE_1 in parsed_body or \
                CARD_ATK_NAME_2 in parsed_body or \
                CARD_ATK_TYPE_2 in parsed_body or \
                CARD_RARITY     in parsed_body \
            ):
                print("Invalid headers in request")

                self.send_response(404)
                self.enableCORS()
                self.end_headers()

            else:
                db = DBController()

                db.createCard( \
                    parsed_body[CARD_SPECIES_ID][0], \
                    parsed_body[CARD_NAME][0], \
                    parsed_body[CARD_TYPE_ID][0], \
                    parsed_body[CARD_HP][0], \
                    parsed_body[CARD_ATK_NAME_1][0], \
                    parsed_body[CARD_ATK_TYPE_1][0], \
                    parsed_body[CARD_ATK_NAME_2][0], \
                    parsed_body[CARD_ATK_TYPE_2][0], \
                    parsed_body[CARD_RARITY][0] \
                )

                print("Card created")

                self.send_response(201)
                self.enableCORS()
                self.end_headers()

        else:
            self.sendCode404()

        self.requestEnded()

    def do_PUT(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_PUT))

        self.requestStarted(STR_PUT)

        card_num = int(self.extractCardIdFromPath())

        db = DBController()

        if db.cardExists(card_num):
            body_len = int(self.headers["Content-Length"])
            body = self.rfile.read(body_len).decode(UTF8)

            parsed_body = parse_qs(body)

            if not ( \
                CARD_SPECIES_ID in parsed_body or \
                CARD_NAME       in parsed_body or \
                CARD_TYPE_ID    in parsed_body or \
                CARD_HP         in parsed_body or \
                CARD_ATK_NAME_1 in parsed_body or \
                CARD_ATK_TYPE_1 in parsed_body or \
                CARD_ATK_NAME_2 in parsed_body or \
                CARD_ATK_TYPE_2 in parsed_body or \
                CARD_RARITY     in parsed_body \
            ):
                print("Invalid headers in request")

                self.send_response(404)
                self.enableCORS()
                self.end_headers()

            else:
                db.updateCard( \
                    parsed_body[CARD_SPECIES_ID][0], \
                    parsed_body[CARD_NAME][0], \
                    parsed_body[CARD_TYPE_ID][0], \
                    parsed_body[CARD_HP][0], \
                    parsed_body[CARD_ATK_NAME_1][0], \
                    parsed_body[CARD_ATK_NAME_2][0], \
                    parsed_body[CARD_ATK_TYPE_1][0], \
                    parsed_body[CARD_ATK_TYPE_2][0], \
                    parsed_body[CARD_RARITY][0], \
                    parsed_body["id"][0] \
                )

                print("Card updated")

                self.send_response(200)
                self.enableCORS()
                self.end_headers()
        else:
            self.sendCode404()

        self.requestEnded()

    def do_DELETE(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_DELETE))

        self.requestStarted(STR_DELETE)

        split_path = self.path.split('/')

        if len(split_path) == 3:
            collection_path = split_path[1]
            element_path = split_path[2]

            db = DBController()

            card_num = int(element_path[4:])

            if(collection_path == "cards" and element_path[0:4] == "card" and db.cardExists(card_num)):
                db.deleteCard(card_num)

                self.send_response(200)
                self.enableCORS()
                self.end_headers()

            else:
                self.sendCode404()

        else:
            self.sendCode404()

        self.requestEnded()

    def do_PATCH(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_PATCH))

        self.requestStarted(STR_PATCH)
        self.sendCode404()
        self.requestEnded()

    def do_COPY(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_COPY))

        self.requestStarted(STR_COPY)
        self.sendCode404()
        self.requestEnded()

    def do_HEAD(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_HEAD))

        self.requestStarted(STR_HEAD)
        self.sendCode404()
        self.requestEnded()

    def do_OPTIONS(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_OPTIONS))

        self.requestStarted(STR_OPTIONS)

        self.send_response(200)

        self.enableCORS()

        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        self.end_headers()

        self.requestEnded()

    def do_LINK(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_LINK))

        self.requestStarted(STR_LINK)
        self.sendCode404()
        self.requestEnded()

    def do_UNLINK(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_UNLINK))

        self.requestStarted(STR_UNLINK)
        self.sendCode404()
        self.requestEnded()

    def do_PURGE(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_PURGE))

        self.requestStarted(STR_PURGE)
        self.sendCode404()
        self.requestEnded()

    def do_LOCK(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_LOCK))

        self.requestStarted(STR_LOCK)
        self.sendCode404()
        self.requestEnded()

    def do_UNLOCK(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_UNLOCK))

        self.requestStarted(STR_UNLOCK)
        self.sendCode404()
        self.requestEnded()

    def do_PROPFIND(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_PROPFIND))

        self.requestStarted(STR_PROPFIND)
        self.sendCode404()
        self.requestEnded()

    def do_VIEW(self):
        log.log_debug(STR_REQ_RECIEVED.format(STR_VIEW))

        self.requestStarted(STR_VIEW)
        self.sendCode404()
        self.requestEnded()
