// Adam Manning 2021

const serverURL = "http://localhost:8080/";

// Content types
const cTypeFormEncodedData = "application/x-www-form-urlencoded";
const cTypeJSON = "application/json";

// REST Methods
const methodPOST = "POST";
const methodGET = "GET";
const methodPUT = "PUT";
const methodPATCH = "PATCH";
const methodDELETE = "DELETE";

// Card keys
const cardIDStr        = "id";
const cardSpecIDStr    = "s_id";
const cardNameStr      = "name";
const cardTypeIDStr    = "type";
const cardHPStr        = "hp";
const cardAtkName1Str  = "atkName1";
const cardAtkName2Str  = "atkName2";
const cardAtkType1Str  = "atkType1";
const cardAtkType2Str  = "atkType2";
const cardRarityStr    = "rarity";

// Color to change the background of card depending on its type
const COLOR_BUG       = "#A8B820";
const COLOR_DARK      = "#705848";
const COLOR_DRAGON    = "#7038F8";
const COLOR_ELECTRIC  = "#F8D030";
const COLOR_FAIRY     = "#EE99AC";
const COLOR_FIGHTING  = "#C03028";
const COLOR_FIRE      = "#F08030";
const COLOR_FLYING    = "#A890F0";
const COLOR_GHOST     = "#705898";
const COLOR_GRASS     = "#78C850";
const COLOR_GROUND    = "#E0C068";
const COLOR_ICE       = "#98D8D8";
const COLOR_NORMAL    = "#A8A878";
const COLOR_POISON    = "#A040A0";
const COLOR_PSYCHIC   = "#F85888";
const COLOR_ROCK      = "#B8A038";
const COLOR_STEEL     = "#B8B8D0";
const COLOR_WATER     = "#6890F0";

// Location of image files
const imgDir = "img/"

// Divs
var divCards = getElem("#cards");

// Text inputs
var txtCardName = getElem("#card_name");
var txtAtkName1 = getElem("#atkName1");
var txtAtkName2 = getElem("#atkName2");
var txtHP       = getElem("#pokemon_hp");

// Select inputs - drop down menues
var selAtkType1 = getElem("#atkType1");
var selAtkType2 = getElem("#atkType2");
var selCardType = getElem("#pokemon_type");
var selRarity   = getElem("#rarity");
var selSpecies  = getElem("#pokemon_species");

// Hidden inputs
var hidPokemonId = getElem("#p_id");

// Arrays
var arrCards    = []; // Used to store the card objects retrieved from database
var arrNames    = []; // Used to store the names of all pokemon in database
var arrRarities = []; // Used to store all possible rarities from database
var arrTypes    = []; // Used to store all possible types from database

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
function log(arg)
{
  if(outputFlag)
  {
    console.log("[***LOG:  " + arg + "***]");
  }
}

// Event handler - Handles adding a card to the database
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
        method: methodPOST,
        headers:
        {
          "Content-Type": cTypeFormEncodedData
        }
      }
    );
    resetForm();

    getCardsFromServer();
  } // End if(validFormData)
} // End btnAddCardOnClick()

// Event handler - clears the form when the "Clear Form" button is clicked
function btnClearFormOnClick()
{
  resetForm();
  log("Form reset");
}

// Event handler - Sends updated card details to server when the update button is clicked
function btnUpdateCardOnClick()
{
  if(isValidFormData()){
    log("Form data is valid");

    let data = encodeFormData();

    fetch
    (
      (serverURL + "cards/" + "card" + hidPokemonId.value),
      {
        body: data,
        method: methodPUT,
        headers:
        {
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
  log("Setting event handlers...");

  btnAddCard.onclick      = btnAddCardOnClick;
  btnClearForm.onclick    = btnClearFormOnClick;
  btnUpdateCard.onclick   = btnUpdateCardOnClick;
  btnCancelUpdate.onclick = btnCancelUpdateOnClick;

  log("Finished setting event handlers");
}

// Creates a <button> element
function makeButton()
{
  log("Creating <button>");

  let button = document.createElement("button");

  log("Finished creating <button>")

  return button;
}

// Creates a <div> element
function makeDiv()
{
  log("Creating <div>")

  let div = document.createElement("div");

  log("Finished creating <div>")

  return div;
}

// Creates a <img> element
function makeImg()
{
  log("Creating <img>")

  let img = document.createElement("img");

  log("Finished creating <img>")

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
  log("Creating CardImg");

  let img = makeImg();
  img.className = "cardImg";

  let id = card[cardSpecIDStr];
  log("Species: " + id);

  img.src = imgDir + id + ".gif";
  img.alt = arrNames[id - 1].name; //Should subtract 1

  log("Finished creating CardImg");

  return img;
}

function makeCardImgContainer()
{
  log("Creating CardImageContainer");

  let imgContainer = makeDiv();
  imgContainer.className = "cardImgContainer";

  log("Finished creating CardImageContainer");

  return imgContainer;
}

function makeCardTextContainer()
{
  log("Creating CardTextContainer");

  let txtContainer = makeDiv();
  txtContainer.className = "cardTextContainer";

  log("Finished creating CardTextContainer");

  return txtContainer;
}

function makeCardEditButton(card){
  log("Creating CardEditButton");

  let editButton = makeButton();
  editButton.innerHTML = "Edit Details"
  editButton.onclick = function()
  {
    log("Editing card with id(" + card[cardIDStr] + ")");

    txtCardName.value = card[cardNameStr];
    txtHP.value = card[cardHPStr];

    if(card[cardAtkName1Str] == "None")
    {
      txtAtkName1.value = "";
    }
    else
    {
      txtAtkName1.value = card[cardAtkName2Str];
    }

    if(card[cardAtkName2Str] == "None")
    {
      txtAtkName2.value = "";
    }
    else
    {
      txtAtkName2.value = card[cardAtkName2Str];
    }

    selSpecies.selectedIndex  = card[cardSpecIDStr] - 1;
    selCardType.selectedIndex = card[cardTypeIDStr];
    selAtkType1.selectedIndex = card[cardAtkType1Str];
    selAtkType2.selectedIndex = card[cardAtkType2Str];
    selRarity.selectedIndex   = card[cardRarityStr];

    hidPokemonId.value = card[cardIDStr];

    setLastCard();
    switchToUpdateMode();
  } // newCardEditButton.onclick

  log("Finished creating CardEditButton");
  return editButton;
}

function makeCardDeleteButton(card)
{
  log("Creating CardDeleteButton");

  let deleteButton = makeButton();
  deleteButton.innerHTML = "Delete Card";
  deleteButton.onclick = function()
  {
    let willDelete = confirm("Are you sure you want to delete " + card[cardNameStr] + "?");

    if(willDelete)
    {
      log(willDelete);

      fetch
      (
        (serverURL + "cards/" + "card" +  card[cardIDStr]),
        {
          method: methodDELETE
        }
      )
      .then
      (
        function(response)
        {
          let tempResponse = response.clone();

          log(tempResponse);

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

  log("Finished creating CardDeleteButton");

  return deleteButton;
}

function makeCardDiv(card)
{
  log("Creating CardDiv");

  let cardDiv = makeDiv();
  cardDiv.className = "cardDiv";
  cardDiv.id = "card" + arrNames[card[cardSpecIDStr]];

  log("Finished creating CardDiv");

  return cardDiv;
}

function makeNameDiv(card)
{
  log("Creating NameDiv");

  let nameDiv = makeDiv();
  nameDiv.innerHTML = "Name: " + card[cardNameStr];

  log("Finished creating NameDiv");

  return nameDiv;
}

function makeHPDiv(card)
{
  log("Creating HPDiv");

  let hpDiv = makeDiv();
  hpDiv.innerHTML = "HP: " + card[cardHPStr];

  log("Finished creating HPDiv");

  return hpDiv;
}

function makeSpeciesDiv(card)
{
  log("Creating SpeciesDiv");

  let speciesDiv = makeDiv();
  speciesDiv.innerHTML = "Species: " + arrNames[card[cardSpecIDStr] - 1].name;


  log("Finished creating SpeciesDiv");

  return speciesDiv;
}

function makeAttack1Div(card)
{
  log("Creating Attack1Div");

  let attack1Div = makeDiv();
  attack1Div.innerHTML = "Atttack 1: " + card[cardAtkName1Str];

  log("Finished creating Attack1Div");

  return attack1Div;
}

function makeAttack2Div(card)
{
  log("Creating Attack2Div");

  let attack1Div = makeDiv();
  attack1Div.innerHTML = "Atttack 2: " + card[cardAtkName2Str];

  log("Finished creating Attack2Div");

  return attack1Div;
}

function makeRarityDiv(card)
{
  log("Creating RarityDiv");

  let rarityDiv = makeDiv();
  rarityDiv.innerHTML = "Rarity: " + arrRarities[card[cardRarityStr]][cardRarityStr];

  log("Finished creating Rarity");

  return rarityDiv;
}

function makeTypeDiv(card)
{
  log("Creating TypeDiv");

  let typeDiv = makeDiv();
  typeDiv.innerHTML = "Type: " + arrTypes[card[cardTypeIDStr]].type;

  log("Finished creating TypeDiv");

  return typeDiv;
}

function pickGradient(card)
{
  log("Chosing gradient...");

  let gradientColor = "";
  let gradientType = arrTypes[card[cardTypeIDStr]].type.toLowerCase();

  log(gradientType);

  switch (gradientType)
  {
    case "bug":       gradientColor = COLOR_BUG;       break;
    case "dark":      gradientColor = COLOR_DARK;      break;
    case "dragon":    gradientColor = COLOR_DRAGON;    break;
    case "electric":  gradientColor = COLOR_ELECTRIC;  break;
    case "fairy":     gradientColor = COLOR_FAIRY;     break;
    case "fighting":  gradientColor = COLOR_FIGHTING;  break;
    case "fire":      gradientColor = COLOR_FIRE;      break;
    case "flying":    gradientColor = COLOR_FLYING;    break;
    case "ghost":     gradientColor = COLOR_GHOST;     break;
    case "grass":     gradientColor = COLOR_GRASS;     break;
    case "ground":    gradientColor = COLOR_GROUND;    break;
    case "ice":       gradientColor = COLOR_ICE;       break;
    case "normal":    gradientColor = COLOR_NORMAL;    break;
    case "poison":    gradientColor = COLOR_POISON;    break;
    case "psychic":   gradientColor = COLOR_PSYCHIC;   break;
    case "rock":      gradientColor = COLOR_ROCK;      break;
    case "steel":     gradientColor = COLOR_STEEL;     break;
    case "water":     gradientColor = COLOR_WATER;     break;
    default:          gradientColor = "#000000";              break;
  } // switch

  log("Gradient chosen: " + gradientColor)
  return gradientColor;
}

function setGradient(elem, color1, color2)
{
  log("Setting gradient");

  elem.style = "background: linear-gradient(" + String(color1) + "," + String(color2) + ");";

  log("Gradient set");
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
  log("Resetting form...");

  txtCardName.value = "";
  txtAtkName1.value = "";
  txtAtkName2.value = "";
  txtHP.value       = "";

  selAtkType1.selectedIndex = 0;
  selAtkType2.selectedIndex = 0;
  selCardType.selectedIndex = 0;
  selRarity.selectedIndex   = 0;
  selSpecies.selectedIndex  = 0;

  log("Finished resetting form");
}

function isValidFormData()
{
  log("Checking for valid form data...");

  let validFormData = true;

  let reqName = document.querySelector("#reqName");
  let reqHP = document.querySelector("#reqHP");

  log("Checking HP...");

  if(txtHP.value <= 0)
  {
    reqHP.className = "error";
    validFormData = false;
    log("Invalid data found: HP <= 0");
  }
  else
  {
    reqHP.className = "reqField";
    log("HP OK");
  }

  log("Checking name...")
  if(txtCardName.value.length == 0)
  {
    reqName.className = "error";
    validFormData = false;
    log("Invalid data found: Length of name cannot be 0");
  }
  else
  {
    reqName.className = "reqField";
    log("Name OK");
  }

  log("Form data is: " + (validFormData ? "Valid" : "Invalid"));

  return validFormData;
}

function encodeFormData()
{
  log("Encoding form data...");

  let tempId       = hidPokemonId.value;
  let tempAtkName1 = txtAtkName1.value.trim();
  let tempAtkName2 = txtAtkName2.value.trim();
  let tempHP       = txtHP.value.trim();
  let tempName     = txtCardName.value.trim();

  let tempAtkType1 = selAtkType1.selectedIndex;
  let tempAtkType2 = selAtkType2.selectedIndex;
  let tempRarity   = selRarity.selectedIndex;
  let tempSpecies  = selSpecies.selectedIndex + 1;
  let tempType     = selCardType.selectedIndex

  if(tempAtkName1 == "")
  {
    tempAtkName1 = "None";
    tempAtkType1 = "None";
  }
  if(tempAtkName2 == "")
  {
    tempAtkName2 = "None";
    tempAtkType2 = "None";
  }

  let data =
  cardIDStr       + "=" + encodeURIComponent(tempId)       + "&" +
  cardSpecIDStr   + "=" + encodeURIComponent(tempSpecies)  + "&" +
  cardNameStr     + "=" + encodeURIComponent(tempName)     + "&" +
  cardTypeIDStr   + "=" + encodeURIComponent(tempType)     + "&" +
  cardHPStr       + "=" + encodeURIComponent(tempHP)       + "&" +
  cardAtkName1Str + "=" + encodeURIComponent(tempAtkName1) + "&" +
  cardAtkType1Str + "=" + encodeURIComponent(tempAtkType1) + "&" +
  cardAtkName2Str + "=" + encodeURIComponent(tempAtkName2) + "&" +
  cardAtkType2Str + "=" + encodeURIComponent(tempAtkType2) + "&" +
  cardRarityStr   + "="  + encodeURIComponent(tempRarity);

  log(data);

  log("Endcoding complete");

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
  log("Getting cards from server");

  // Clear all current cards for those coming from server
  arrCards = [];
  divCards.innerHTML = "";

  fetch
  (
    (serverURL + "cards"),
    {
      method: methodGET,
      headers:
      {
        "Accept": cTypeJSON
      } // Headers
    }
  ) // fetch
  .then
  (
    function(response)
    {
      log("Cards recieved");

      let tempResponse = response.clone();
      let cards = tempResponse.json();

      return cards;
    }
  ) // then
  .then
  (
    function(cards)
    {
      log("Adding cards to array");

      cards.forEach
      (
        function(card)
        {
          log(card.toString());

          arrCards.push(card);
        }
      ); // forEach

      log("Finished adding cards to array");
    }
  )
  .then
  (
    function()
    {
      log("Creating card objects");

      arrCards.forEach
      (
        function(card)
        {
          log("Current card: " + card.toString());

          let newCardImg = makeCardImg(card);
          let newCardImgContainer = makeCardImgContainer();
          let newCardTextContainer = makeCardTextContainer();
          let newCardEditButton = makeCardEditButton(card);
          let newCardDeleteButton = makeCardDeleteButton(card);
          let newCardDiv = makeCardDiv(card);
          let newNameDiv = makeNameDiv(card);
          let newHPDiv = makeHPDiv(card);
          let newAttack1Div = makeAttack1Div(card);
          let newAttack2Div = makeAttack2Div(card);
          let newSpeciesDiv = makeSpeciesDiv(card)
          let newTypeDiv = makeTypeDiv(card);
          let newRarityDiv = makeRarityDiv(card);
          let gradientColor = pickGradient(card);

          setGradient(newCardDiv, "#FFFFFF", gradientColor);

          newCardImgContainer.appendChild(newCardImg);

          newCardTextContainer.appendChild(newNameDiv);
          newCardTextContainer.appendChild(newHPDiv);
          newCardTextContainer.appendChild(newSpeciesDiv);
          newCardTextContainer.appendChild(newAttack1Div);
          newCardTextContainer.appendChild(newAttack2Div);
          newCardTextContainer.appendChild(newTypeDiv);
          newCardTextContainer.appendChild(newRarityDiv);
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
  .catch
  (
    function(err)
    {
      console.log(err)
    }
  );
}

function getNamesFromServer()
{
  log("Getting names from server");

  fetch
  (
    (serverURL + "names"),
    {
      method: methodGET,
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
      log("Names recieved");

      let tempResponse = response.clone();

      let names = tempResponse.json();

      log("Names: " + names.toString());

      return names;
    }
  )
  .then
  (
    function(names)
    {
      log("Adding names to array")
      names.forEach
      (
        function(name)
        {
          log(name);
          arrNames.push(name);
        }
      );
    }
  )
  .then
  (
    function()
    {
      log("Adding names to drop down")
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
  log("Getting rarities from server");

  fetch
  (
    (serverURL + "rarities"),
    {
      method: methodGET,
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
      log("Rarities recieved")
      let tempResponse = response.clone();

      let rarities = tempResponse.json();

      log(rarities);

      return rarities;
    }
  )
  .then
  (
    function(rarities)
    {
      log("Adding rarities to array");

      rarities.forEach
      (
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
      log("Adding rarities to drop down");

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
  log("Getting types from server")

  fetch
  (
    (serverURL + "types"),
    {
      method: methodGET,
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
      log("Types recieved")
      let tempResponse = response.clone();

      let types = tempResponse.json();

      log(types);

      return types;
    }
  )
  .then
  (
    function(types)
    {
      log("Adding types to array")
      types.forEach
      (
        function(type)
        {
          arrTypes.push(type);
        }
      );
    }
  )
  .then
  (
    function()
    {
      log("Adding types to drop downs")
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
