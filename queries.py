createCard = "INSERT INTO cards (s_id, name, type, hp, atkName1, atkName2, atkType1, atkType2, rarity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

deleteCard = "DELETE FROM cards WHERE id=?"

updateCard = "UPDATE cards SET s_id=?, name=?, type=?, hp=?, atkName1=?, atkName2=?, atkType1=?, atkType2=?, rarity=? WHERE id=?"

getCard = "SELECT * FROM cards WHERE id=?"
getCards = "SELECT * FROM cards"

getName = "SELECT * FROM names WHERE id=?"
getNames = "SELECT * FROM names"

getRarity = "SELECT * FROM rarities WHERE id=?"
getRarities = "SELECT * FROM rarities"

getType = "SELECT * FROM types WHERE id=?"
getTypes = "SELECT * FROM types"
