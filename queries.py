 # Adam Manning 2021

CREATE_CARD = "INSERT INTO cards (s_id, name, type, hp, atkName1, atkName2, atkType1, atkType2, rarity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

DELETE_CARD = "DELETE FROM cards WHERE id=?"

UPDATE_CARD = "UPDATE cards SET s_id=?, name=?, type=?, hp=?, atkName1=?, atkName2=?, atkType1=?, atkType2=?, rarity=? WHERE id=?"

GET_CARD = "SELECT * FROM cards WHERE id=?"
GET_CARDS = "SELECT * FROM cards"

GET_NAME = "SELECT * FROM names WHERE id=?"
GET_NAMES = "SELECT * FROM names"

GET_RARITY = "SELECT * FROM rarities WHERE id=?"
GET_RARITIES = "SELECT * FROM rarities"

GET_TYPE = "SELECT * FROM types WHERE id=?"
GET_TYPES = "SELECT * FROM types"
