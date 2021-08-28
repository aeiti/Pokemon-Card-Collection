 # Adam Manning 2021

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
        self.dbName = dbDir + "pokemon.db"
        self.connection = sqlite3.connect(self.dbName)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def getDatabseName(self):
        return self.dbname

    def cardExists(self, cid):
        self.cursor.execute(queries.getCard, (cid,))
        exists = self.cursor.fetchall();

        if len(exists) == 1:
            return True

        return False

    def createCard(self, s_id, name, t_id, hp, atkName1, atkName2, atkType1, atkType2, rarity):
        self.cursor.execute(queries.createCard, (s_id, name, t_id, hp, atkName1, atkType1, atkName2, atkType2, rarity))
        self.connection.commit()

    def deleteCard(self, c_id):
        self.cursor.execute(queries.deleteCard, (c_id,))
        self.connection.commit()

    def updateCard(self, s_id, name, t_id, hp, atkName1, atkName2, atkType1, atkType2, rarity, cid):
        self.cursor.execute(queries.updateCard, (s_id, name, t_id, hp, atkName1, atkName2, atkType1, atkType2, rarity, cid))
        self.connection.commit()

    def getCard(self, c_id):
        self.cursor.execute(queries.getCard, (c_id,))
        rows = self.cursor.fetchall()
        return rows

    def getCards(self):
        self.cursor.execute(queries.getCards)
        rows = self.cursor.fetchall()
        return rows

    def getName(self, n_id):
        self.cursor.execute(queries.getName, (n_id,))
        rows = self.cursor.fetchall()
        return rows

    def getNames(self):
        self.cursor.execute(queries.getNames)
        rows = self.cursor.fetchall()
        return rows

    def getRarity(self, r_id):
        self.cursor.execute(queries.getRarity, (r_id,))
        rows = self.cursor.fetchall()
        return rows

    def getRarities(self):
        self.cursor.execute(queries.getRarities)
        rows = self.cursor.fetchall()
        return rows

    def getType(self, t_id):
        self.cursor.execute(queries.getType, (t_id,))
        rows = self.cursor.fetchall()
        return rows

    def getTypes(self):
        self.cursor.execute(queries.getTypes)
        rows = self.cursor.fetchall()
        return rows
