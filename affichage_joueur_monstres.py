#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 09:37:27 2025

@author: Drayen
"""
import pygame as pg
import os.path as path
from matplotlib.pyplot import imread as PltImread

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns

from pyjdr.creatures_definition import player, monster
from pyjdr.Messages import Error
from pyjdr.sauvegarde_et_chargement import getpath
modul_path = getpath()

def get_simplify_type(creature) :
    creature = type(creature)
    if "monster" in str(creature):
        return monster
    elif "player" in str(creature):
        return player
    return creature

def afficher_creature(creature):
    """
    creature is player or monster type
    """
    type_creature = get_simplify_type(creature)
    if not type_creature in (player, monster):
        Error("TypeError", f"invalid type '{
              type(creature)}', only player or monster types are available")
        return "TypeError"

    win = Console(width=100)

    if type_creature == player :
        nom = creature.nom
        race = nom
    else :
        nom = creature.nom
        race = creature.race
    win.print(f"\t\t [bold black on white]{nom}[/bold black on white] \n")

    # informations de base
    if type_creature == player:
        infos_base = Table(box=box.ROUNDED, border_style="green",
                           title="Informations de base", title_style="bold green")
        infos_base.add_column("Attribut", justify="left", style="bold cyan")
        infos_base.add_column("Valeur", justify="right", style="magenta")

        infos_base.add_row("Niveau", str(creature.niv))
        infos_base.add_row("Race", creature.race)
        infos_base.add_row("Métier", creature.metier)
        infos_base.add_row("Défense", str(sum(creature.defences)))
        infos_base.add_row("Points de vie", f"{
                           creature.vie[0]}/{creature.vie[1]}")
        infos_base.add_row("Initiative", str(creature.stats["DEX"]))
        infos_base.add_row("Dé de vie", str(creature.Dvie))
        infos_base.add_row("Argent", f"{creature.argent} PO")

        win.print(infos_base)

        win.print(Panel.fit(
            Text(creature.infos),
            title="[bold green]Informations complementaires[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))

    elif type_creature == monster:
        infos_base = Table(box=box.ROUNDED, border_style="green", title="Informations de base", title_style="bold green")
        infos_base.add_column("Attribut", style="bold cyan", width=15)
        infos_base.add_column("Valeur", style="magenta")

        infos_base.add_row("INIT", str(creature.Get("init")))
        infos_base.add_row("VIE", str(creature.Get("vie")))

        infos = creature.Get("infos")
        for e in infos:
            infos_base.add_row(e, infos[e])

        win.print(infos_base)


    # Modificateurs des stats
    table = Table(box=box.ROUNDED, border_style="blue", title="stats", title_style="bold blue")

    table.add_column("name", justify="left", style="bold cyan")
    table.add_column("value", justify="right", style="magenta")

    if type_creature == player:
        stats = creature.modificateurs_stats
    else:
        stats = creature.modificateurs_stats
        for e in creature.stats :
            stats[e] = creature.stats[e]

    for stat in stats:
        table.add_row(stat, str(stats[stat]))
    win.print(table)


    # capacites
    win.print(Panel.fit(
        Text("\n".join(str(cap) for cap in creature.capacites), style="white"),
        title="[bold purple]Capacités[/bold purple]",
        border_style="cyan",
        padding=(1, 2)
    ))


    # Equipements
    Equipements = []
    # armes
    for arme in creature.armes:
        if isinstance(arme, dict):
            texte = "\n".join(f"{k} : {v}" for k, v in arme.items())
        else:
            texte = arme
        Equipements.append(Panel.fit(
            Text(texte, style="white"),
            border_style="yellow"
        ))

    if type_creature == player:
        # armures
        for armure in creature.armures:
            if isinstance(arme, dict):
                texte = "\n".join(f"{k} : {v}" for k, v in armure.items())
            else:
                texte = armure
            Equipements.append(Panel.fit(
                Text(texte, style="white"),
                border_style="yellow"
            ))
        # boucliers
        for bouclier in creature.boucliers:
            if isinstance(arme, dict):
                texte = "\n".join(f"{k} : {v}" for k, v in bouclier.items())
            else:
                texte = bouclier
            Equipements.append(Panel.fit(
                Text(texte, style="white"),
                border_style="yellow"
            ))

    win.print(Panel.fit(
        Columns(Equipements, equal=True, expand=True),
        title="[bold red]Equipements[/bold red]",
        border_style="yellow",
        padding=(1, 1)
    ))


    # caracteristiques propres aux joueurs
    if type_creature == player:

        # armes utilisables par le joueur
        Armes_utilisables = []
        dic = {True: "Oui", False: "Non"}
        for k, v in creature.armes_utilisables.items():
            texte = f"{k}:{dic.get(v)}"
            Armes_utilisables.append(texte)

        armes_utilisables = Table(box=box.ROUNDED, border_style="yellow", title="Armes utilisables", title_style="bold yellow")
        armes_utilisables.add_column("Arme", justify="left", style="bold cyan")
        armes_utilisables.add_column("Utilisable", justify="right", style="magenta")

        for e in Armes_utilisables:
            e = e.split(":")
            armes_utilisables.add_row(e[0], e[1])

        win.print(armes_utilisables)

        win.print(Panel.fit(
            Text("\n".join(str(item) for item in creature.inv), style="white"),
            title="[bold white]Inventaire[/bold white]",
            border_style="bright_black",
            padding=(1, 2)
        ))


    image = getpath()+"/monstres/monstres_images/" + race + ".webp"
    is_image = path.isfile(image)
    if is_image :
        im = PltImread(image)
        width, height, _ = im.shape
    else :
        width, height = 720, 400

    termine = False

    pg.init()
    screen = pg.display.set_mode((width, height))  # Definition fenetre

    icon = pg.image.load(f"{modul_path}/image/icons/32x32/light/dragon-svgrepo-com.svg")
    pg.display.set_icon(icon)

    pg.display.set_caption(f"pyjdr -- affichage_perso -- {nom}")

    fps = pg.time.Clock()

    if is_image:
        arriere_plan = pg.image.load(image)
        arriere_plan = arriere_plan.convert_alpha()

    while not termine:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                termine = True

        if is_image:
            screen.fill([255, 255, 255])
            screen.blit(arriere_plan, (0, 0))
        else:
            screen.fill([0, 0, 0])  # met l'arrière plan en noir
            screen.blit(pg.font.SysFont("Arial", 25).render(
                f"image non disponible pour {nom}", True, [102, 205, 0]), (20, 100))
            screen.blit(pg.font.SysFont("Arial", 25).render(
                "vérifiez le nom ou créez une image webp dans :", True, [102, 205, 0]), (20, 130))
            screen.blit(pg.font.SysFont("Arial", 25).render(
                f"{modul_path}/", True, [102, 205, 0]), (60, 160))
            screen.blit(pg.font.SysFont("Arial", 25).render(
                "/monstres/monstres_images/", True, [102, 205, 0]), (60, 190))

        pg.display.flip()
        fps.tick(25)

    pg.quit()
    print(modul_path)
