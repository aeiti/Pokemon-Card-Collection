"""
This script builds the required database for the server.
"""

import sqlite3

TEXT_DIR = "../text/"

NAMES_FILE = "names.txt"
TYPES_FILE = "types.txt"
RARITES_FILE = "rarities.txt"

# Default file encoding
UTF8 = "utf-8"

def main():
    """
    Main function of script
    """

    connection = sqlite3.connect("pokemon.db")
    cursor = connection.cursor()

    read_names(cursor, connection)
    read_rarities(cursor, connection)
    read_types(cursor, connection)

    connection.close()
# End main()

def read_names(cursor, connection):
    """
    Reads names from the text file for insertion into database.
    Args:
        cursor: Database's cursor
        connection: Connnection to database
    """

    # Populate names table
    with open(TEXT_DIR + NAMES_FILE, encoding=UTF8, mode='r') as names:
        for line in names:
            line = line.strip()
            cursor.execute("INSERT INTO names (name) VALUES (?)", (line,))
            connection.commit()

        names.close()
# End read_names()

def read_rarities(cursor, connection):
    """
    Reads rarites from the text file for insertion into database.
    Args:
        cursor: Database's cursor
        connection: Connnection to database
    """
    # Populate rarities table
    with open(TEXT_DIR + RARITES_FILE, encoding=UTF8, mode='r') as rarities:
        for line in rarities:
            line = line.strip()
            cursor.execute("INSERT INTO rarities (rarity) VALUES (?)", (line,))
            connection.commit()

        rarities.close()
# End read_rarities()

def read_types(cursor, connection):
    """
    Reads types from the text file for insertion into database.
    Args:
        cursor: Database's cursor
        connection: Connnection to database
    """
    # Populate types table
    with open(TEXT_DIR + TYPES_FILE, encoding=UTF8, mode='r') as types:
        for line in types:
            line = line.strip()
            cursor.execute("INSERT INTO types (type) VALUES (?)", (line,))
            connection.commit()

        types.close()
# End read_types()

# Only run the script if it is the main file
if __name__ == "__main__":
    main()
