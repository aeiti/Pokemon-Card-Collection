"""
DBController.py
Adam Manning 2021
Allows for access to the database
"""

import sqlite3

# All queries are stored here
import queries

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

dbDir = "db/"
class DBController:
    def __init__(self):
        self.DB_NAME = dbDir + "pokemon.db"
        self.connection = sqlite3.connect(self.DB_NAME)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def getDatabaseName(self):
        return self.DB_NAME

    def cardExists(self, card_id):
        self.cursor.execute(queries.GET_CARD, (card_id,))
        exists = self.cursor.fetchall()

        if len(exists) == 1:
            return True

        return False

    def createCard(self, species_id, name, type_id, hp, atk_name1, atk_name2, atk_type1, atk_type2, rarity):
        self.cursor.execute(queries.CREATE_CARD, (species_id, name, type_id, hp, atk_name1, atk_type1, atk_name2, atk_type2, rarity))
        self.connection.commit()

    def deleteCard(self, card_id):
        self.cursor.execute(queries.DELETE_CARD, (card_id,))
        self.connection.commit()

    def updateCard(self, species_id, name, type_id, hp, atk_name1, atk_name2, atk_type1, atk_type2, rarity, card_id):
        self.cursor.execute(queries.UPDATE_CARD, (species_id, name, type_id, hp, atk_name1, atk_name2, atk_type1, atk_type2, rarity, card_id))
        self.connection.commit()

    def getCard(self, card_id):
        self.cursor.execute(queries.GET_CARD, (card_id,))
        rows = self.cursor.fetchall()
        return rows

    def getCards(self):
        self.cursor.execute(queries.GET_CARDS)
        rows = self.cursor.fetchall()
        return rows

    def getName(self, name_id):
        self.cursor.execute(queries.GET_NAME, (name_id,))
        rows = self.cursor.fetchall()
        return rows

    def getNames(self):
        self.cursor.execute(queries.GET_NAMES)
        rows = self.cursor.fetchall()
        return rows

    def getRarity(self, rarity_id):
        self.cursor.execute(queries.GET_RARITY, (rarity_id,))
        rows = self.cursor.fetchall()
        return rows

    def getRarities(self):
        self.cursor.execute(queries.GET_RARITIES)
        rows = self.cursor.fetchall()
        return rows

    def getType(self, type_id):
        self.cursor.execute(queries.GET_TYPE, (type_id,))
        rows = self.cursor.fetchall()
        return rows

    def getTypes(self):
        self.cursor.execute(queries.GET_TYPES)
        rows = self.cursor.fetchall()
        return rows
