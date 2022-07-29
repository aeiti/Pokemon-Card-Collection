"""
PokemonHTTPRequestHandler.py
Adam Manning (C) 2021
"""

from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

import json

from DBController import DBController

numRequests = 0

# Headers
HEADER_CONTENT_TYPE = "Content-Type"
HEADER_CORS = "Access-Control-Allow-Origin"

CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_HTML = "text/html"

UTF8 = "utf-8"

ERR = "err/{0}.html"
ERR_404 = ERR.format(404)

OUTPUT_MODE = "verbose"

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
        # pylint: disable=global-statement
        global numRequests
        # pylint: enable=global-statement

        numRequests = numRequests + 1

    def requestStarted(self, requestType):
        self.incRequestCount()
        print(f"START REQUEST NUMBER {numRequests}")
        self.showPath(requestType)

    def requestEnded(self):
        print(f"END REQUEST NUMBER {numRequests}")
        print()

    def showPath(self, requestType):
        print(f"{requestType} PATH: {self.path}")

    def extractCardIdFromPath(self):
        splitPath = self.path.split('/')

        if len(splitPath) == 3:
            collectionPath = splitPath[1]
            elementPath = splitPath[2]

            if( collectionPath == "cards" and \
                len(elementPath) > 4 and \
                elementPath[0:4] == "card" ):

                cardNo = int(elementPath[4:])

                return cardNo
        return -1

    def readPageFromFile(self, filename):
        with open(filename, encoding=UTF8) as f:
            for line in f:
                self.wfile.write(line)

    def enableCORS(self):
        self.send_header(HEADER_CORS, "*")

    def sendCode404(self):
        self.send_response(404)
        self.end_headers()

    def sendPage404(self):
        self.send_response(404)
        self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_HTML)
        self.readPageFromFile(ERR_404)

    def getCardFromDB(self):
        db = DBController()

        cid = self.path.split("/")[2][4:]

        if db.cardExists(cid):
            card = db.getCard(cid)

            self.send_response(200)
            self.enableCORS()
            self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_JSON)
            self.end_headers()

            jsonCard = json.dumps(card)

            self.wfile.write(bytes(jsonCard, UTF8))

        else:
            self.send_response(404)
            self.enableCORS()
            self.end_headers()

    def getCardsFromDB(self):
        db = DBController()

        cards = db.getCards()

        jsonCards = json.dumps(cards)

        self.verbosePrint(jsonCards)

        self.send_response(200)
        self.enableCORS()
        self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_JSON)
        self.end_headers()

        self.wfile.write(bytes(jsonCards, UTF8))

    def getNamesFromDB(self):
        db = DBController()

        names = db.getNames()
        jsonNames = json.dumps(names)

        self.send_response(200)
        self.enableCORS()
        self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_JSON)
        self.end_headers()

        self.wfile.write(bytes(jsonNames, UTF8))

    def getRaritiesFromDB(self):
        db = DBController()

        rarities = db.getRarities()
        jsonRarities = json.dumps(rarities)

        self.send_response(200)
        self.enableCORS()
        self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_JSON)
        self.end_headers()
        self.wfile.write(bytes(jsonRarities, UTF8))

    def getTypesFromDB(self):
        db = DBController()

        types = db.getTypes()
        jsonTypes = json.dumps(types)

        self.send_response(200)
        self.enableCORS()
        self.send_header(HEADER_CONTENT_TYPE, CONTENT_TYPE_JSON)
        self.end_headers()

        self.wfile.write(bytes(jsonTypes, UTF8))

    def do_GET(self):
        self.requestStarted("GET")

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
        self.requestStarted("POST")

        if self.path == "/cards":
            bodyLen = int(self.headers["Content-Length"])
            body = self.rfile.read(bodyLen).decode(UTF8)

            self.verbosePrint(body)

            parsed_body = parse_qs(body)
            self.verbosePrint(parsed_body)

            if not ( \
                CARD_SPECIES_ID      in parsed_body or \
                CARD_NAME      in parsed_body or \
                CARD_TYPE_ID      in parsed_body or \
                CARD_HP        in parsed_body or \
                CARD_ATK_NAME_1  in parsed_body or \
                CARD_ATK_TYPE_1  in parsed_body or \
                CARD_ATK_NAME_2  in parsed_body or \
                CARD_ATK_TYPE_2  in parsed_body or \
                CARD_RARITY    in parsed_body \
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
        self.requestStarted("PATCH")

        cardNo = int(self.extractCardIdFromPath())

        db = DBController()

        if db.cardExists(cardNo):
            bodyLen = int(self.headers["Content-Length"])
            body = self.rfile.read(bodyLen).decode(UTF8)

            parsed_body = parse_qs(body)

            if not ( \
                CARD_SPECIES_ID      in parsed_body or \
                CARD_NAME      in parsed_body or \
                CARD_TYPE_ID      in parsed_body or \
                CARD_HP        in parsed_body or \
                CARD_ATK_NAME_1  in parsed_body or \
                CARD_ATK_TYPE_1  in parsed_body or \
                CARD_ATK_NAME_2  in parsed_body or \
                CARD_ATK_TYPE_2  in parsed_body or \
                CARD_RARITY    in parsed_body \
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
        self.requestStarted("DELETE")

        splitPath = self.path.split('/')

        if len(splitPath) == 3:
            collectionPath = splitPath[1]
            elementPath = splitPath[2]

            db = DBController()

            cardNo = int(elementPath[4:])

            if(collectionPath == "cards" and elementPath[0:4] == "card" and db.cardExists(cardNo)):
                db.deleteCard(cardNo)

                self.send_response(200)
                self.enableCORS()
                self.end_headers()

            else:
                self.sendCode404()

        else:
            self.sendCode404()

        self.requestEnded()

    def do_PATCH(self):
        self.requestStarted("PATCH")
        self.sendCode404()
        self.requestEnded()

    def do_COPY(self):
        self.requestStarted("COPY")
        self.sendCode404()
        self.requestEnded()

    def do_HEAD(self):
        self.requestStarted("HEAD")
        self.sendCode404()
        self.requestEnded()

    def do_OPTIONS(self):
        self.requestStarted("OPTIONS")

        self.send_response(200)

        self.enableCORS()

        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        self.end_headers()

        self.requestEnded()

    def do_LINK(self):
        self.requestStarted("LINK")
        self.sendCode404()
        self.requestEnded()

    def do_UNLINK(self):
        self.requestStarted("UNLINK")
        self.sendCode404()
        self.requestEnded()

    def do_PURGE(self):
        self.requestStarted("PURGE")
        self.sendCode404()
        self.requestEnded()

    def do_LOCK(self):
        self.requestStarted("LOCK")
        self.sendCode404()
        self.requestEnded()

    def do_UNLOCK(self):
        self.requestStarted("UNLOCK")
        self.sendCode404()
        self.requestEnded()

    def do_PROPFIND(self):
        self.requestStarted("PROPFIND")
        self.sendCode404()
        self.requestEnded()

    def do_VIEW(self):
        self.requestStarted("VIEW")
        self.sendCode404()
        self.requestEnded()
