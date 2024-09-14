//##############################################################################################//
//# Authors: Mateo Peña Costa and Raquel Cámara Domene
//# Description: Script to manage the emblems of the page
//##############################################################################################//

// When the document is loaded
document.addEventListener('DOMContentLoaded', function() {
    const emblems = document.querySelectorAll('.embl-2 img');
    const embl1Containers = document.querySelectorAll('.embl-1');

    emblems.forEach(emblem => {
        emblem.addEventListener('click', function() {
            //Find the first empty container
            const emptyEmbl1 = Array.from(embl1Containers).find(container => container.innerHTML.trim() === ''); /* provided by AI */

            if (emptyEmbl1) {
                //Clone the emblem and add it to the container
                const newEmblem = emblem.cloneNode(true);  /* provided by AI */
                newEmblem.addEventListener('click', function() {
                    newEmblem.remove();
                });
                emptyEmbl1.appendChild(newEmblem);
            }
        });
    });

    //Remove emblem from container
    embl1Containers.forEach(container => {
        container.addEventListener('click', function() {
            if (container.firstChild) {
                container.firstChild.remove();
            }
        });
    });
});