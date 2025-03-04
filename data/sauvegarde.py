import json
import os

from pokemon import Pokemon

def sauvegarder_partie(nom_joueur, pokemons):
    # Crée le dossier s'il n'existe pas
    os.makedirs('data/sauvegardes', exist_ok=True)

    # Crée un dictionnaire avec les données à sauvegarder
    donnees_sauvegarde = {
        'nom': nom_joueur,
        'pokemons': [pokemon.to_dict() for pokemon in pokemons]  # Supposons que chaque Pokémon a une méthode to_dict()
    }

    # Écrit les données dans un fichier JSON
    with open(f'data/sauvegardes/{nom_joueur}_sauvegarde.json', 'w') as fichier:
        json.dump(donnees_sauvegarde, fichier)

def charger_partie(nom_joueur):
    try:
        # Lit les données depuis le fichier JSON
        with open(f'data/sauvegardes/{nom_joueur}_sauvegarde.json', 'r') as fichier:
            donnees_sauvegarde = json.load(fichier)

        # Restaure l'état du jeu à partir des données chargées
        pokemons = [Pokemon.from_dict(pokemon_data) for pokemon_data in donnees_sauvegarde['pokemons']]
        return pokemons
    except FileNotFoundError:
        print("Aucune sauvegarde trouvée pour ce nom de joueur.")
        return None
