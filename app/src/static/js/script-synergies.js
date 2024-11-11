//##############################################################################################//
//# Authors: Mateo Peña Costa and Raquel Cámara Domene
//# Description: Script to handle the sinergies of the characters and emblems, 
//#              and to recommend characters based on the selected sinergies and level.
//##############################################################################################//

//################//
//GLOBAL VARIABLES//
//################//
let personajes = ;
let emblemas = ;
let sinergias = ;
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
        1;1: 1, 2: 0, 3: 0, 4: 0, 5: 0 },
        2;1: 1, 2: 0, 3: 0, 4: 0, 5: 0 },
        3;1: 0.75, 2: 0.25, 3: 0, 4: 0, 5: 0 },
        4;1: 0.55, 2: 0.30, 3: 0.15, 4: 0, 5: 0 },
        5;1: 0.45, 2: 0.33, 3: 0.20, 4: 0.02, 5: 0 },
        6;1: 0.30, 2: 0.40, 3: 0.25, 4: 0.05, 5: 0 },
        7;1: 0.19, 2: 0.30, 3: 0.35, 4: 0.10, 5: 0.01 },
        8;1: 0.18, 2: 0.25, 3: 0.36, 4: 0.18, 5: 0.03 },
        9;1: 0.10, 2: 0.20, 3: 0.25, 4: 0.35, 5: 0.10 },
        10;1: 0.05, 2: 0.10, 3: 0.20, 4: 0.40, 5: 0.25 },
        11;1: 0.01, 2: 0.02, 3: 0.12, 4: 0.50, 5: 0.35 }
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