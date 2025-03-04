import random
import pygame
from pokemon import Pokemon
import os

class Combat:
    def __init__(self, screen, pokemon_adverses, font=None):
        self.screen = screen
        self.pokemon_adverses = pokemon_adverses
        self.pokemon2 = random.choice(pokemon_adverses)
        self.font = font

        self.attaques = [
            {"nom": "Tonnerre"},
            {"nom": "Etincelle"},
            {"nom": "Eclair"},
            {"nom": "Fatal-Foudre"}
        ]

        self.tour_pokemon1 = True

        # Initialiser les positions des Pokémon
        self.pokemon2.position = (500, 300)  # Position initiale du Pokémon 2

    def afficher_fond(self):
        """Affiche le fond d'écran."""
        self.screen.blit(self.background_image, (0, 0))  # Utiliser l'image de fond

    def type_avantage(self, attaquant, defenseur):
        """Retourne le multiplicateur de dégâts en fonction des types."""
        type_avantages = {
            ('eau', 'terre'): 2,
            ('terre', 'feu'): 2,
            ('feu', 'eau'): 0.5
        }
        for (type_attaquant, type_defenseur), multiplicateur in type_avantages.items():
            if attaquant.type_ == type_attaquant and defenseur.type_ == type_defenseur:
                return multiplicateur
        return 1

    def attaquer(self, attaquant, defenseur, attaque_index):
        """Effectue l'attaque entre deux Pokémon et met à jour les PV."""
        degats = random.randint(15, 30)
        multiplicateur = self.type_avantage(attaquant, defenseur)
        degats *= multiplicateur

        defenseur.subir_degats(degats)

        print(f"{attaquant.nom} utilise {self.attaques[attaque_index]['nom']} et inflige {degats} dégâts!")
        print(f"{defenseur.nom} a maintenant {defenseur.pv}/100 PV.")

        # Vérifier si le Pokémon adverse est KO
        if defenseur == self.pokemon2 and not defenseur.est_vivant():
            print(f"{defenseur.nom} est KO !")
            self.animer_sortie_pokemon(self.pokemon2)
            self.switch_pokemon_adverse()

        return degats

    def animer_sortie_pokemon(self, pokemon):
        """Anime la sortie du Pokémon KO vers la droite."""
        clock = pygame.time.Clock()
        original_position = pokemon.position
        target_position = (original_position[0] + 200, original_position[1])
        steps = 50

        for step in range(steps):
            self.afficher_fond()
            pokemon.position = (
                original_position[0] + (target_position[0] - original_position[0]) * step / steps,
                original_position[1]
            )
            self.screen.blit(pokemon.image, pokemon.position)
            pygame.display.flip()
            clock.tick(60)

    def switch_pokemon_adverse(self):
        """Switch le Pokémon adverse lorsqu'il est KO avec animation."""
        print(f"{self.pokemon2.nom} est KO !")

        pokemons_vivants = [p for p in self.pokemon_adverses if p.est_vivant()]

        if self.pokemon2 in pokemons_vivants:
            pokemons_vivants.remove(self.pokemon2)

        if pokemons_vivants:
            self.pokemon2 = random.choice(pokemons_vivants)
            self.pokemon2.pv = 100  # Réinitialiser les PV du nouveau Pokémon
            print(f"L'adversaire envoie {self.pokemon2.nom} !")
            self.animer_entree_pokemon(self.pokemon2)
        else:
            print("Tous les Pokémon adverses sont KO !")

    def animer_entree_pokemon(self, pokemon):
        """Anime l'entrée du nouveau Pokémon depuis la droite."""
        clock = pygame.time.Clock()
        original_position = (self.screen.get_width() + 100, pokemon.position[1])
        target_position = (500, 300)  # Position cible pour le nouveau Pokémon
        steps = 50

        for step in range(steps):
            self.afficher_fond()
            pokemon.position = (
                original_position[0] + (target_position[0] - original_position[0]) * step / steps,
                original_position[1]
            )
            self.screen.blit(pokemon.image, pokemon.position)
            pygame.display.flip()
            clock.tick(60)

    def verifier_fin_combat(self):
        """Vérifie si le Pokémon adverse est KO et le remplace si nécessaire."""
        if not self.pokemon2.est_vivant():
            self.animer_sortie_pokemon(self.pokemon2)
            self.switch_pokemon_adverse()

    def capturer(self, pokemon, joueur):
        """Logique pour capturer un Pokémon."""
        # Exemple de logique de capture
        taux_capture = random.random()  # Génère un nombre aléatoire entre 0 et 1
        if taux_capture > 0.5:  # Par exemple, 50% de chance de capture
            print(f"{joueur.nom} a capturé {pokemon.nom} !")
            joueur.ajouter_pokemon(pokemon)  # Supposons que joueur a une méthode ajouter_pokemon
            return True
        else:
            print(f"{joueur.nom} n'a pas réussi à capturer {pokemon.nom} !")
            return False

    def fuite(self, pokemon1, pokemon2):
        """Logique pour déterminer si la fuite est réussie."""
        taux_fuite = random.random()  # Génère un nombre aléatoire entre 0 et 1
        if taux_fuite > 0.3:  # Par exemple, 70% de chance de fuite réussie
            print(f"{pokemon1.nom} a réussi à fuir !")
            return True
        else:
            print(f"{pokemon1.nom} n'a pas réussi à fuir !")
            return False
