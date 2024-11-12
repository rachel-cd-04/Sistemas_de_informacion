//##############################################################################################//
//# Authors: Mateo Peña Costa and Raquel Cámara Domene
//# Description: Script to handle the sinergies of the characters and emblems, 
//#              and to recommend characters based on the selected sinergies and level.
//##############################################################################################//

//################//
//GLOBAL VARIABLES//
//################//

let personajesElement = document.getElementById('champ-data');
let personajes = JSON.parse(personajesElement.textContent);

let emblemasElement = document.getElementById('emblem-data');
let emblemas = JSON.parse(emblemasElement.textContent);

let sinergiasElement = document.getElementById('synergie-data'); 
let sinergias = JSON.parse(sinergiasElement.textContent);

let sinergiasContainer = {}; //Container for active synergies

let personajesSeleccionadosID = new Array(12).fill(0); //Arrays to store the id of selected characters on theirs positions
let personajesSeleccionados = {};  //Array to store the number of times a character has been selected

let tope = 0; //Count of selected emblems
let emblemasSeleccionadosID = new Array(5).fill(0); //Arrays to store the id of selected emblems on theirs positions
let emblemasSeleccionados = new Array(12).fill(0); //Array to store the number of times a emblem has been selected
//#################//



//##################//
//SYNERGIE FUNCTIONS//
//##################//

//Aux Function to get the id of a character by its name
function getIdByName(name) {
    for (let id in personajes) {
        if (personajes[id].nombre === name) {
            return id;
        }
    }
    return null; // Si no se encuentra el nombre
}

//Function to handle the click on a character (add theirs sinergies to the container)
function handleClickChamp(name, posicion) {
    //If the character is already selected, increase the count and return
    if (personajesSeleccionados[name]) {
        personajesSeleccionados[name]++;
        personajesSeleccionadosID[posicion] = name;
        return;
    }

    personajesSeleccionados[name] = 1; //Increase the count of the character
    personajesSeleccionadosID[posicion] = name; //Store the character id in the position

    let id = getIdByName(name);
    let champSinergias = personajes[id].sinergias;

    //Add the sinergies to the container
    champSinergias.forEach(sinergia => {
        if (sinergiasContainer[sinergia.nombre]) {
            sinergiasContainer[sinergia.nombre]++;
        } 
        else {
            sinergiasContainer[sinergia.nombre] = 1;
        }
    });

    updateSynergiesContainer();
}

//Function to remove the sinergies of a character from the container
function removeChamp(posicion) {
    let name = personajesSeleccionadosID[posicion];
    personajesSeleccionadosID[posicion] = "";

    //If the character is duplicated, return
    if (personajesSeleccionadosID.includes(name)) {
        return;
    }
 
    let id = getIdByName(name);
    let champSinergias = personajes[id].sinergias;

    //Remove the sinergies from the container
    champSinergias.forEach(sinergia => {
        if (sinergiasContainer[sinergia.nombre]) {
            sinergiasContainer[sinergia.nombre]--;
            if (sinergiasContainer[sinergia.nombre] === 0) {
                delete sinergiasContainer[sinergia.nombre];
            }
        }
    });

    personajesSeleccionados[name] = 0; //Reset the character position
    personajesSeleccionadosID[posicion] = ""; //Reset the character id in the position

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

function obtenerAtributosSinergia(nombre) {
    for (let i = 0; i < sinergias.length; i++) {
        if (sinergias[i].nombre === nombre) {
            return sinergias[i];
        }
    }
    return null; // Si no se encuentra la sinergia
}

//Function to update the sinergies container
function updateSynergiesContainer() {
    let container = document.querySelector('.sinergias-container');
    container.innerHTML = ''; //Clear the container

    let emblDivs = [];

    //Create the divs for each sinergie
    for (let nombre in sinergiasContainer) {
        let sinergia = obtenerAtributosSinergia(nombre);
        if (sinergia) {
            //Create main div
            let emblDiv = document.createElement('div');
            emblDiv.className = 'embl';

            //Create number of times the sinergie is active
            let numDiv = document.createElement('div');
            numDiv.className = 'num';
            numDiv.textContent = `${sinergiasContainer[sinergia.nombre]}`;

            //Create the sinergie name
            let synerDiv = document.createElement('div');
            synerDiv.className = 'syner';
            synerDiv.textContent = `${sinergia.nombre}`;

            //Create the levels of the sinergie
            let cantidadDiv = document.createElement('div');
            cantidadDiv.className = 'cantPosible';
            cantidadDiv.textContent = `${sinergia.unidades_mejora}`;

            //Create the image of the sinergie
            let imgDiv = document.createElement('img');
            imgDiv.className = 'imag';

            imgDiv.src = `${sinergia.url_}`;
            imgDiv.alt = sinergia.nombre;

            //Add the elements to the main div
            emblDiv.appendChild(imgDiv);
            emblDiv.appendChild(numDiv);
            emblDiv.appendChild(synerDiv);
            emblDiv.appendChild(cantidadDiv);

            //Add the div to the array
            emblDivs.push({ element: emblDiv, count: sinergiasContainer[sinergia.nombre] });
        }
        else {
            alert('Error al obtener los atributos de la sinergia, sinergia no encontrada');
        }
    }

    //Sort the divs by the number of times the sinergie is active
    emblDivs.sort((a, b) => b.count - a.count);

    //Add the divs to the container
    emblDivs.forEach(item => container.appendChild(item.element));
}


//Add the event listeners to the characters and emblems
document.querySelectorAll('.champ-2 img').forEach((img, index) => {
    img.addEventListener('click', () => {
        let posicion = obtainPositionInContainerChamp();
        let name = obtainNameInContainerChamp(event);
        handleClickChamp(name, posicion);
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

//Aux Function to get the name of the first empty div in the character container
function obtainNameInContainerChamp(event) {
    let champ = event.currentTarget.closest('.champ-2');
    if (champ) {
        let nameElement = champ.querySelector('.name');
        if (nameElement) {
            return nameElement.textContent.trim();
        }
    }
    return null;
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