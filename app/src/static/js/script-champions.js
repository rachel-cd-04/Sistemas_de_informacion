//##############################################################################################//
//# Authors: Mateo Peña Costa and Raquel Cámara Domene
//# Description: Script to manage the champions of the page
//##############################################################################################//

// When the document is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Selecciona todos los contenedores de campeones en el campo
    const champMenu = document.querySelectorAll('.champ');
    // Selecciona todas las imágenes de campeones en el buscador
    const imgChamps = document.querySelectorAll('.img-champ');

    const champDataScript = document.getElementById('champ-data'); 
    const champs = JSON.parse(champDataScript.textContent);

    imgChamps.forEach(img => {
        img.addEventListener('click', function() {
            for (let i = 0; i < champMenu.length; i++) {
                if (champMenu[i].children.length === 0) {
                    const champName = img.alt; // Obtiene el nombre del campeón del atributo alt
                    const champ = champs.find(champ => champ.nombre === champName); // Busca el campeón por nombre

                    if (champ) {
                        const campoImg = document.createElement('img');
                        campoImg.setAttribute('src', champ.url_campo); // Usa la URL del atributo url_campo
                        campoImg.setAttribute('alt', champName);
                        campoImg.classList.add('img-champ');
                        champMenu[i].appendChild(campoImg); // Añade la imagen al contenedor
                    }

                    break;
                }
            }
        });
    });

    // Eliminar campeón del contenedor
    champMenu.forEach(container => {
        container.addEventListener('click', function() {
            if (container.firstChild) {
                container.firstChild.remove();
            }
        });
    });
});

