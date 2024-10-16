# -*- coding: utf-8 -*-
import turtle
import math
import random
import time

# Paramètres de jeu
CANNON_STEP = 10
LASER_SPEED = 10  # Réduire la vitesse du laser
ALIEN_SPEED = 0.3   # Réduire la vitesse de l'alien
DETECTION_RADIUS = 20  # Rayon de détection de collision

# Configuration de la fenêtre
window = turtle.Screen()
window.setup(width=800, height=600)
window.bgcolor("black")
window.title("Space Invaders")
window.tracer(0)  # Désactiver la mise à jour automatique de l’écran

# Création du canon (partie inférieure)
cannon = turtle.Turtle()
cannon.penup()
cannon.color("white")
cannon.shape("square")
cannon.setposition(0, -230)
cannon.shapesize(stretch_wid=1, stretch_len=3)

# Création de la partie supérieure du canon
def create_cannon_top():
    part2 = turtle.Turtle()
    part2.shape("square")
    part2.color("white")
    part2.penup()
    part2.speed(0)
    part2.setposition(0, -210)
    part2.shapesize(stretch_wid=1, stretch_len=1.5)
    return part2

part2 = create_cannon_top()

# Créer un extraterrestre
def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.shape("square")
    alien.color("green")
    alien.shapesize(stretch_wid=1.5, stretch_len=2)
    alien.setposition(random.randint(-390, 390), 250)  # Position aléatoire en haut
    return alien

# Liste pour stocker les lasers et les extraterrestres
lasers = []
aliens = []  # Liste initiale vide

# Vérifier la collision entre un laser et un extraterrestre
def check_collision(laser, alien):
    distance = laser.distance(alien)
    return distance < DETECTION_RADIUS

# Créer un laser
def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color("red")
    laser.shape("square")
    laser.shapesize(stretch_wid=0.5, stretch_len=2)
    laser.setheading(90)
    laser.setposition(cannon.xcor(), cannon.ycor() + 20)
    return laser

# Déplacer les lasers
def move_lasers():
    for laser in lasers.copy():
        laser.forward(LASER_SPEED)
        # Retirer les lasers qui sortent de l’écran
        if laser.ycor() > window.window_height() / 2:
            laser.clear()
            laser.hideturtle()
            lasers.remove(laser)

        # Vérifier les collisions avec tous les extraterrestres
        for alien in aliens.copy():
            if check_collision(laser, alien):
                laser.clear()
                laser.hideturtle()
                lasers.remove(laser)
                alien.clear()
                alien.hideturtle()
                aliens.remove(alien)  # Retirer l'extraterrestre

# Déplacer le canon et la partie supérieure à gauche
def move_left():
    x = cannon.xcor() - CANNON_STEP
    if x > -390:  # Limite de la fenêtre
        cannon.setx(x)
        part2.setx(x)  # Met à jour la position de la partie supérieure

# Déplacer le canon et la partie supérieure à droite
def move_right():
    x = cannon.xcor() + CANNON_STEP
    if x < 390:  # Limite de la fenêtre
        cannon.setx(x)
        part2.setx(x)  # Met à jour la position de la partie supérieure

# Lier les touches du clavier
window.listen()
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(lambda: lasers.append(create_laser()), "space")

# Boucle de jeu principale
while True:
    window.update()  # Mettre à jour l’écran
    move_lasers()   # Déplacer les lasers

    # Apparition unique d'un extraterrestre à intervalles prolongés
    if not aliens:  # Vérifie s'il n'y a pas d'extraterrestres
        if random.random() < 0.02:  # Chance d'apparition très faible
            aliens.append(create_alien())

    # Déplacer l'extraterrestre
    for alien in aliens.copy():
        alien.setx(alien.xcor() + ALIEN_SPEED)
        # Inverser la direction lorsque l'alien atteint les bords
        if alien.xcor() > 390 or alien.xcor() < -390:
            ALIEN_SPEED = -ALIEN_SPEED
            for a in aliens:
                a.sety(a.ycor() - 20)  # Descendre les extraterrestres

    turtle.delay(10)  # Ajouter un léger délai pour la fluidité

# Garder la fenêtre ouverte
turtle.done()
