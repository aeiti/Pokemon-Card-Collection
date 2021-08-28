import sqlite3

textDir = "../text/"

connection = sqlite3.connect("pokemon.db")
cursor = connection.cursor()

# Populate names table
names = open(textDir + "names.txt")

for line in names:
    line = line.strip()
    cursor.execute("INSERT INTO names (name) VALUES (?)", (line,))
    connection.commit()

names.close()

# Populate types table
types = open(textDir + "types.txt")

for line in types:
    line = line.strip()
    cursor.execute("INSERT INTO types (type) VALUES (?)", (line,))
    connection.commit()

types.close()

# Populate rarities table
rarities = open(textDir + "rarities.txt")

for line in rarities:
    line = line.strip()
    cursor.execute("INSERT INTO rarities (rarity) VALUES (?)", (line,))
    connection.commit()

rarities.close()

connection.close()
