# Teamfight Tactics Team Manager
## Video Demo: https://youtu.be/Y_9dR4FunNM
## Description: 

Our names are Mateo Peña Costa and Raquel Cámara Domene. We are two students from the University of Zaragoza (UNIZAR), Spain. We are currently attending computer engineering and wanted to do some extra learning this Summer so we decided to take the CS50 course.


This idea came up when I (Raquel Cámara) wanted to learn how to play Teamfight Tactics which is an autobattler game in which you compete against 7 other players. Each player forms a team of champions who fight automatically in rounds. The goal is to be the last player standing. But it was difficult at first to know which pieces to move or what to choose. Seeing the statistics that every month 33 million people play Teamfight Tactics we decided to make this tool so that beginners like me could use it.

The hardest part of learning the game was knowing which champions to use, so we decided that a tool to help new players might be a good idea and since Teamfight Tactics uses a lot of math and probability we could integrate an algorithm to help with this task.
This is because each champion adds from 1 to 3 synergies when placed in the game. The synergies have different levels of activation so you want your champions to have as many synergies in common as possible. Having the database of champions, we can calculate who is the optimal champion to add in your next round.
Champions also have different probabilities of appearance depending on the player’s level, so we will have that in consideration too, making that a champion can not be recommended if the player doesn't have enough level, and higher percentage of appearance champions will be shown first in the recommendations tab.

Finally we opted to make a desktop website due to the fact that a large part of the players play on PC and have similar websites as reference like:
- Mobalytics: https://mobalytics.gg/tft?int_source=homepage&int_medium=mainbutton
- TFTactics: https://tftactics.gg/

(Ours, of course, is not as complex and instead is aimed at new inexperienced players)

### Project Structure

-As for the programming language used in the project, it has been javascript, html and css. To organise everything better, we decided to make several folders, in the main folder (project) we have the html: `index.html`, `start_team.html` and `aboutUs.html`. In addition there are also 3 subfolders: `base_data`, `scripts` and `style-css`.  `index.html` contains the code necessary for the main page of our website, and is linked to `index-style.css` in the `style.css` folder. `start_team.html` contains the code necessary for the page that contains everything necessary for the user to select level, champions and emblems and display the recommendation(s) they need to continue the game, and is linked to `start_team-style.css` within the `style.css` folder. Finally `aboutUs.html` contains the code necessary for the home page of our website, and is linked to `index-style.css` within the `style.css` folder.
Inside the folder `base_datos` we can find a folder ‘images’ that contains several images such as the background of the home page, the logo that appears in all of them, and some more images used in the home page. Also this `imagenes` folder has 3 subfolders: `champs` (contains the used images of the champions), `emblems` (contains the used images of the emblems), `synergies` (contains the images of the emblems that appear in the synergies section inside `start_team.html`).


- **Project**
	- `base_datos`
		- `imagenes`
	  		- `champs`
	  		- `emblems`
	  		- `synergies`
	- `scripts`
		- `script-champions.js`
		- `script-emblems.js`
		- `script-synergies.js`
	- `style-css`
		- `AU-style.css`
		- `index-style.css`
		- `start_team-style.css`
		- `background.jpeg`
	- `index.html`
	- `start_team.html`
	- `aboutUs.html`


### Scripts

#### `script-champions.js` and `script-emblems.js`
- Both `script-champions.js` and `script-emblems.js` are quite basic, their functionality is to manage clicks on champions and emblems either to add them to the collection or remove them. We have two containers with the champions and emblems of Teamfight Tactics Set 12 in the `start_team.html`, thanks to the two scripts, clicking on one of the images inside the two containers will add it to another container representing the battlefield in the game, it is expected from a user to put on the board all the champions and emblems that they are currently playing in the game in real time.

#### `script-synergies.js`
- If we look at the script `script-synergies.js` we can see how it is more complex than the previous two. First we have 3 vectors that form a small database.
The first vector called ‘characters’ consists of 60 characters, one component for each character, where each component has as attributes a name, the synergies that activates that character, and the cost of it. In addition, the index of each character is the index given in the html container.
The second vector ‘emblems’ contains 21 emblems, one component for each emblem. Each component has as attributes its name and the synergy it activates. The index of these components ranges from 1-21.
Finally, the third vector contains 27 synergies, of which 21 are emblems and the rest are synergies granted by the characters. Each component contains the levels at which each synergy is activated. The index of these components are the names of these synergies.

- We also have a section for more global variables (not initialized) which will contain information about the state of the web.
`sinergiasContainer`: Contains all the synergies being played at the moment.
`personajesSeleccionadosID`: Contains the ID of the selected champions, the index of the vector represents the position in the container of champions (so called battlefield or board).
`personajesSeleccionados`: How many times a champion is selected, indexed by their ID.
`tope`: Counter for the emblems.
`emblemasSeleccionadosID`: Contains the ID of the selected emblems, the index of the vector represents the position in the container of emblems.
`emblemasSeleccionados`: How many times an emblem is selected, indexed by their ID.

- The functions relevant to the synergies menu are also in this .js.
We have two functions to handle the action of adding a champion or a player which are:
`handleClickChamp` and  `handleClickEmblem`. These functions need the `id` of the element and the first free `position` in the container in which they are going to be added. They both manage the synergies, adding when it's necessary from `sinergiasContainer`.
Another two functions are used similar when a champion or emblem is removed:
`removeChamp` and `removeEmblem` which use the position of the champion/emblem removed. They both manage the synergies, removing when it's necessary from `sinergiasContainer`.
The four functions call `updateSynergiesContainer` when finished. This function will remove all synergies from the container in the .html and then add the ones from `sinergiasContainer`, each one which is image, name and information stored in the three big database vectors.
We then have the eventListeners, for adding and removing both champions and emblems.
Finally there are two auxiliary functions `obtainPositionInContainerChamp` and `obtainPositionInContainerEmblem`  that are called in the addEventListeners for adding champions and emblems in order to calculate the next free position.

- At the end of the file we have the functions related to recommendations. The first function is an auxiliary function for the recommended characters button in the html. Just below it we can see several ‘event listeners’. The first one is set for when you select a champion, the second one for when you select an emblem, the third one for when you remove a champion and the fourth one for when you remove an emblem. They all perform the action of recalculating the best recommendation.
Then we have two functions, the first one called `findBestChamps` calculates the best character to recommend taking into account appearance probabilities based on level and cost. It goes over all the characters seeing if the user already has them or not, in case he already has them he doesn't recommend them. For the calculation count the number of synergies each character activates and see if this character can appear at the level the user is at. Then see if this character has more synergies than the previous one, and if not, see if it has the same synergies and add it to the vector of recommended characters. It then sorts the vector by cost and probability.
The second function, called `updateRecChamps` displays the vector resulting from the previous function, in the recommendations section on the right of the screen making the necessary divs.
Finally we can see how an update of the recommendations is done.

### Conclusion

The disadvantage of this project would be the fact that it is only prepared for Set 12, so when the following sets were released, it would have to be redone manually for these, changing the content of the vectors that served as a database and some other details.

We are very proud of the final website and all the work done, not to mention the amount of knowledge we have learned from this project.
