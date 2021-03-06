 <!-- Adam Manning 2021 -->
 <h6>
  *I began this project as an assignment for college and is intended to demonstrate the use of the REST API.
 </h6>

# cards

<!--
[pikachu]: https://cdn.bulbagarden.net/upload/thumb/1/1a/SurfingPikachuWizardsPromo28.jpg/200px-SurfingPikachuWizardsPromo28.jpg

[venusaur]: https://cdn.bulbagarden.net/upload/thumb/d/d9/VenusaurWizardsPromo13.jpg/180px-VenusaurWizardsPromo13.jpg

[charizard]: https://cdn.bulbagarden.net/upload/thumb/4/4e/CharizardBaseSet4.jpg/200px-CharizardBaseSet4.jpg

[blastoise]: https://cdn.bulbagarden.net/upload/thumb/a/a5/BlastoiseBaseSet2.jpg/180px-BlastoiseBaseSet2.jpg
-->

<!-- ![Surfing Pikachu][pikachu] ![Venusaur][venusaur] ![Charizard][charizard] ![Blastoise][blastoise] -->
<!--
<img src="https://cdn.bulbagarden.net/upload/thumb/1/1a/SurfingPikachuWizardsPromo28.jpg/200px-SurfingPikachuWizardsPromo28.jpg" height="175"><img src="https://cdn.bulbagarden.net/upload/thumb/d/d9/VenusaurWizardsPromo13.jpg/180px-VenusaurWizardsPromo13.jpg" height="175px" alt="Venusaur"><img src="https://cdn.bulbagarden.net/upload/thumb/4/4e/CharizardBaseSet4.jpg/200px-CharizardBaseSet4.jpg"  height="175px" alt="Charizard"><img src="https://cdn.bulbagarden.net/upload/thumb/a/a5/BlastoiseBaseSet2.jpg/180px-BlastoiseBaseSet2.jpg"  height="175px" alt="Blastoise">
-->

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
