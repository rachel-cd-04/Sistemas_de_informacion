//##############################################################################################//
//# Authors: Mateo Peña Costa and Raquel Cámara Domene
//# Description: Script to manage the champions of the page
//##############################################################################################//

// When the document is loaded
document.addEventListener('DOMContentLoaded', function() {
    const champMenu = document.querySelectorAll('.champ');
    const imgChamps = document.querySelectorAll('.img-champ');

    imgChamps.forEach(img => {
        img.addEventListener('click', function() {
            for (let i = 0; i < champMenu.length; i++) {
                if (champMenu[i].children.length === 0) {
                    const clonedImg = img.cloneNode(true); // Clone the image  /* provided by AI */
                    const imgSrc = img.src;
                    const imgName = imgSrc.substring(imgSrc.lastIndexOf('/') + 1);
                    const newImgName = 'V-' + imgName.replace('.jpg', '.png'); // Change the image format
                    const newImgSrc = imgSrc.replace(imgName, newImgName);
                    clonedImg.src = newImgSrc;
                    clonedImg.classList.add('img-champ');
                    champMenu[i].appendChild(clonedImg); // Add the image to the container
                    break;
                }
            }
        });
    });

    // Remove champion from container
    champMenu.forEach(container => {
        container.addEventListener('click', function() {
            if (container.firstChild) {
                container.firstChild.remove();
            }
        });
    });
});