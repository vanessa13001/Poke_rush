import math
import pygame
import random
import sys
from PIL import Image, ImageSequence

from pokemon import Pokemon
from combat import Combat
from pokedex import Pokedex
from player import Joueur
from button import Button
from menu import *
from data.sauvegarde import sauvegarder_partie, charger_partie

# Initialisation de pygame
pygame.init()

# Définir les dimensions de la fenêtre
WIDTH, HEIGHT = 1250, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poké Rush")
icon = pygame.image.load('img/new_icon.png')
pygame.display.set_icon(icon)

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
HOVER_COLOR = (255, 0, 0)
GRAY = (192, 192, 192)
RED_LIGHT = (255, 100, 100)  # Couleur rouge clair
LIGHT_BLUE = (100, 150, 255)  # Couleur bleu légèrement plus foncé
BACKGROUND_BLUE = (100, 150, 255)  # Couleur du fond de l'écran de choix

# Police pour le texte
font = pygame.font.Font("font/pokemon_fire_red.ttf", 24)  # Changer 24 à 40

# Police plus grande pour les messages
message_font = pygame.font.Font("font/pokemon_fire_red.ttf", 36)

# Création d'un joueur
joueur = Joueur("Ash")

# Création de quelques Pokémon pour l'exemple
pokemon_options = [
    Pokemon("Pikachu", "electric", 100, 5, 30, 20, 'img/sprites/pikachu_back.png', xp=0, xp_to_next_level=100),
    Pokemon("Bulbasaur", "plante", 100, 5, 25, 15, 'img/sprites/squirtle_back.png', xp=0, xp_to_next_level=100),
    Pokemon("Articuno", "feu", 100, 5, 28, 18, 'img/sprites/articuno_back.png', xp=0, xp_to_next_level=100)
]

# Création de Pokémon adverses
pokemon_adverses = [
    Pokemon("Carabaffe", "terre", 100, 5, 25, 15, 'img/sprites/wartortle.png', xp=0, xp_to_next_level=100),
    Pokemon("Raichu", "electric", 100, 5, 30, 20, 'img/sprites/raichu.png', xp=0, xp_to_next_level=100)
]

# Création de l'objet Pokédex
pokedex = Pokedex()

# Charger et redimensionner l'image de fond pour le combat
background_image = pygame.image.load('img/background_v4.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Charger l'image de la Poké Ball
pokeball_image = pygame.image.load('img/poke-ball.png')
pokeball_image = pygame.transform.scale(pokeball_image, (100, 100))  # Redimensionnez selon vos besoins

# Charger et redimensionner l'image de fond pour l'écran de choix des Pokémon
choose_background_image = pygame.image.load('img/R2.jpg')
choose_background_image = pygame.transform.scale(choose_background_image, (WIDTH, HEIGHT))

# Variables de gestion d'attaque
attaque_en_cours = False
attaque_affichee = None
temps_affichage_attaque = 0

# Index de l'attaque sélectionnée par l'utilisateur
selected_attack_index = 0

# Variables pour la gestion du temps de l'attaque
attaque_time = None

# Variables pour la gestion de la fuite
fuite_reussie = False
message_fuite_affiche = False
temps_fuite = 0
fuite_tentee = False
confirmation_fuite = False

# Ajoutez cette variable pour gérer l'affichage du message d'échec de fuite
message_echec_fuite_affiche = False
temps_echec_fuite = 0

# Variable pour suivre le tour actuel
tour_pokemon1 = True

# Délai entre les attaques
delai_attaque = 2000

# Variable pour la capture
capture_en_cours = False
capture_affichee = None
temps_affichage_capture = 0

def load_gif(filename, scale_factor=1.5):
    gif = Image.open(filename)
    frames = []
    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert('RGBA')
        # Redimensionner le frame
        width, height = frame.size
        new_size = (int(width * scale_factor), int(height * scale_factor))
        frame = frame.resize(new_size, Image.LANCZOS)
        pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode)
        frames.append(pygame_image)
    return frames

# Charger les GIFs des Pokémon avec un facteur d'échelle
pokemon_gifs = [
    load_gif('img/sprites/pikachu.gif', scale_factor=1.5),
    load_gif('img/sprites/squirtle_back.gif', scale_factor=1.5),
    load_gif('img/sprites/articuno.gif', scale_factor=1.5)
]

# Variables pour suivre les frames des GIFs
gif_frames = [0, 0, 0]
gif_delay = 50  # Délai entre les frames en millisecondes
last_update_time = pygame.time.get_ticks()

def afficher_cadre_pokemon(pokemon, x, y):
    cadre_surface = pygame.Surface((220, 90), pygame.SRCALPHA)
    cadre_surface.fill(WHITE)

    nom = font.render(pokemon.nom, False, BLACK)
    screen.blit(nom, (x + 10, y + 5))

    lvl_text = font.render(f"Lv {pokemon.niveau}", False, BLACK)
    screen.blit(lvl_text, (x + 180 - lvl_text.get_width(), y + 5))

    xp_text = font.render(f"XP {pokemon.xp}/{pokemon.xp_to_next_level}", False, BLACK)
    screen.blit(xp_text, (x + 10, y + 35))

    pv_bar_width = 200
    pv_bar_height = 10
    pv_ratio = max(pokemon.pv / 100, 0)

    pygame.draw.rect(screen, GREEN, (x + 10, y + 60, pv_bar_width, pv_bar_height), border_radius=5)
    pygame.draw.rect(screen, GREEN, (x + 10, y + 60, pv_bar_width * pv_ratio, pv_bar_height), border_radius=5)
    pygame.draw.rect(screen, (255, 0, 0), (x + 10 + pv_bar_width * pv_ratio, y + 60, pv_bar_width - pv_bar_width * pv_ratio, pv_bar_height), border_radius=5)

    pv_text = font.render(f"{pokemon.pv} / 100", False, BLACK)
    screen.blit(pv_text, (x + 10, y + 75))

def afficher_boutons_attaque():
    attaques = ["Attaque 1", "Attaque 2", "Attaque 3", "Attaque 4"]
    bouton_width, bouton_height = 150, 40
    spacing = 20
    y_offset = HEIGHT - 150
    boutons = []
    for i, attaque in enumerate(attaques):
        x_pos = 850 + (i % 2) * (bouton_width + spacing)
        y_pos = y_offset + (i // 2) * (bouton_height + spacing)

        bouton = pygame.Rect(x_pos, y_pos, bouton_width, bouton_height)

        if i == selected_attack_index:
            pygame.draw.rect(screen, YELLOW, bouton, border_radius=10)
        else:
            pygame.draw.rect(screen, WHITE, bouton, border_radius=10)

        pygame.draw.rect(screen, BLACK, bouton, 3, border_radius=10)

        texte = font.render(attaque, False, BLACK)
        screen.blit(texte, (x_pos + (bouton_width - texte.get_width()) // 2, y_pos + (bouton_height - texte.get_height()) // 2))

        boutons.append(bouton)

    return boutons

def afficher_bouton_fuite():
    bouton_width, bouton_height = 150, 40
    x_pos, y_pos = 1080, HEIGHT - 270  # Décalé de 5 pixels supplémentaires vers la gauche
    bouton = pygame.Rect(x_pos, y_pos, bouton_width, bouton_height)

    pygame.draw.rect(screen, WHITE, bouton, border_radius=10)
    pygame.draw.rect(screen, BLACK, bouton, 3, border_radius=10)

    texte = font.render("Fuite", False, BLACK)
    screen.blit(texte, (x_pos + (bouton_width - texte.get_width()) // 2, y_pos + (bouton_height - texte.get_height()) // 2))

    return bouton

def afficher_bouton_capture():
    bouton_width, bouton_height = 150, 40
    x_pos, y_pos = 900, HEIGHT - 270
    bouton = pygame.Rect(x_pos, y_pos, bouton_width, bouton_height)

    pygame.draw.rect(screen, WHITE, bouton, border_radius=10)
    pygame.draw.rect(screen, BLACK, bouton, 3, border_radius=10)

    texte = font.render("Capturer", False, BLACK)
    screen.blit(texte, (x_pos + (bouton_width - texte.get_width()) // 2, y_pos + (bouton_height - texte.get_height()) // 2))

    return bouton

def afficher_bouton_sauvegarder():
    bouton_width, bouton_height = 150, 40
    x_pos, y_pos = 730, HEIGHT - 270  # Ajustez x_pos pour placer le bouton à côté de "Capturer"
    bouton = pygame.Rect(x_pos, y_pos, bouton_width, bouton_height)

    pygame.draw.rect(screen, WHITE, bouton, border_radius=10)
    pygame.draw.rect(screen, BLACK, bouton, 3, border_radius=10)

    texte = font.render("Sauvegarder", False, BLACK)
    screen.blit(texte, (x_pos + (bouton_width - texte.get_width()) // 2, y_pos + (bouton_height - texte.get_height()) // 2))

    return bouton

def demander_prenom():
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 20, 200, 40)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text

def afficher_confirmation_fuite():
    cadre_width, cadre_height = 300, 150
    x_pos, y_pos = (WIDTH - cadre_width) // 2, (HEIGHT - cadre_height) // 2
    cadre = pygame.Rect(x_pos, y_pos, cadre_width, cadre_height)

    pygame.draw.rect(screen, WHITE, cadre, border_radius=10)
    pygame.draw.rect(screen, BLACK, cadre, 3, border_radius=10)

    message = font.render("Voulez-vous vraiment fuir ?", False, BLACK)
    screen.blit(message, (x_pos + (cadre_width - message.get_width()) // 2, y_pos + 20))

    bouton_oui = pygame.Rect(x_pos + 50, y_pos + 80, 80, 40)
    bouton_non = pygame.Rect(x_pos + 170, y_pos + 80, 80, 40)

    if bouton_oui.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, YELLOW, bouton_oui, border_radius=10)
    else:
        pygame.draw.rect(screen, WHITE, bouton_oui, border_radius=10)

    if bouton_non.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, YELLOW, bouton_non, border_radius=10)
    else:
        pygame.draw.rect(screen, WHITE, bouton_non, border_radius=10)

    pygame.draw.rect(screen, BLACK, bouton_oui, 3, border_radius=10)
    pygame.draw.rect(screen, BLACK, bouton_non, 3, border_radius=10)

    texte_oui = font.render("Oui", False, BLACK)
    texte_non = font.render("Non", False, BLACK)
    screen.blit(texte_oui, (bouton_oui.centerx - texte_oui.get_width() // 2, bouton_oui.centery - texte_oui.get_height() // 2))
    screen.blit(texte_non, (bouton_non.centerx - texte_non.get_width() // 2, bouton_non.centery - texte_non.get_height() // 2))

    return bouton_oui, bouton_non

def animer_fuite(pokemon, screen):
    alpha = 255
    x_pos = 150  # Position initiale en x
    vitesse_fuite = 10  # Vitesse de déplacement vers la gauche
    while alpha > 0 and x_pos > -100:
        screen.blit(background_image, (0, 0))  # Afficher le fond
        combat.afficher_fond()

        x_pos -= vitesse_fuite
        pokemon.image.set_alpha(alpha)
        screen.blit(pokemon.image, (x_pos, HEIGHT - 550))  # Maintenir la position en y

        afficher_cadre_pokemon(pokemon1, 30, 150)
        afficher_cadre_pokemon(combat.pokemon2, 1000, 50)  # Déplacez le cadre de pokemon2 vers la gauche

        pygame.display.update()
        pygame.time.delay(20)

        alpha -= 5

    # Assurez-vous que l'image du Pokémon est complètement transparente après la fuite
    pokemon.image.set_alpha(0)

def animer_capture(pokemon, screen):
    alpha = 255
    pokeball_x = WIDTH - 580 - pokeball_image.get_width() - 20 + 300  # Position x à côté de pokemon, décalé vers la droite
    pokeball_y = HEIGHT - 750 + (pokemon.image.get_height() - pokeball_image.get_height()) // 2 + 50  # Position y décalée vers le bas
    shake_amplitude = 10  # Amplitude de la secousse
    shake_speed = 5  # Vitesse de la secousse
    shake_duration = 30  # Durée de la secousse en frames
    pause_duration = 30  # Durée de la pause entre les secousses

    while alpha > 0:
        screen.blit(background_image, (0, 0))  # Afficher le fond
        combat.afficher_fond()

        pokemon.image.set_alpha(alpha)
        screen.blit(pokemon.image, (WIDTH - 580, HEIGHT - 750))  # Maintenez le Pokémon à sa position initiale

        afficher_cadre_pokemon(pokemon1, 30, 150)
        afficher_cadre_pokemon(combat.pokemon2, 1000, 50)

        pygame.display.update()
        pygame.time.delay(20)

        alpha -= 5

    # Assurez-vous que l'image du Pokémon capturé est complètement transparente
    pokemon.image.set_alpha(0)

    # Première animation de la Poké Ball avec secousse
    for i in range(shake_duration):
        screen.blit(background_image, (0, 0))  # Afficher le fond
        combat.afficher_fond()

        # Calculer la position horizontale avec secousse
        shake_offset = shake_amplitude * math.sin(shake_speed * i)
        pokeball_x_with_shake = pokeball_x + shake_offset

        # Afficher la Poké Ball avec secousse
        screen.blit(pokeball_image, (pokeball_x_with_shake, pokeball_y))

        pygame.display.update()
        pygame.time.delay(30)  # Ajustez le délai pour la vitesse de l'animation

    # Pause entre les secousses
    pygame.time.delay(pause_duration * 30)

    # Deuxième animation de la Poké Ball avec secousse
    for i in range(shake_duration):
        screen.blit(background_image, (0, 0))  # Afficher le fond
        combat.afficher_fond()

        # Calculer la position horizontale avec secousse
        shake_offset = shake_amplitude * math.sin(shake_speed * i)
        pokeball_x_with_shake = pokeball_x + shake_offset

        # Afficher la Poké Ball avec secousse
        screen.blit(pokeball_image, (pokeball_x_with_shake, pokeball_y))

        pygame.display.update()
        pygame.time.delay(30)  # Ajustez le délai pour la vitesse de l'animation

    # Afficher le message de confirmation de capture
    screen.blit(background_image, (0, 0))  # Afficher le fond
    combat.afficher_fond()
    screen.blit(pokeball_image, (pokeball_x, pokeball_y))
    screen.blit(pokemon.image, (50, 50))  # Positionner le Pokémon capturé en haut à gauche

    # Afficher le cadre avec le message de confirmation
    cadre_surface = pygame.Surface((400, 100), pygame.SRCALPHA)
    cadre_surface.fill(WHITE)
    pygame.draw.rect(cadre_surface, BLACK, (0, 0, 400, 100), 3, border_radius=10)
    screen.blit(cadre_surface, (WIDTH // 2 - 200, HEIGHT // 2 - 50))

    capture_message = message_font.render(f"{pokemon.nom} a été capturé !", False, BLACK)
    screen.blit(capture_message, (WIDTH // 2 - capture_message.get_width() // 2, HEIGHT // 2 - capture_message.get_height() // 2))

    pygame.display.update()
    pygame.time.delay(3000)  # Afficher pendant 5 secondes

def choose_pokemon():
    global last_update_time  # Déclarer last_update_time comme variable globale
    selected_pokemon = None
    selected_index = 0  # Index du Pokémon sélectionné

    while True:
        CHOOSE_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("white")

        # Afficher l'image de fond pour l'écran de choix
        screen.blit(choose_background_image, (0, 0))

        CHOOSE_TEXT = font.render("Choisis ton Pokémon :", True, "Black")
        CHOOSE_RECT = CHOOSE_TEXT.get_rect(center=(640, 180))
        screen.blit(CHOOSE_TEXT, CHOOSE_RECT)

        for i, frames in enumerate(pokemon_gifs):
            rect = frames[gif_frames[i]].get_rect(center=(400 + i * 240, 360))
            screen.blit(frames[gif_frames[i]], rect)
            if rect.collidepoint(CHOOSE_MOUSE_POS):
                pygame.draw.rect(screen, BACKGROUND_BLUE, rect.inflate(60, 60), 3)
                if pygame.mouse.get_pressed()[0]:
                    selected_pokemon = i
            elif i == selected_index:
                pygame.draw.rect(screen, BACKGROUND_BLUE, rect.inflate(60, 60), 3)

        CHOOSE_BACK = Button(image=None, pos=(640, 560),
                             text_input="BACK", font=font, base_color="Black", hovering_color="yellow")
        CHOOSE_BACK.changeColor(CHOOSE_MOUSE_POS)
        CHOOSE_BACK.update(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CHOOSE_BACK.checkForInput(CHOOSE_MOUSE_POS):
                    return None
                if selected_pokemon is not None:
                    return pokemon_options[selected_pokemon]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(pokemon_gifs)
                elif event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(pokemon_gifs)
                elif event.key == pygame.K_RETURN:
                    return pokemon_options[selected_index]

        # Mettre à jour les frames des GIFs plus fréquemment
        current_time = pygame.time.get_ticks()
        if current_time - last_update_time > gif_delay:
            for i in range(len(gif_frames)):
                gif_frames[i] = (gif_frames[i] + 1) % len(pokemon_gifs[i])
            last_update_time = current_time

# Initialisation de l'objet Combat
pokemon1 = choose_pokemon()
if pokemon1 is None:
    pygame.quit()
    sys.exit()

# Ajouter le Pokémon choisi à l'équipe du joueur
joueur.ajouter_pokemon(pokemon1)

# Charger la partie sauvegardée si elle existe
nom_joueur = joueur.nom
pokemons_charges = charger_partie(nom_joueur)
if pokemons_charges:
    joueur.equipe = pokemons_charges

combat = Combat(screen, pokemon_adverses)
combat.background_image = background_image

# Combat en cours
combat_en_cours = True

# Boucle principale du jeu
running = True
while running:
    screen.blit(background_image, (0, 0))  # Afficher le fond
    pygame.draw.rect(screen, WHITE, (50, 50, WIDTH - 100, HEIGHT - 100))

    combat.afficher_fond()

    # Ne pas afficher Pikachu si la fuite a réussi
    if not fuite_reussie:
        screen.blit(pokemon1.image, (150, HEIGHT - 550))
    screen.blit(combat.pokemon2.image, (WIDTH - 580, HEIGHT - 750))

    afficher_cadre_pokemon(pokemon1, 30, 150)
    afficher_cadre_pokemon(combat.pokemon2, 1000, 50)

    boutons = afficher_boutons_attaque()
    bouton_fuite = afficher_bouton_fuite()
    bouton_capture = afficher_bouton_capture()
    bouton_sauvegarder = afficher_bouton_sauvegarder()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_attack_index = (selected_attack_index - 2) % 4
            elif event.key == pygame.K_DOWN:
                selected_attack_index = (selected_attack_index + 2) % 4
            elif event.key == pygame.K_LEFT:
                selected_attack_index = (selected_attack_index - 1) % 4
            elif event.key == pygame.K_RIGHT:
                selected_attack_index = (selected_attack_index + 1) % 4
            elif event.key == pygame.K_f:
                confirmation_fuite = True
            elif event.key == pygame.K_c:  # Utilisez la touche "C" pour capturer
                capture_en_cours = True
                capture_reussie = combat.capturer(combat.pokemon2, joueur)
                if capture_reussie:
                    capture_affichee = f"{combat.pokemon2.nom} a été capturé avec succès !"
                    temps_affichage_capture = pygame.time.get_ticks()
                    animer_capture(combat.pokemon2, screen)
                else:
                    capture_affichee = f"La capture de {combat.pokemon2.nom} a échoué !"
                    temps_affichage_capture = pygame.time.get_ticks()
            elif event.key == pygame.K_s:  # Utilisez la touche "S" pour sauvegarder
                prenom = demander_prenom()
                sauvegarder_partie(prenom, joueur.obtenir_pokemons())
                print(f"Partie sauvegardée pour {prenom}")
            elif event.key == pygame.K_RETURN:
                if not attaque_en_cours:
                    if tour_pokemon1:
                        degats = combat.attaquer(pokemon1, combat.pokemon2, selected_attack_index)
                        attaque_affichee = f"{pokemon1.nom} utilise {combat.attaques[selected_attack_index]['nom']} et inflige {degats} dégâts!"
                        temps_affichage_attaque = pygame.time.get_ticks()
                        tour_pokemon1 = False
                        attaque_time = pygame.time.get_ticks()

                        if not combat.pokemon2.est_vivant():
                            pokemon1.gain_xp(50)  # XP gagnée lorsque l'adversaire est mis KO
                            combat.animer_sortie_pokemon(combat.pokemon2)  # Animer la sortie du Pokémon KO
                            combat.switch_pokemon_adverse()  # Changer de Pokémon adverse

                        afficher_cadre_pokemon(pokemon1, 30, 150)
                        afficher_cadre_pokemon(combat.pokemon2, 1000, 50)

                    attaque_en_cours = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if bouton_sauvegarder.collidepoint(event.pos):
                prenom = demander_prenom()
                sauvegarder_partie(prenom, joueur.obtenir_pokemons())
                print(f"Partie sauvegardée pour {prenom}")

    if attaque_en_cours:
        if pygame.time.get_ticks() - attaque_time > delai_attaque:
            if not tour_pokemon1:
                attaque_index = random.randint(0, 3)
                degats = combat.attaquer(combat.pokemon2, pokemon1, attaque_index)
                attaque_affichee = f"{combat.pokemon2.nom} utilise {combat.attaques[attaque_index]['nom']} et inflige {degats} dégts!"
                temps_affichage_attaque = pygame.time.get_ticks()
                tour_pokemon1 = True

                afficher_cadre_pokemon(pokemon1, 30, 150)
                afficher_cadre_pokemon(combat.pokemon2, 1000, 50)

            attaque_en_cours = False

    if attaque_affichee:
        if pygame.time.get_ticks() - temps_affichage_attaque < 2000:
            # Créer un cadre arrondi pour le texte de l'attaque
            cadre_surface = pygame.Surface((WIDTH - 100, 50), pygame.SRCALPHA)
            cadre_surface.fill(WHITE)
            pygame.draw.rect(cadre_surface, BLACK, (0, 0, WIDTH - 100, 50), 3, border_radius=10)
            screen.blit(cadre_surface, (50, HEIGHT - 260))

            texte_attaque = message_font.render(attaque_affichee, False, BLACK)
            screen.blit(texte_attaque, (WIDTH // 2 - texte_attaque.get_width() // 2, HEIGHT - 260 + 10))
        else:
            attaque_affichee = None

    if capture_en_cours:
        if pygame.time.get_ticks() - temps_affichage_capture < 2000:
            texte_capture = message_font.render(capture_affichee, False, BLACK)
            screen.blit(texte_capture, (WIDTH // 2 - texte_capture.get_width() // 2, HEIGHT // 2))
        else:
            capture_en_cours = False

    if confirmation_fuite:
        bouton_oui, bouton_non = afficher_confirmation_fuite()
        if bouton_oui.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            fuite_reussie = combat.fuite(pokemon1, combat.pokemon2)
            if fuite_reussie:
                print(f"{pokemon1.nom} a réussi à fuir !")
                combat_en_cours = False
                animer_fuite(pokemon1, screen)

                message_fuite_affiche = True
                temps_fuite = pygame.time.get_ticks()
                fuite_tentee = True
            else:
                message_echec_fuite_affiche = True
                temps_echec_fuite = pygame.time.get_ticks()

            confirmation_fuite = False
        elif bouton_non.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            confirmation_fuite = False

    if not combat_en_cours:
        if message_fuite_affiche:
            if pygame.time.get_ticks() - temps_fuite < 3000:
                fuite_message = message_font.render(f"{pokemon1.nom} a pris la fuite !", False, BLACK)
                screen.blit(fuite_message, (WIDTH // 2 - fuite_message.get_width() // 2, HEIGHT // 2))
            else:
                message_fuite_affiche = False

    if message_echec_fuite_affiche:
        if pygame.time.get_ticks() - temps_echec_fuite < 3000:
            echec_fuite_message = message_font.render(" Ne veut pas fuir !", False, BLACK)
            screen.blit(echec_fuite_message, (WIDTH // 2 - echec_fuite_message.get_width() // 2, HEIGHT // 2))
        else:
            message_echec_fuite_affiche = False

    pygame.display.update()
    pygame.time.Clock().tick(60)

pygame.quit()
