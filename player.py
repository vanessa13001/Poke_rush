from pokedex import Pokedex

class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.pokemon_rencontres = []
        self.equipe = []  # Liste pour stocker les Pokémon capturés

    def rencontrer_pokemon(self, pokemon):
        """Ajoute un Pokémon rencontré au joueur et l'enregistre dans le Pokédex."""
        self.pokemon_rencontres.append(pokemon)
        pokemon_pokedex = Pokedex()
        pokemon_pokedex.enregistrer_pokedex(pokemon)

    def ajouter_pokemon(self, pokemon):
        """Ajoute un Pokémon capturé à l'équipe du joueur."""
        self.equipe.append(pokemon)
        print(f"{pokemon.nom} a été ajouté à l'équipe de {self.nom}.")

    def obtenir_pokemons(self):
        """Retourne la liste des Pokémon dans l'équipe du joueur."""
        return self.equipe
