<b>PROJECT NAME</b> : Projet de visualition CMI ISI : site web interactif avec données Marvel

<b>DESCRIPTION</b> : De manière synthétique, ce projet propose trois visualitions consistant à modéliser : le réseau social d'un personnage, le champ lexical caractéristique d'un personnage, et une évolution temporelle de la popularité d'un ensemble de personnages. Plus de détails concernant les visualisations sont disponibles dans les pages web du site.

<b>TABLE OF CONTENTS</b> : <ul>
<li> Un dossier Static contenant toutes les ressources statiques (images, code css,...) </li>
<li> Un dossier Templates contenant nos fichiers html qui servent à : choisir les visualisations désirées et les paramètres (quand il y'a lieu), ainsi que l'affichage du résultat </li>
<li> Un fichier webapp.py dans lequel toutes nos routes sont définies </li>
<li> Un fichier cloud.py qui contient les fonctions utiles à la génération des données exploitées dans le WordCloud </li>
<li> Un fichier final_graph.py qui contient toutes les fonctions qui permettent d'obtenir les années de parution des comics/series des personnages choisis qui seront utilisées par le graphique chronologique.</li> </ul>

<b>ACCESS</b> : Afin de vous connecter sur le site, il suffit de lancer le fichier webapp.py et de vous connecter sur localhost:5000. Le sit sera prochainement disponible sur nos adresses du CREMI également.

<b>USAGE</b> : L'accès sur le site mènera vers une page qui demandera à l'utilisateur de choisir le type de visualisation qu'il aimerait voir. Trois images sont proposées, il suffit de cliquer sur une des images et l'utilisateur sera redirigé vers la page d'accueil de la visualisation choisie. Voici une brève présentation du des visualisations, le détail étant sur chaque page correspondante. <ul>
<li> Réseau social : Il suffit d'accéder à la page d'accueil et d'utiliser la liste déroulante afin de choisir un personnage initial (noeud rouge) autour duquel le graphe se construira le graphe (les comics dans lequel il apparait sont en bleu clair, et les personnages annexes sont en jaune). Il est possible de cliquer sur un personnage afin d'obtenir le graphe centré sur celui-ci. L'historique de notre cheminement est présent en bas à gauche de la fenetre. Lorsqu'on clique sur un de ces liens, le graphe se construit autour du personnage en question, et l'arborescence se réinitialise, comme si on avait saisi ce personnage là à l'aide du formulaire. Le graphe peut parfois prendre une trentaine de secondes pour se construire. D'autre part, il peut occasionellement etre condensé en un seul point, et afin de déplier le graphe, il suffit de cliquer sur le noeud (ou le tirer) </li>
<li> WordCloud : L'utilisateur doit d'abord choisir l'univers de comics qui l'interesse. Ensuite, il peut choisir le personnage dont il aimerait voir le WordCloud et valider son choix. La page sur laquelle il sera amené contiendra le WordCloud du personnage en question (avec par défaut les 200 mots les plus importants). Il est possible de saisir un nombre de mots plus petit (ou plus grand) à l'aide d'un champ de saisie, et la page se rafraichira et donnera le nouveau WordCloud. Si la disposition des mots ne plait pas à l'utilisateur, il suffit de rafraichir la page et une nouvelle disposition sera proposée. Il est interessant d'ouvrir plusieurs onglets cote à cote afin de comparer les mots les plus caractéristiques de plusieurs personnages. </li>
<li> Evolution de popularité chronologique : une fois que l'utilisateur aura lancé l'animation, les années défileront et les personnages (représentés par des points de couleur propre à leur univers) se déplaceront vers la droite lorsque le nombre de comics dnas lequel ils apparaissent augmente, et vers le haut lorsque le nombre de series dans lequel ils apparaissent augmente. A la fin de l'animation, l'utilisateur peut faire défiler les années et se positionner à des années qui l'interessent, et les points reviendront dans les états conséquents. </li> </ul>

![welcome](https://user-images.githubusercontent.com/49319690/70246254-bac15180-1777-11ea-90d1-5d4770b30d1d.PNG)

![capture_graph](https://user-images.githubusercontent.com/49319690/70246280-ca409a80-1777-11ea-8705-bf0eda2516be.png)

![worldcloud](https://user-images.githubusercontent.com/49319690/70246370-f1976780-1777-11ea-9b00-57be753e4c57.png)

![final_graph](https://user-images.githubusercontent.com/49319690/70246405-ffe58380-1777-11ea-8856-a19f6f10aa06.png)

<b>AUTHORS</b> : Wael BEN HADJ YAHIA, Marie-Mathilde GARCIA, Dorian HERVE

<b>CONTRIBUTING</b> : Pour contribuer à ce projet, il serait possible de proposer d'autres types de visualitions, et/ou enrichir les données qui sont exploitées ici.

<b>CREDITS</b> : Nous tenons à remercier : <ul>

<li> M. Bruno Pinaud et M. Guy Melancon pour leur encadrement durant la réalisation de ce projet. </li>

<li> L'auteur du graphe d3 "Les Misérables" pour notre visualition graphe noeud/lien : https://gist.github.com/mbostock/4062045 </li>

<li> L'auteur du WordCloud disponible sur : https://www.d3-graph-gallery.com/graph/wordcloud_size.html </li>

<li> Mike Bostock : https://bost.ocks.org/mike/nations/ </li> </ul>
