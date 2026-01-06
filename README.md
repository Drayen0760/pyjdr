# pyjdr
<p>
<img src="https://github.com/Drayen0760/pyjdr/blob/main/image/pyjdr_image.png"/>
</p>

pyjdr est un module python qui fournit une aide à la gestion de vos parties et combats de jeu de role en permettant de stocker des informations sur des joueurs et des monstre
pyjdr utilise une interface en ligne de commande

## Installation 

### sous Linux et MacOs
- télécharger le fichier  ```pyjdr_installer.py``` depuis ce [github](https://github.com/Drayen0760/pyjdr/blob/main/pyjdr_installer.py)

- exécuter dans le terminale la commande suivante :
```sh
python3 /chemin/vers/le/script/pyjdr_installer.py
```

### sous Windows
****__Non Implémenté__****


## Utilisation

Deux fonctions principales :

<details>

 <summary>start()</summary> 

 Permet de démarer une partie
```python
import pyjdr
pyjdr.start() # pour démarer
```
![demostart](https://github.com/Drayen0760/pyjdr/blob/main/image/pyjdr_demo_start.png)

</details>


<details>

 <summary>gamemanager()</summary> 

pour gérer les parties (suppression, renommage, visualisation)

```python
import pyjdr
pyjdr.gamemaneger() # pour démarer
```
![demogamemanager](https://github.com/Drayen0760/pyjdr/blob/main/image/pyjdr_demo_gamemanager.png)
</details>
