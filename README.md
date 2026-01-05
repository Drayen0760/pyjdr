# pyjdr
<p>
<img src="https://github.com/Drayen0760/pyjdr/blob/main/image/pyjdr_image.jpeg"/>
</p>

pyjdr est un module python qui fournit une aide à la gestion de vos parties et combats de jeu de role en permettant de stocker des informations sur des joueurs et des monstre
pyjdr utilise une interface en ligne de commande

## Installation 
---

### sous Linux et MacOs
- télécharger le fichier  ```pyjdr_installer.py``` depuis ce [github](https://github.com/Drayen0760/pyjdr/blob/main/pyjdr_installer.py)

- exécuter dans le terminale la commande suivante :
```sh
python3 /chemin/vers/le/script/pyjdr_installer.py
```

### sous Windows
****__Non Implémenté__****

## Utilisation
---
Deux fonctions principales :

<details>

 <summary>start()</summary> 

 Permet de démarer une partie
```python
import pyjdr
pyjdr.start() # pour démarer
```

<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#00ff00;">In [</span><span style=" font-weight:600; color:#00ff00;">1</span><span style=" color:#00ff00;">]:</span> import pyjdr</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">pygame 2.6.1 (SDL 2.28.4, Python 3.12.3)</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Hello from the pygame community. https://www.pygame.org/contribute.html</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#00ff00;">In [</span><span style=" font-weight:600; color:#00ff00;">2</span><span style=" color:#00ff00;">]:</span> pyjdr.start()</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">nom de votre partie : demo_game</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">cette partie existe déjà, vous voulez la charger ?</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">oui (1) ou non (0) : 1</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">/!\ Ce programme est seulement une aide pour le Jeu De Rôle qui vous permet d'enregistrer et de gérer vos persos. Ce n'est en aucun cas une simulation du jeu de rôle,peu de protections sont mises en places et vous pouvez très bien vous améliorer sans raison, je fais donc appel à votre sérieux et à votre bon sens pour ne pas détruire votre expérience de jeu !</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-weight:600; text-decoration: underline; color:#006400;">consigne de jeu : </span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">- vous pouvez y avoir accès à tout moment en entrant <span style=" color:#006400;">&quot;help&quot;</span> dans les inputs </p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">généraux</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">- un dé se représente sous la forme <span style=" font-weight:600;">(</span>a,b<span style=" font-weight:600;">)</span> où a est lmaine nb de dé lancé et b et</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">le type de dé <span style=" font-weight:600;">(</span>d6 ou d20 par ex<span style=" font-weight:600;">)</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">- les rgles du jeux de rôle utilisées sont celles de Chroniques Oubliées</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">- à chaque tour, vous devrez faire différent choix :</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">    <span style=" font-weight:600; color:#4682b4;">1</span> - lancer un combat <span style=" font-weight:600;">(</span>c<span style=" font-weight:600;">)</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">    <span style=" font-weight:600; color:#4682b4;">2</span> - interagir avec les PNJ <span style=" font-weight:600;">(</span>i<span style=" font-weight:600;">)</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">    <span style=" font-weight:600; color:#4682b4;">3</span> - franchir un obstacle <span style=" font-weight:600;">(</span>o<span style=" font-weight:600;">)</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">    <span style=" font-weight:600; color:#4682b4;">4</span> - se soigner <span style=" font-weight:600;">(</span>sort ou potions<span style=" font-weight:600;">)</span> <span style=" font-weight:600;">(</span>s<span style=" font-weight:600;">)</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">    <span style=" font-weight:600; color:#4682b4;">5</span> - interchanger le jour et la nuit <span style=" font-weight:600;">(</span>n ou j en fonction du cas<span style=" font-weight:600;">)</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">    <span style=" font-weight:600; color:#4682b4;">6</span> - dormir pour récupérer des PV <span style=" font-weight:600;">(</span>uniquement de nuit <span style=" font-weight:600;">(</span>d<span style=" font-weight:600;">)</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">    <span style=" font-weight:600; color:#4682b4;">7</span> - quitter et sauvegarder <span style=" font-weight:600;">(</span>q<span style=" font-weight:600;">)</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">    <span style=" font-weight:600; color:#4682b4;">8</span> - quitter sans sauvegarder <span style=" font-weight:600;">(</span>e<span style=" font-weight:600;">)</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">    <span style=" font-weight:600; color:#4682b4;">9</span> - afficher un personnage <span style=" font-weight:600;">(</span>a<span style=" font-weight:600;">)</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">    <span style=" font-weight:600; color:#4682b4;">10</span> - naviguer dans la liste des monstres <span style=" font-weight:600;">(</span>m<span style=" font-weight:600;">)</span></p>
<br/>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"> menu principal - votre choix : q</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Votre partie a été <span style=" color:#006400;">enregistrée</span> avec succès dans le dossier : 'demo_game'</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>


</details>


<details>

 <summary>gamemanager()</summary> 

pour gérer les parties (suppression, renommage, visualisation)

```python
import pyjdr
pyjdr.gamemaneger() # pour démarer
```
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#00ff00;">In [</span><span style=" font-weight:600; color:#00ff00;">1</span><span style=" color:#00ff00;">]:</span> import pyjdr</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" color:#00ff00;">In [</span><span style=" font-weight:600; color:#00ff00;">2</span><span style=" color:#00ff00;">]:</span> pyjdr.gamemanager()</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">liste des parties : </p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">	0) demo_game</p>
<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">actions disponibles : </p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">	0) supprimer une partie (s)</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">	1) visualiser une partie (v)</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">	2) renommer partie+joueurs (r)</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">	3) quitter (q)</p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;">Gamemanager - votre choix : </p></body></html>
</details>
