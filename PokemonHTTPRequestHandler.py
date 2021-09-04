# Adam Manning 2021

from DBController import DBController

from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

import json

numRequests = 0

# Headers
header_ContentType = "Content-Type"
header_CORS = "Access-Control-Allow-Origin"

content_TypeJSON = "application/json"
content_TypeHTML = "text/html"

utf8 = "utf-8"

err = "err/{0}.html"
err404 = err.format(404)

outputMode = "verbose";

# Card keys
cardSpecID = "s_id"
cardName = "name"
cardTypeID = "type"
cardHP = "hp"
cardAtkName1 = "atkName1"
cardAtkName2 = "atkName2"
cardAtkType1 = "atkType1"
cardAtkType2 = "atkType2"
cardRarity = "rarity"

class PokemonHTTPRequestHandler(BaseHTTPRequestHandler):
    def verbosePrint(self, arg):
        if outputMode == "verbose":
            print(arg)

    def incRequestCount(self):
        global numRequests
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
            collectionPath = splitPath[1];
            elementPath = splitPath[2];

            if( collectionPath == "cards" and \
                len(elementPath) > 4 and \
                elementPath[0:4] == "card" ):

                cardNo = int(elementPath[4:])

                return cardNo
        return -1

    def readPageFromFile(self, filename):
        f = open(filename)

        for line in f:
            self.wfile.write(line)

        f.close()

    def enableCORS(self):
        self.send_header(header_CORS, "*")

    def sendCode404(self):
        self.send_response(404)
        self.end_headers()

    def sendPage404(self):
        self.send_response(404)
        self.send_header(header_ContentType, content_TypeHTML)
        self.readPageFromFile(err404)

    def getCardFromDB(self):
        db = DBController()

        cid = self.path.split("/")[2][4:]

        if db.cardExists(cid):
            card = db.getCard(cid)

            self.send_response(200)
            self.enableCORS()
            self.send_header(header_ContentType, content_TypeJSON)
            self.end_headers()

            jsonCard = json.dumps(card)

            self.wfile.write(bytes(jsonCard, utf8))

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
        self.enableCORS();
        self.send_header(header_ContentType, content_TypeJSON)
        self.end_headers()

        self.wfile.write(bytes(jsonCards, utf8))

    def getNamesFromDB(self):
        db = DBController()

        names = db.getNames()
        jsonNames = json.dumps(names)

        self.send_response(200)
        self.enableCORS()
        self.send_header(header_ContentType, content_TypeJSON)
        self.end_headers()

        self.wfile.write(bytes(jsonNames, utf8))

    def getRaritiesFromDB(self):
        db = DBController()

        rarities = db.getRarities()
        jsonRarities = json.dumps(rarities)

        self.send_response(200)
        self.enableCORS()
        self.send_header(header_ContentType, content_TypeJSON)
        self.end_headers()
        self.wfile.write(bytes(jsonRarities, utf8))

    def getTypesFromDB(self):
        db = DBController()

        types = db.getTypes()
        jsonTypes = json.dumps(types)

        self.send_response(200)
        self.enableCORS()
        self.send_header(header_ContentType, content_TypeJSON)
        self.end_headers()

        self.wfile.write(bytes(jsonTypes, utf8))

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
            body = self.rfile.read(bodyLen).decode(utf8)

            self.verbosePrint(body)

            parsed_body = parse_qs(body)
            self.verbosePrint(parsed_body)

            if not ( \
                cardSpecID      in parsed_body or \
                cardName      in parsed_body or \
                cardTypeID      in parsed_body or \
                cardHP        in parsed_body or \
                cardAtkName1  in parsed_body or \
                cardAtkType1  in parsed_body or \
                cardAtkName2  in parsed_body or \
                cardAtkType2  in parsed_body or \
                cardRarity    in parsed_body \
            ):
                print("Invalid headers in request")

                self.send_response(404)
                self.enableCORS()
                self.end_headers()

            else:
                db = DBController()

                db.createCard( \
                    parsed_body[cardSpecID][0], \
                    parsed_body[cardName][0], \
                    parsed_body[cardTypeID][0], \
                    parsed_body[cardHP][0], \
                    parsed_body[cardAtkName1][0], \
                    parsed_body[cardAtkType1][0], \
                    parsed_body[cardAtkName2][0], \
                    parsed_body[cardAtkType2][0], \
                    parsed_body[cardRarity][0] \
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
            body = self.rfile.read(bodyLen).decode(utf8)

            parsed_body = parse_qs(body)

            if not ( \
                cardSpecID      in parsed_body or \
                cardName      in parsed_body or \
                cardTypeID      in parsed_body or \
                cardHP        in parsed_body or \
                cardAtkName1  in parsed_body or \
                cardAtkType1  in parsed_body or \
                cardAtkName2  in parsed_body or \
                cardAtkType2  in parsed_body or \
                cardRarity    in parsed_body \
            ):
                print("Invalid headers in request")

                self.send_response(404)
                self.enableCORS()
                self.end_headers()

            else:
                db.updateCard( \
                    parsed_body[cardSpecID][0], \
                    parsed_body[cardName][0], \
                    parsed_body[cardTypeID][0], \
                    parsed_body[cardHP][0], \
                    parsed_body[cardAtkName1][0], \
                    parsed_body[cardAtkName2][0], \
                    parsed_body[cardAtkType1][0], \
                    parsed_body[cardAtkType2][0], \
                    parsed_body[cardRarity][0], \
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
            collectionPath = splitPath[1];
            elementPath = splitPath[2];

            db = DBController();

            cardNo = int(elementPath[4:])

            if( collectionPath == "cards" and \
                elementPath[0:4] == "card" and \
                db.cardExists(cardNo) \
                ):
                    db.deleteCard(cardNo)

                    self.send_response(200);
                    self.enableCORS();
                    self.end_headers();

            else:
                self.sendCode404();

        else:
            self.sendCode404();

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
