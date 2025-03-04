import json

class Pokedex:
    def __init__(self):
        self.pokedex = self.charger_pokedex()

    def charger_pokedex(self):
        try:
            with open('pokedex.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def enregistrer_pokedex(self, pokemon):
        """Enregistre le Pokémon dans le Pokédex."""
        if pokemon.nom not in [p['nom'] for p in self.pokedex]:
            self.pokedex.append({
                'nom': pokemon.nom,
                'types': pokemon.type_,
                'pv': pokemon.pv,
                'attaque': pokemon.attaque,
                'defense': pokemon.defense
            })
            with open('pokedex.json', 'w') as file:
                json.dump(self.pokedex, file, indent=4)

    def afficher_pokedex(self, screen, font):
        """Affiche tous les Pokémon enregistrés dans le Pokédex."""
        y_position = 100  # Position initiale pour l'affichage
        for pokemon in self.pokedex:
            texte = f"Nom: {pokemon['nom']} | Type: {pokemon['types']} | PV: {pokemon['pv']} | Attaque: {pokemon['attaque']} | Défense: {pokemon['defense']}"
            texte_surface = font.render(texte, True, (0, 0, 0))  # Texte en noir
            screen.blit(texte_surface, (20, y_position))
            y_position += 40  # Espace entre chaque Pokémon
