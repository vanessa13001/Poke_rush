import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu Poké Rush")
icon = pygame.image.load('img/new_icon.png')
pygame.display.set_icon(icon)

BG = pygame.image.load("assets/bg12.jpg")
BG = pygame.transform.scale(BG, (1280, 720))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def options():
    username = ""
    input_active = True
    font = get_font(45)
    input_rect = pygame.Rect(430, 260, 400, 50)
    color_active = pygame.Color("black")
    color_passive = pygame.Color("gray")
    color = color_passive

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")

        OPTIONS_TEXT = font.render("Quel est ton nom ? :", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 180))  # Remonté légèrement
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        pygame.draw.rect(SCREEN, color, input_rect, 2)
        user_text_surface = font.render(username, True, "Black")
        SCREEN.blit(user_text_surface, (input_rect.x + 10, input_rect.y + 5))  # Ajusté légèrement vers le haut

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="orange")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False

                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                    return

            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN and username.strip():
                        print(f"Username entered: {username}")  # À remplacer par le lancement du combat
                        return username  # Retourner le nom de l'utilisateur
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        username += event.unicode

        color = color_active if input_active else color_passive

        pygame.display.update()

def settings():
    selected_language = None  # Variable pour stocker la langue choisie

    while True:
        SETTINGS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        SETTINGS_TEXT = get_font(45).render("Choose your language", True, "Black")
        SETTINGS_RECT = SETTINGS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(SETTINGS_TEXT, SETTINGS_RECT)

        ENGLISH_BUTTON = Button(image=None, pos=(640, 400),
                                text_input="English", font=get_font(55), base_color="Black", hovering_color="orange")
        FRENCH_BUTTON = Button(image=None, pos=(640, 520),
                               text_input="Français", font=get_font(55), base_color="Black", hovering_color="orange")
        SETTINGS_BACK = Button(image=None, pos=(640, 640),
                               text_input="BACK", font=get_font(55), base_color="Black", hovering_color="orange")

        for button in [ENGLISH_BUTTON, FRENCH_BUTTON, SETTINGS_BACK]:
            button.changeColor(SETTINGS_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ENGLISH_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    selected_language = "English"
                    print("Language set to English")  # Ajoutez votre logique de changement de langue ici
                if FRENCH_BUTTON.checkForInput(SETTINGS_MOUSE_POS):
                    selected_language = "Français"
                    print("Langue réglée sur Français")  # Ajoutez votre logique de changement de langue ici
                if SETTINGS_BACK.checkForInput(SETTINGS_MOUSE_POS):
                    main_menu(selected_language)  # Passez la langue sélectionnée au menu

        pygame.display.update()

def main_menu():
    running = True
    while running:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("POKE RUSH", True, "orange")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        # Réduction de la taille des boutons et espacement suffisant entre chaque
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
                            text_input="PLAY", font=get_font(60), base_color="#d7fcd4", hovering_color="orange")
        SAUVEGARDE_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 375),
                            text_input="SAUVEGARDE", font=get_font(60), base_color="#d7fcd4", hovering_color="orange")
        SETTINGS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 500),
                            text_input="SETTINGS", font=get_font(60), base_color="#d7fcd4", hovering_color="orange")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 625),
                            text_input="QUIT", font=get_font(60), base_color="#d7fcd4", hovering_color="orange")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        # Espacement encore plus large entre les boutons
        button_gap = 120  # L'écart entre les boutons (plus grand que 100)

        PLAY_BUTTON.rect.centery = 250
        SAUVEGARDE_BUTTON.rect.centery = PLAY_BUTTON.rect.centery + button_gap
        SETTINGS_BUTTON.rect.centery = SAUVEGARDE_BUTTON.rect.centery + button_gap
        QUIT_BUTTON.rect.centery = SETTINGS_BUTTON.rect.centery + button_gap

        for button in [PLAY_BUTTON, SAUVEGARDE_BUTTON, SETTINGS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # play()
                    running = False
                if SAUVEGARDE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    username = options()
                    if username:
                        # Charger la partie sauvegardée pour le joueur
                        print(f"Chargement de la partie pour {username}")
                        # Ajoutez ici la logique pour charger la partie sauvegardée
                if SETTINGS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    settings()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
