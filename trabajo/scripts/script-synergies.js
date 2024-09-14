//##############################################################################################//
//# Authors: Mateo Peña Costa and Raquel Cámara Domene
//# Description: Script to handle the sinergies of the characters and emblems, 
//#              and to recommend characters based on the selected sinergies and level.
//##############################################################################################//

//#########################################//
//DATABASE OF CHAMPS, EMBLEMS AND SYNERGIES//
//#########################################//
const personajes = {
    1: { name: 'Ahri', sinergias: ['Scholar', 'Arcana'], coste: 2 },
    5: { name: 'Akali', sinergias: ['Pyro', 'Multistriker', 'Warrior'], coste: 2 },
    10: { name: 'Ashe', sinergias: ['Eldritch', 'Multistriker'], coste: 1  },
    14: { name: 'Bard', sinergias: ['Sugarcraft', 'Preserver', 'Scholar'], coste: 3 },
    19: { name: 'Blitzcrank', sinergias: ['Honeymancy', 'Vanguard'], coste: 1 },
    23: { name: 'Briar', sinergias: ['Eldritch', 'Ravenous', 'Shapeshifter'], coste: 5 },
    28: { name: 'Camille', sinergias: ['Chrono', 'Multistriker'], coste: 5 },
    32: { name: 'Cassiopeia', sinergias: ['Witchcraft', 'Incantor'], coste: 2 },
    36: { name: 'Diana', sinergias: ['Frost', 'Bastion'], coste: 5 },
    40: { name: 'Elise', sinergias: ['Eldritch', 'Shapeshifter'], coste: 1 },
    44: { name: 'Ezreal', sinergias: ['Portal', 'Blaster'], coste: 3 },
    48: { name: 'Fiora', sinergias: ['Witchcraft', 'Warrior'], coste: 4 },
    52: { name: 'Galio', sinergias: ['Portal', 'Mage', 'Vanguard'], coste: 2 },
    57: { name: 'Gwen', sinergias: ['Sugarcraft', 'Warrior'], coste: 4 },
    61: { name: 'Hecarim', sinergias: ['Arcana', 'Bastion', 'Multistriker'], coste: 3 },
    66: { name: 'Hwei', sinergias: ['Frost', 'Blaster'], coste: 3 },
    70: { name: 'Jax', sinergias: ['Chrono', 'Multistriker'], coste: 1 },
    74: { name: 'Jayce', sinergias: ['Portal', 'Shapeshifter'], coste: 1 },
    78: { name: 'Jinx', sinergias: ['Sugarcraft', 'Hunter'], coste: 3 },
    82: { name: 'Kalista', sinergias: ['Faerie', 'Multistriker'], coste: 4 },
    86: { name: 'Karma', sinergias: ['Chrono', 'Incantor'], coste: 4 },
    90: { name: 'Kassadin', sinergias: ['Portal', 'Multistriker'], coste: 2 },
    94: { name: 'Katarina', sinergias: ['Faerie', 'Warrior'], coste: 3 },
    98: { name: 'KogMaw', sinergias: ['Honeymancy', 'Hunter'], coste: 2 },
    102: { name: 'Lillia', sinergias: ['Faerie', 'Bastion'], coste: 1 },
    106: { name: 'Milio', sinergias: ['Faerie', 'Scholar'], coste: 5 },
    110: { name: 'Mordekaiser', sinergias: ['Eldritch', 'Vanguard'], coste: 3 },
    114: { name: 'Morgana', sinergias: ['Witchcraft', 'BatQueen', 'Preserver'], coste: 5 },
    119: { name: 'Nami', sinergias: ['Eldritch', 'Mage'], coste: 4 },
    123: { name: 'Nasus', sinergias: ['Pyro', 'Shapeshifter'], coste: 4 },
    127: { name: 'Neeko', sinergias: ['Witchcraft', 'Shapeshifter'], coste: 3 },
    131: { name: 'Nilah', sinergias: ['Eldritch', 'Warrior'], coste: 2 },
    135: { name: 'Nomsy', sinergias: ['Dragon', 'Hunter'], coste: 1 },
    139: { name: 'Norra', sinergias: ['Portal', 'BestFriends', 'Mage'], coste: 5 },
    144: { name: 'Nunu&Willump', sinergias: ['Honeymancy', 'Bastion'], coste: 2 },
    148: { name: 'Olaf', sinergias: ['Frost', 'Hunter'], coste: 4 },
    152: { name: 'Poppy', sinergias: ['Witchcraft', 'Bastion'], coste: 1 },
    156: { name: 'Rakan', sinergias: ['Faerie', 'Preserver'], coste: 4 },
    160: { name: 'Rumble', sinergias: ['Sugarcraft', 'Blaster', 'Vanguard'], coste: 2 },
    165: { name: 'Ryze', sinergias: ['Portal', 'Scholar'], coste: 5 },
    169: { name: 'Seraphine', sinergias: ['Faerie', 'Mage'], coste: 1 },
    173: { name: 'Shen', sinergias: ['Pyro', 'Bastion'], coste: 3 },
    177: { name: 'Shyvana', sinergias: ['Dragon', 'Shapeshifter'], coste: 2 },
    181: { name: 'Smolder', sinergias: ['Dragon', 'Blaster'], coste: 5 },
    185: { name: 'Soraka', sinergias: ['Sugarcraft', 'Mage'], coste: 1 },
    189: { name: 'Swain', sinergias: ['Frost', 'Shapeshifter'], coste: 3 },
    193: { name: 'Syndra', sinergias: ['Eldritch', 'Incantor'], coste: 2 },
    197: { name: 'TahmKench', sinergias: ['Arcana', 'Vanguard'], coste: 4 },
    201: { name: 'Taric', sinergias: ['Portal', 'Bastion'], coste: 4 },
    205: { name: 'Tristana', sinergias: ['Faerie', 'Blaster'], coste: 2 },
    209: { name: 'Twitch', sinergias: ['Frost', 'Hunter'], coste: 1 },
    213: { name: 'Varus', sinergias: ['Pyro', 'Blaster'], coste: 4 },
    217: { name: 'Veigar', sinergias: ['Honeymancy', 'Mage'], coste: 3 },
    221: { name: 'Vex', sinergias: ['Chrono', 'Mage'], coste: 3 },
    225: { name: 'Warwick', sinergias: ['Frost', 'Vanguard'], coste: 1 },
    229: { name: 'Wukong', sinergias: ['Druid'], coste: 3 },
    232: { name: 'Xerath', sinergias: ['Arcana', 'Ascendant'], coste: 5 },
    236: { name: 'Ziggs', sinergias: ['Honeymancy', 'Incantor'], coste: 1 },
    240: { name: 'Zilean', sinergias: ['Chrono', 'Frost', 'Preserver'], coste: 2 },
    245: { name: 'Zoe', sinergias: ['Portal', 'Witchcraft', 'Scholar'], coste: 1 },
};

const emblemas = {
    1: { name: 'Eldritch', sinergias: ['Eldritch'] },
    2: { name: 'Faerie', sinergias: ['Faerie'] },
    3: { name: 'Frost', sinergias: ['Frost'] },
    4: { name: 'Honeymancy', sinergias: ['Honeymancy'] },
    5: { name: 'Portal', sinergias: ['Portal'] },
    6: { name: 'Pyro', sinergias: ['Pyro'] },
    7: { name: 'Sugarcraft', sinergias: ['Sugarcraft'] },
    8: { name: 'Witchcraft', sinergias: ['Witchcraft'] },
    9: { name: 'Arcana', sinergias: ['Arcana'] },
    10: { name: 'Bastion', sinergias: ['Bastion'] },
    11: { name: 'Blaster', sinergias: ['Blaster'] },
    12: { name: 'Chrono', sinergias: ['Chrono'] },
    13: { name: 'Hunter', sinergias: ['Hunter'] },
    14: { name: 'Incantor', sinergias: ['Incantor'] },
    15: { name: 'Mage', sinergias: ['Mage'] },
    16: { name: 'Multistriker', sinergias: ['Multistriker'] },
    17: { name: 'Preserver', sinergias: ['Preserver'] },
    18: { name: 'Scholar', sinergias: ['Scholar'] },
    19: { name: 'Shapeshifter', sinergias: ['Shapeshifter'] },
    20: { name: 'Vanguard', sinergias: ['Vanguard'] },
    21: { name: 'Warrior', sinergias: ['Warrior'] }
};

const sinergias = {
    Scholar: { cantidadPosible: ['2 / 4 / 6'] },
    Arcana: { cantidadPosible: ['2 / 3 / 4 / 5'] },
    Pyro: { cantidadPosible: ['2 / 3 / 4 / 5'] },
    Multistriker: { cantidadPosible: ['3 / 5 / 7 / 9'] },
    Warrior: { cantidadPosible: ['2 / 4 / 6'] },
    Eldritch: { cantidadPosible: ['3 / 5 / 7 / 10'] },
    Ravenous: { cantidadPosible: ['1'] },
    Shapeshifter: { cantidadPosible: ['2 / 4 / 6 / 8'] },
    Chrono: { cantidadPosible: ['2 / 4 / 6'] },
    Witchcraft: { cantidadPosible: ['2 / 4 / 6 / 8'] },
    Incantor: { cantidadPosible: ['2 / 4'] },
    Frost: { cantidadPosible: ['3 / 5 / 7 / 9'] },
    Bastion: { cantidadPosible: ['2 / 4 / 6 / 8'] },
    Portal: { cantidadPosible: ['3 / 6 / 8 / 10'] },
    Blaster: { cantidadPosible: ['2 / 4 / 6'] },
    Hunter: { cantidadPosible: ['2 / 4 / 6'] },
    Mage: { cantidadPosible: ['3 / 5 / 7 / 9'] },
    Vanguard: { cantidadPosible: ['2 / 4 / 6'] },
    Sugarcraft: { cantidadPosible: ['2 / 4 / 6'] },
    Preserver: { cantidadPosible: ['2 / 3 / 4 / 5'] },
    Honeymancy: { cantidadPosible: ['3 / 5 / 7'] },
    Dragon: { cantidadPosible: ['2 / 3'] },
    Faerie: { cantidadPosible: ['2 / 4 / 6 / 8'] },
    BatQueen: { cantidadPosible: ['1'] },
    Ascendant: { cantidadPosible: ['1'] },
    BestFriends: { cantidadPosible: ['1'] },
    Druid: { cantidadPosible: ['1'] }
};
//#################//



//################//
//GLOBAL VARIABLES//
//################//
let sinergiasContainer = {}; //Container for active synergies

let personajesSeleccionadosID = new Array(12).fill(0); //Arrays to store the id of selected characters on theirs positions
let personajesSeleccionados = new Array(246).fill(0); //Array to store the number of times a character has been selected

let tope = 0; //Count of selected emblems
let emblemasSeleccionadosID = new Array(5).fill(0); //Arrays to store the id of selected emblems on theirs positions
let emblemasSeleccionados = new Array(12).fill(0); //Array to store the number of times a emblem has been selected
//#################//



//##################//
//SYNERGIE FUNCTIONS//
//##################//
//Function to handle the click on a character (add theirs sinergies to the container)
function handleClickChamp(id, posicion) {

    //If the character is already selected, increase the count and return
    if (personajesSeleccionados[id] > 0) {
        personajesSeleccionados[id]++;
        personajesSeleccionadosID[posicion] = id;
        return;
    }

    personajesSeleccionados[id]++; //Increase the count of the character
    personajesSeleccionadosID[posicion] = id; //Store the character id in the position

    let sinergias = personajes[id].sinergias;

    //Add the sinergies to the container
    sinergias.forEach(sinergia => {
        if (sinergiasContainer[sinergia]) {
            sinergiasContainer[sinergia]++;
        } 
        else {
            sinergiasContainer[sinergia] = 1;
        }
    });

    updateSynergiesContainer();
}

//Function to remove the sinergies of a character from the container
function removeChamp(posicion) {
    let id = personajesSeleccionadosID[posicion];

    personajesSeleccionadosID[posicion] = 0;
    //If the character is duplicated, return
    if (personajesSeleccionadosID.includes(id)) {
        return;
    }

    let sinergias = personajes[id].sinergias;

    //Remove the sinergies from the container
    sinergias.forEach(sinergia => {
        if (sinergiasContainer[sinergia]) {
            sinergiasContainer[sinergia]--;
            if (sinergiasContainer[sinergia] === 0) {
                delete sinergiasContainer[sinergia];
            }
        }
    });

    personajesSeleccionados[id] = 0; //Reset the character position
    personajesSeleccionadosID[posicion] = 0; //Reset the character id in the position

    updateSynergiesContainer();
}

//Function to handle the click on a emblem (add theirs sinergies to the container)
function handleClickEmblem(id, posicion) {
    //Check if the limit of emblems is reached
    if(tope == 5){
        return;
    }

    tope++;
    emblemasSeleccionados[id]++; //Increase the count of the emblem
    emblemasSeleccionadosID[posicion] = id; //Store the emblem id in the position

    let sinergias = emblemas[id].sinergias;

    //Add the sinergies to the container
    sinergias.forEach(sinergia => {
        if (sinergiasContainer[sinergia]) {
            sinergiasContainer[sinergia]++;
        } else {
            sinergiasContainer[sinergia] = 1;
        }
    });

    updateSynergiesContainer();
}

//Function to remove the sinergies of a emblem from the container
function removeEmblem(posicion) {
    tope--;

    let id = emblemasSeleccionadosID[posicion];
    let sinergias = emblemas[emblemasSeleccionadosID[posicion]].sinergias;

    //Remove the sinergies from the container
    sinergias.forEach(sinergia => {
        if (sinergiasContainer[sinergia]) {
            sinergiasContainer[sinergia]--;
            if (sinergiasContainer[sinergia] === 0) {
                delete sinergiasContainer[sinergia];
            }
        }
    });

    emblemasSeleccionados[id] = 0; //Reset the emblem position
    emblemasSeleccionadosID[posicion] = 0; //Reset the emblem id in the position

    updateSynergiesContainer();
}

//Function to update the sinergies container
function updateSynergiesContainer() {
    let container = document.querySelector('.sinergias-container');
    container.innerHTML = ''; //Clear the container

    let emblDivs = [];

    //Create the divs for each sinergie
    for (let sinergia in sinergiasContainer) {
        //Create main div
        let emblDiv = document.createElement('div');
        emblDiv.className = 'embl';

        //Create number of times the sinergie is active
        let numDiv = document.createElement('div');
        numDiv.className = 'num';
        numDiv.textContent = `${sinergiasContainer[sinergia]}`;

        //Create the sinergie name
        let synerDiv = document.createElement('div');
        synerDiv.className = 'syner';
        synerDiv.textContent = `${sinergia}`;

        //Create the levels of the sinergie
        let cantidadDiv = document.createElement('div');
        cantidadDiv.className = 'cantPosible';
        cantidadDiv.textContent = `${sinergias[sinergia].cantidadPosible.join(' / ')}`;

        //Create the image of the sinergie
        let imgDiv = document.createElement('img');
        imgDiv.className = 'imag';
        //Check if the sinergie is Mage or Shapeshifter to change the image format (excepcional cases)
        if (sinergia == "Mage" || sinergia == "Shapeshifter") {
            imgDiv.src = `base_datos/imagenes/synergies/${sinergia}_TFT_icon.svg`;
        }
        else {
            imgDiv.src = `base_datos/imagenes/synergies/${sinergia}_TFT_icon.webp`;
        }
        imgDiv.alt = sinergia;

        //Add the elements to the main div
        emblDiv.appendChild(imgDiv);
        emblDiv.appendChild(numDiv);
        emblDiv.appendChild(synerDiv);
        emblDiv.appendChild(cantidadDiv);

        //Add the div to the array
        emblDivs.push({ element: emblDiv, count: sinergiasContainer[sinergia] });
    }

    //Sort the divs by the number of times the sinergie is active
    emblDivs.sort((a, b) => b.count - a.count);  /* provided by AI */

    //Add the divs to the container
    emblDivs.forEach(item => container.appendChild(item.element));
}


//Add the event listeners to the characters and emblems
document.querySelectorAll('.champ-2 img').forEach((img, index) => {
    img.addEventListener('click', () => {
        let posicion = obtainPositionInContainerChamp();
        handleClickChamp(index + 1, posicion);
    });
});

document.querySelectorAll('.champ_menu .champ').forEach((div, index) => {
    div.addEventListener('click', () => removeChamp(index));
});

document.querySelectorAll('.embl-2 img').forEach((img, index) => {
    img.addEventListener('click', () => {
        let posicion = obtainPositionInContainerEmblem();
        handleClickEmblem(index + 1, posicion);
    });
});

document.querySelectorAll('.emblem .embl-1').forEach((div, index) => {
    div.addEventListener('click', () => removeEmblem(index));
});

//Aux Function to get the position of the first empty div in the character container
function obtainPositionInContainerChamp() {
    let container = document.querySelector('.champ_menu');
    let champs = container.querySelectorAll('.champ');
    for (let i = 0; i < champs.length; i++) {
        if (personajesSeleccionadosID[i] === 0) {
            return i;
        }
    }
    return -1; //If the position is not found
}

//Aux Function to get the position of the first empty div in the emblem container
function obtainPositionInContainerEmblem() {
    let container = document.querySelector('.emblem-title-container .emblem');
    let emblemas = container.querySelectorAll('.embl-1, .embl-2');
    for (let i = 0; i < emblemas.length; i++) {
        if (emblemasSeleccionadosID[i] === 0) {
            return i;
        }
    }
    return -1; //If the position is not found
}
//#################//


//########################//
//RECOMMENDATION FUNCTIONS//
//########################//
//Aux Function for the button to recommend characters
function recommendChamps() {
    let nivel = parseInt(document.getElementById('nivel').value);
    findBestChamps(nivel);
}

//Add the event listeners to the characters and emblems
document.querySelectorAll('.champ-2 img').forEach((img) => {
    img.addEventListener('click', () => {
        let nivel = parseInt(document.getElementById('nivel').value);
        findBestChamps(nivel);
    });
});

document.querySelectorAll('.embl-2 img').forEach((img) => {
    img.addEventListener('click', () => {
        let nivel = parseInt(document.getElementById('nivel').value);
        findBestChamps(nivel);
    });
});

document.querySelectorAll('.champ_menu .champ').forEach((img) => {
    img.addEventListener('click', () => {
        let nivel = parseInt(document.getElementById('nivel').value);
        findBestChamps(nivel);
    });
});

document.querySelectorAll('.emblem .embl-1').forEach((img) => {
    img.addEventListener('click', () => {
        let nivel = parseInt(document.getElementById('nivel').value);
        findBestChamps(nivel);
    });
});

//Function to find the best characters to recommend
function findBestChamps(nivel) {
    let mejoresChamps = [];
    let maxSinergiasActivas = 0;

    //Probabilities of appearance for each level and cost
    const probabilidades = {
        1: { 1: 1, 2: 0, 3: 0, 4: 0, 5: 0 },
        2: { 1: 1, 2: 0, 3: 0, 4: 0, 5: 0 },
        3: { 1: 0.75, 2: 0.25, 3: 0, 4: 0, 5: 0 },
        4: { 1: 0.55, 2: 0.30, 3: 0.15, 4: 0, 5: 0 },
        5: { 1: 0.45, 2: 0.33, 3: 0.20, 4: 0.02, 5: 0 },
        6: { 1: 0.30, 2: 0.40, 3: 0.25, 4: 0.05, 5: 0 },
        7: { 1: 0.19, 2: 0.30, 3: 0.35, 4: 0.10, 5: 0.01 },
        8: { 1: 0.18, 2: 0.25, 3: 0.36, 4: 0.18, 5: 0.03 },
        9: { 1: 0.10, 2: 0.20, 3: 0.25, 4: 0.35, 5: 0.10 },
        10: { 1: 0.05, 2: 0.10, 3: 0.20, 4: 0.40, 5: 0.25 },
        11: { 1: 0.01, 2: 0.02, 3: 0.12, 4: 0.50, 5: 0.35 }
    };

    //Iterate over the characters
    for (let id in personajes) {
        //Check if the character is already selected (don't recommend it)
        if (!personajesSeleccionadosID.includes(parseInt(id))) {
            let personaje = personajes[id];
            let sinergias = personaje.sinergias;
            let sinergiasActivas = 0;

            //Count the ammount of synergies that it activates
            sinergias.forEach(sinergia => {
                if (sinergiasContainer[sinergia]) {
                    sinergiasActivas++;
                }
            });

            //Check if the character can appear at the level
            if (probabilidades[nivel][personaje.coste] > 0) {
                //Check if the character has more synergies than the previous best
                if (sinergiasActivas > maxSinergiasActivas) {
                    maxSinergiasActivas = sinergiasActivas;
                    mejoresChamps = [id];
                } 
                //If not, check if it has the same amount of synergies and add it to the array
                else if (sinergiasActivas === maxSinergiasActivas) {
                    mejoresChamps.push(id);
                }
            }
        }
    }

    //Sort the array of characters by cost and probability
    mejoresChamps.sort((a, b) => {
        let costeA = personajes[a].coste;
        let costeB = personajes[b].coste;
        let probA = probabilidades[nivel][costeA];
        let probB = probabilidades[nivel][costeB];

        if (probA === probB) {
            return costeA - costeB;
        }
        return probB - probA;
    });

    return mejoresChamps;
}

//Function to update the recommended characters container
function updateRecChamps() {
    let nivel = parseInt(document.getElementById('nivel').value);
    //Call the function to find the best characters
    let mejoresChamps = findBestChamps(nivel);

    //Clear the container
    document.querySelectorAll('.recchamp').forEach((recchamp) => {
        recchamp.remove();
    });

    //Iterate over the best characters and add them to the container
    mejoresChamps.forEach((id, index) => {
        let champ = personajes[id];
        let img = document.createElement('img');

        img.src = `base_datos/imagenes/champs/${champ.name}.png`; //Set the image source
        img.alt = champ.name;

        //Create the div for the border of the character and add the image
        let recchamp = document.createElement('div');
        recchamp.className = `recchamp recchamp-${champ.coste}`;
        recchamp.appendChild(img);

        //Add the div to the container
        document.querySelector('.recommendation-container').appendChild(recchamp);
    });
}

//Add the event listeners to the level selector and the characters
document.getElementById('nivel').addEventListener('change', updateRecChamps);
document.querySelectorAll('.champ-2 img, .embl-2 img, .champ_menu .champ, .emblem .embl-1').forEach((img) => {
    img.addEventListener('click', updateRecChamps);
});
//#################//