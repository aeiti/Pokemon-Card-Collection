// Adam Manning 2017

const serverURL = "http://localhost:8080/";

const cTypeFormEncodedData = "application/x-www-form-urlencoded";
const cTypeJSON = "application/json";

// Color to change the background of card depending on its type
const BUG       = "#A8B820";
const DARK      = "#705848";
const DRAGON    = "#7038F8";
const ELECTRIC  = "#F8D030";
const FAIRY     = "#EE99AC";
const FIGHTING  = "#C03028";
const FIRE      = "#F08030";
const FLYING    = "#A890F0";
const GHOST     = "#705898";
const GRASS     = "#78C850";
const GROUND    = "#E0C068";
const ICE       = "#98D8D8";
const NORMAL    = "#A8A878";
const POISON    = "#A040A0";
const PSYCHIC   = "#F85888";
const ROCK      = "#B8A038";
const STEEL     = "#B8B8D0";
const WATER     = "#6890F0";

// Location of image files
const imgDir = "img/"

var initialLoadCards = true;

// Divs
var divCards = getElem("#cards");

// Text inputs
var txtCardName = getElem("#card_name");
var txtAtkName1 = getElem("#atkName1");
var txtAtkName2 = getElem("#atkName2");
var txtHP       = getElem("#pokemon_hp");

// Select inputs
var selAtkType1 = getElem("#atkType1");
var selAtkType2 = getElem("#atkType2");
var selCardType = getElem("#pokemon_type");
var selRarity   = getElem("#rarity");
var selSpecies  = getElem("#pokemon_species");

// Hidden inputs
var hidPokemonId = getElem("#p_id");

// Arrays
var arrCards    = [];
var arrNames    = [];
var arrRarities = [];
var arrTypes    = [];

// Previous card in form
var prevName;
var prevHP;
var prevSpecies;
var prevCardType;
var prevAtkName1, prevAtkName2;
var prevAtkType1, prevAtkType2;

// Buttons
var btnAddCard = getElem("#btnCreateCard");
var btnClearForm = getElem("#btnClearForm");
var btnUpdateCard = getElem("#btnUpdateCard");
var btnCancelUpdate = getElem("#btnCancelUpdate");

//////////////////////////////////////////////////
// End of variable declarations/initializations //
//////////////////////////////////////////////////



//////////////////////////////////////////////////
////////// Start of function definitions /////////
//////////////////////////////////////////////////

// For debugging only
var outputFlag = true;
function print(arg)
{
  if(outputFlag)
  {
    console.log(arg);
  }
}

function btnAddCardOnClick()
{
  if(isValidFormData())
  {
    cardBody = encodeFormData();

    fetch
    (
      (serverURL + "cards"),
      {
        body: cardBody,
        method: "POST",
        headers: {
          "Content-Type": cTypeFormEncodedData
        }
      }
    );
    resetForm();

    getCardsFromServer();
  } // End if(validFormData)
} // End btnAddCardOnClick()

function btnClearFormOnClick()
{
  resetForm();
  print("Form reset");

}
// Handler for updating card details. Sends new information to server
function btnUpdateCardOnClick()
{
  if(isValidFormData()){
    print("Form data is valid");

    let data = encodeFormData();

    fetch
    (
      (serverURL + "cards/" + "card" + hidPokemonId.value),
      {
        body: data,
        method: "PUT",
        headers: {
          "Content-Type": cTypeFormEncodedData
        }
      }
    )
    .then
    (
      function()
      {
        switchToAddMode();
        resetForm();
        getCardsFromServer();
      }
    );
  }
} // End btnUpdateCardOnClick()

// Discards all changes and reload the most recent card
function btnCancelUpdateOnClick()
{
  getLastCard();
  switchToAddMode();
} // End btnCancelEditOnClick

// Only set form buttons
function setEventHandlers()
{
  print("Setting event handlers...");

  btnAddCard.onclick      = btnAddCardOnClick;
  btnClearForm.onclick    = btnClearFormOnClick;
  btnUpdateCard.onclick   = btnUpdateCardOnClick;
  btnCancelUpdate.onclick = btnCancelUpdateOnClick;

  print("Finished setting event handlers");
}

// Creates a <button> element
function makeButton()
{
  print("Creating <button>");

  let button = document.createElement("button");

  print("Finished creating <button>")

  return button;
}

// Creates a <div> element
function makeDiv()
{
  print("Creating <div>")

  let div = document.createElement("div");

  print("Finished creating <div>")

  return div;
}

// Creates a <img> element
function makeImg()
{
  print("Creating <img>")

  let img = document.createElement("img");

  print("Finished creating <img>")

  return img;
}

function addOptionToSelect(sel, value, text)
{
  let newOption = document.createElement("option");
  newOption.value = String(value);
  newOption.innerHTML = String(text);

  sel.appendChild(newOption);
}

function makeCardImg(card)
{
  print("Creating CardImg");

  let img = makeImg();
  img.className = "cardImg";

  let id = card["s_id"];
  print("Species: " + id);

  img.src = imgDir + id + ".gif";
  img.alt = arrNames[id - 1].name; //Should subtract 1

  print("Finished creating CardImg");

  return img;
}

function makeCardImgContainer()
{
  print("Creating CardImageContainer");

  let imgContainer = makeDiv();
  imgContainer.className = "cardImgContainer";

  print("Finished creating CardImageContainer");

  return imgContainer;
}

function makeCardTextContainer()
{
  print("Creating CardTextContainer");

  let txtContainer = makeDiv();
  txtContainer.className = "cardTextContainer";

  print("Finished creating CardTextContainer");

  return txtContainer;
}

function makeCardEditButton(card){
  print("Creating CardEditButton");

  let editButton = makeButton();
  editButton.innerHTML = "Edit Details"
  editButton.onclick = function()
  {
    print("Editing card with id(" + card["id"] + ")");

    txtCardName.value = card["name"];
    txtHP.value = card["hp"]

    if(card["atkName1"] == "None")
    {
      txtAtkName1.value = ""
    }
    else
    {
      txtAtkName1.value = card["atkName1"];
    }

    if(card["atkName2"] == "None")
    {
      txtAtkName2.value = ""
    }
    else
    {
      txtAtkName2.value = card["atkName2"]
    }

    selSpecies.selectedIndex  = card["s_id"] - 1;
    selCardType.selectedIndex = card["type"];
    selAtkType1.selectedIndex = card["atkType1"];
    selAtkType2.selectedIndex = card["atkType2"];
    selRarity.selectedIndex   = card["rarity"];

    hidPokemonId.value = card["id"];

    setLastCard();
    switchToUpdateMode();
  } // newCardEditButton.onclick

  print("Finished creating CardEditButton");
  return editButton;
}

function makeCardDeleteButton(card)
{
  print("Creating CardDeleteButton");

  let deleteButton = makeButton();
  deleteButton.innerHTML = "Delete Card";
  deleteButton.onclick = function()
  {
    let willDelete = confirm("Are you sure you want to delete " + card["name"] + "?");

    if(willDelete)
    {
      print(willDelete);

      fetch
      (
        (serverURL + "cards/" + "card" +  card["id"]),
        {
          method: "DELETE"
        }
      )
      .then
      (
        function(response)
        {
          let tempResponse = response.clone();

          print(tempResponse);

          return tempResponse;
        }
      )
      .then
      (
        function()
        {
          getCardsFromServer();
        }
      )
    }
  } // newCardDeleteButton.onclick

  print("Finished creating CardDeleteButton");

  return deleteButton;
}

function makeCardDiv(card)
{
  print("Creating CardDiv");

  let cardDiv = makeDiv();
  cardDiv.className = "cardDiv";
  cardDiv.id = "card" + arrNames[card["s_id"]];

  print("Finished creating CardDiv");

  return cardDiv;
}

function makeNameDiv(card)
{
  print("Creating NameDiv");

  let nameDiv = makeDiv();
  nameDiv.innerHTML = "Name: " + card["name"];

  print("Finished creating NameDiv");

  return nameDiv;
}

function makeHPDiv(card)
{
  print("Creating HPDiv");

  let hpDiv = makeDiv();
  hpDiv.innerHTML = "HP: " + card["hp"];

  print("Finished creating HPDiv");

  return hpDiv;
}

function makeSpeciesDiv(card)
{
  print("Creating SpeciesDiv");

  let speciesDiv = makeDiv();
  speciesDiv.innerHTML = "Species: " + arrNames[card["s_id"] - 1].name;

  print("Finished creating SpeciesDiv");

  return speciesDiv;
}

function makeTypeDiv(card)
{
  print("Creating TypeDiv");

  let typeDiv = makeDiv();
  typeDiv.innerHTML = "Type: " + arrTypes[card["type"]].type;

  print("Finished creating TypeDiv");

  return typeDiv;
}

function pickGradient(card)
{
  print("Chosing gradient...");

  let gradientColor = "";
  let gradientType = arrTypes[card["type"]].type.toLowerCase();

  print(gradientType);

  switch (gradientType)
  {
    case "bug":       gradientColor = BUG;       break;
    case "dark":      gradientColor = DARK;      break;
    case "dragon":    gradientColor = DRAGON;    break;
    case "electric":  gradientColor = ELECTRIC;  break;
    case "fairy":     gradientColor = FAIRY;     break;
    case "fighting":  gradientColor = FIGHTING;  break;
    case "fire":      gradientColor = FIRE;      break;
    case "flying":    gradientColor = FLYING;    break;
    case "ghost":     gradientColor = GHOST;     break;
    case "grass":     gradientColor = GRASS;     break;
    case "ground":    gradientColor = GROUND;    break;
    case "ice":       gradientColor = ICE;       break;
    case "normal":    gradientColor = NORMAL;    break;
    case "poison":    gradientColor = POISON;    break;
    case "psychic":   gradientColor = PSYCHIC;   break;
    case "rock":      gradientColor = ROCK;      break;
    case "steel":     gradientColor = STEEL;     break;
    case "water":     gradientColor = WATER;     break;
    default:          gradientColor = "";        break;
  } // switch

  print("Gradient chosen: " + gradientColor)
  return gradientColor;
}

function setGradient(elem, color1, color2)
{
  print("Setting gradient");

  elem.style = "background: linear-gradient(" + String(color1) + "," + String(color2) + ");";

  print("Gradient set");
}

// function scrollToBottomOfCards(){
//   divCards.scrollTop = divCards.scrollHeight;
// }

function getSelectedOption(sel)
{
  option = sel.options[sel.selectedIndex].innerHTML;
  return option;
}

function getElem(name)
{
  let elem = document.querySelector(name);
  return elem;
}

function resetForm()
{
  print("Resetting form...");

  txtCardName.value = "";
  txtAtkName1.value = "";
  txtAtkName2.value = "";
  txtHP.value       = "";

  selAtkType1.selectedIndex = 0;
  selAtkType2.selectedIndex = 0;
  selCardType.selectedIndex = 0;
  selRarity.selectedIndex   = 0;
  selSpecies.selectedIndex  = 0;

  print("Finished resetting form");
}

function isValidFormData()
{
  print("Checking for valid form data...");

  let validFormData = true;

  let reqName = document.querySelector("#reqName");
  let reqHP = document.querySelector("#reqHP");

  print("Checking HP...");

  if(txtHP.value <= 0)
  {
    reqHP.className = "error";
    validFormData = false;
    print("Invalid data found: HP <= 0");
  }
  else
  {
    reqHP.className = "reqField";
    print("HP OK");
  }

  print("Checking name...")
  if(txtCardName.value.length == 0)
  {
    reqName.className = "error";
    validFormData = false;
    print("Invalid data found: Length of name cannot be 0");
  }
  else
  {
    reqName.className = "reqField";
    print("Name OK");
  }

  print("Form data is: " + (validFormData ? "Valid" : "Invalid"));

  return validFormData;
}

function encodeFormData()
{
  print("Encoding form data...");

  let cId       = hidPokemonId.value;
  let cAtkName1 = txtAtkName1.value.trim();
  let cAtkName2 = txtAtkName2.value.trim();
  let cHP       = txtHP.value.trim();
  let cName     = txtCardName.value.trim();

  let cAtkType1 = selAtkType1.selectedIndex;
  let cAtkType2 = selAtkType2.selectedIndex;
  let cRarity   = selRarity.selectedIndex;
  let cSpecies  = selSpecies.selectedIndex + 1;
  let cType     = selCardType.selectedIndex

  if(cAtkName1 == "")
  {
    cAtkName1 = "None";
    cAtkType1 = "None";
  }
  if(cAtkName2 == "")
  {
    cAtkName2 = "None";
    cAtkType2 = "None";
  }

  let data =
  "id="       + encodeURIComponent(cId)       + "&" +
  "s_id="     + encodeURIComponent(cSpecies)  + "&" +
  "name="     + encodeURIComponent(cName)     + "&" +
  "t_id="     + encodeURIComponent(cType)     + "&" +
  "hp="       + encodeURIComponent(cHP)       + "&" +
  "atkName1=" + encodeURIComponent(cAtkName1) + "&" +
  "atkType1=" + encodeURIComponent(cAtkType1) + "&" +
  "atkName2=" + encodeURIComponent(cAtkName2) + "&" +
  "atkType2=" + encodeURIComponent(cAtkType2) + "&" +
  "rarity="   + encodeURIComponent(cRarity);

  print(data);

  print("Endcoding complete");

  return data;
}

// Get all data from form and store it for use later
function setLastCard()
{
  prevName      = txtCardName.value;
  prevHP        = txtHP.value;
  prevSpecies   = selSpecies.selectedIndex;
  prevCardType  = selCardType.selectedIndex;
  prevAtkName1  = txtAtkName1.value;
  prevAtkName2  = txtAtkName2.value;
  prevAtkType1  = selAtkType1.selectedIndex;
  prevAtkType2  = selAtkType2.selectedIndex;
}

// Set all form data to the card before update was clicked
function getLastCard()
{
  txtCardName.value         = prevName;
  txtHP.value               = prevHP;
  selSpecies.selectedIndex  = prevSpecies;
  selCardType.selectedIndex = prevCardType;
  txtAtkName1.value         = prevAtkName1;
  txtAtkName2.value         = prevAtkName2;
  selAtkType1.selectedIndex = prevAtkType1;
  selAtkType2.selectedIndex = prevAtkType2;
}

// Hide the button to add a card and show the update and cancel buttons
function switchToAddMode()
{
  btnAddCard.style.display = "inline";
  btnClearForm.style.display = "inline";
  btnUpdateCard.style.display = "none";
  btnCancelUpdate.style.display = "none";

  resetForm();
}

// Hide the update and cancel buttons and show the button to add a card
function switchToUpdateMode()
{
  btnAddCard.style.display = "none";
  btnClearForm.style.display = "none";
  btnUpdateCard.style.display = "inline";
  btnCancelUpdate.style.display = "inline";
}

// Server communications
function getCardsFromServer()
{
  print("Getting cards from server");

  // Clear all current cards for those coming from server
  arrCards = [];
  divCards.innerHTML = "";

  fetch
  (
    (serverURL + "cards"),
    {
      method: "GET",
      headers: {
        "Accept": cTypeJSON
      } // Headers
    }
  ) // fetch
  .then
  (
    function(response)
    {
      print("Cards recieved");

      let tempResponse = response.clone();
      let cards = tempResponse.json();

      return cards;
    }
  ) // then
  .then
  (
    function(cards)
    {
      print("Adding cards to array");

      cards.forEach(
        function(card){
          print(card.toString());

          arrCards.push(card);
        }
      ); // forEach

      print("Finished adding cards to array")
    }
  )
  .then
  (
    function()
    {
      print("Creating card objects");

      arrCards.forEach
      (
        function(card)
        {
          print("Current card: " + card.toString());

          let newCardImg = makeCardImg(card);
          let newCardImgContainer = makeCardImgContainer();
          let newCardTextContainer = makeCardTextContainer();
          let newCardEditButton = makeCardEditButton(card);
          let newCardDeleteButton = makeCardDeleteButton(card);
          let newCardDiv = makeCardDiv(card);
          let newNameDiv = makeNameDiv(card);
          let newHPDiv = makeHPDiv(card);
          let newSpeciesDiv = makeSpeciesDiv(card)
          let newTypeDiv = makeTypeDiv(card);
          let gradientColor = pickGradient(card);

          setGradient(newCardDiv, "#FFFFFF", gradientColor);

          newCardImgContainer.appendChild(newCardImg);

          newCardTextContainer.appendChild(newNameDiv);
          newCardTextContainer.appendChild(newHPDiv);
          newCardTextContainer.appendChild(newSpeciesDiv);
          newCardTextContainer.appendChild(newTypeDiv);

          newCardTextContainer.appendChild(newCardEditButton);
          newCardTextContainer.appendChild(newCardDeleteButton);

          newCardDiv.appendChild(newCardImgContainer);
          newCardDiv.appendChild(newCardTextContainer);

          divCards.appendChild(newCardDiv);
        }
      ); // forEach
    }
  ) // then
  .then
  (
    function()
    {
      divCards.scrollTop = divCards.scrollHeight;
    }
  ) // then
  .catch(
    function(err)
    {
      console.log(err)
    }
  );
}

function getNamesFromServer()
{
  print("Getting names from server");

  fetch
  (
    (serverURL + "names"),
    {
      method: "GET",
      headers: {
        "Accept": cTypeJSON
      }
    }
  )
  .then
  (
    function(response)
    {
      print("Names recieved");

      let tempResponse = response.clone();

      let names = tempResponse.json();

      print("Names: " + names.toString());

      return names;
    }
  )
  .then
  (
    function(names)
    {
      print("Adding names to array")
      names.forEach
      (
        function(name)
        {
          print(name);
          arrNames.push(name);
        }
      );
    }
  )
  .then
  (
    function()
    {
      print("Adding names to drop down")
      arrNames.forEach
      (
        function(name)
        {
          addOptionToSelect(selSpecies, name.id, name.name);
        }
      );
    }
  );
}

function getRaritiesFromServer()
{
  print("Getting rarities from server");

  fetch
  (
    (serverURL + "rarities"),
    {
      method: "GET",
      headers:
      {
        "Accept": cTypeJSON
      }
    }
  )
  .then
  (
    function(response)
    {
      print("Rarities recieved")
      let tempResponse = response.clone();

      let rarities = tempResponse.json();

      print(rarities);

      return rarities;
    }
  )
  .then
  (
    function(rarities)
    {
      rarities.forEach(
        function(rarity)
        {
          arrRarities.push(rarity);
        }
      );
    }
  )
  .then
  (
    function()
    {
      arrRarities.forEach
      (
        function(rarity)
        {
          addOptionToSelect(selRarity, rarity.id, rarity.rarity);
        }
      );
    }
  )
}

function getTypesFromServer()
{
  print("Getting types from server")

  fetch
  (
    (serverURL + "types"),
    {
      method: "GET",
      headers: {
        "Accept": cTypeJSON
      }
    }
  )
  .then
  (
    function(response)
    {
      print("Types recieved")
      let tempResponse = response.clone();

      let types = tempResponse.json();

      print(types);

      return types;
    }
  )
  .then
  (
    function(types)
    {
      print("Adding names to array")
      types.forEach(
        function(type){
          arrTypes.push(type);
        }
      );
    }
  )
  .then
  (
    function()
    {
      print("Adding names to drop down")
      arrTypes.forEach
      (
        function(type)
        {
          addOptionToSelect(selAtkType1, type.id, type.type);
          addOptionToSelect(selAtkType2, type.id, type.type);
          addOptionToSelect(selCardType, type.id, type.type);
        }
      );
    }
  )
}
//////////////////////////////////////////////////
////////// End function definitions //////////////
//////////////////////////////////////////////////


getNamesFromServer();
getTypesFromServer();
getRaritiesFromServer();
getCardsFromServer();
setEventHandlers();
