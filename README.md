 <!-- Adam Manning 2021 -->

# Pokémon Card Collection

[pikachu_sprite]: img/25.gif
[venusaur_sprite]: img/3.gif
[charizard_sprite]: img/6.gif
[blastoise_sprite]: img/9.gif

[pikachu_card]: https://archives.bulbagarden.net/media/upload/c/cd/PikachuJungle60.jpg
[venusar_card]: https://archives.bulbagarden.net/media/upload/a/a4/VenusaurBaseSet15.jpg
[charizard_card]: https://archives.bulbagarden.net/media/upload/4/4e/CharizardBaseSet4.jpg
[blastoise_card]: https://archives.bulbagarden.net/media/upload/a/a5/BlastoiseBaseSet2.jpg

| ![Pikachu][pikachu_sprite] | ![Venusaur][venusaur_sprite] | ![Charizard][charizard_sprite] | ![Blastoise][blastoise_sprite] |
| :-----------------: | :-------------------: | :---------------------: | :---------------------: |
| <img src="https://archives.bulbagarden.net/media/upload/c/cd/PikachuJungle60.jpg" height="175"> | <img src="https://archives.bulbagarden.net/media/upload/a/a4/VenusaurBaseSet15.jpg" height="175px" alt="Venusaur"> | <img src="https://archives.bulbagarden.net/media/upload/4/4e/CharizardBaseSet4.jpg"  height="175px" alt="Charizard"> | <img src="https://archives.bulbagarden.net/media/upload/a/a5/BlastoiseBaseSet2.jpg"  height="175px" alt="Blastoise"> |

# Table of Contents

1. [Table of Contents](#table-of-contents)
1. [About](#about)
1. [Resource: `cards`](#resource-cards)
    1. [Attributes](#attributes)
1. [Database](#database)
    1. [Database Schema](#database-schema)
    1. [Building the Database](#building-the-database)
1. [Server](#server)
    1. [Starting the Server](#starting-the-server)
    1. [REST Endpoints](#rest-endpoints)
          1. [List](#list)
          1. [Retrieve](#retrieve)
          1. [Create](#create)
          1. [Replace](#replace)
          1. [Delete](#delete)
1. [Webpage](#webpage)
    1. [Open the Webpage](#open-the-webpage)

# About


I began this project as an assignment for college and it is intended to demonstrate the use of the REST API.

The purpose of this web app is to track a Pokémon card collection in a database.

[Back to Top](#table-of-contents)

# Resource: cards

## Attributes

* `id`: The card's unique id in the Database
* `s_id`: A number representing the species number in the National Poke&#769;dex
* `name`: Either the name of the card or any desired nickname
* `type`: The type of the card
* `hp`: The number of hit points on the face of the card
* `atkName1`: The name of the card's first attack
* `atkName2`: The name of the card's second attack
* `atkType1`: The type of the card's first attack
* `atkType2`: The type of the card's first attack
* `rarity`: Describes how rare the card is

[Back to Top](#table-of-contents)

# Database

## Database Schema

```sql
CREATE TABLE cards
  (
    id INTEGER PRIMARY KEY, s_id INTEGER,
    name VARCHAR(255), type VARCHAR(255), hp VARCHAR(255),
    atkName1 VARCHAR(255), atkType1 VARCHAR(255),
    atkName2 VARCHAR(255), atkType2 VARCHAR(255),
    rarity VARCHAR(255)
  );

CREATE TABLE names
  (id INTEGER PRIMARY KEY, name VARCHAR(255));

CREATE TABLE types
  (id INTEGER PRIMARY KEY, type VARCHAR(255));
```

## Building the Database

1. Open Terminal
1. Navigate to the `Pokemon-Card-Collection` directory
1. Run: `chmod 744 build_database.sh`
1. Run: `./build_database.sh`
1. Type `y` to build the database or `n` to cancel

[Back to Top](#table-of-contents)

# Server

## Starting the Server

1. Open Terminal
1. Navigate to the `Pokemon-Card-Collection` directory
1. Run: `chmod 744 startServer`
1. Run: `./startServer`

[Back to Top](#table-of-contents)

## REST Endpoints

- ### List
	- **Method:** `GET`
	- **Path:** `http://localhost:8080/cards`

- ### Retrieve
	- **Method:** `GET`
	- **Path:** `http://localhost:8080/cards/card0`

- ### Create
	- **Method:** `POST`
	- **Path:** `http://localhost:8080/cards`

- ### Replace
	- **Method:** `PATCH`
	- **Path:** `http://localhost:8080/cards/card0`

- ### Delete
	- **Method:** `DELETE`
	- **Path:** `http://localhost:8080/cards/card0`

[Back to Top](#table-of-contents)

# Webpage

## Open the Webpage
1. [Build the database](#building-the-database)
1. [Start the server](#starting-the-server)
1. Open Safari
1. File -> Open -> {Pokemon-Card-Collection}/index.html

[Back to Top](#table-of-contents)
