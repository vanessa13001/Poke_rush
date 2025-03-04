import random
import pygame

class Pokemon:
    def __init__(self, nom, type_, pv, niveau, attaque, defense, image_path, xp=0, xp_to_next_level=100):
        self.nom = nom
        self.type_ = type_
        self.pv = pv
        self.niveau = niveau
        self.attaque = attaque
        self.defense = defense
        self.xp = xp
        self.xp_to_next_level = xp_to_next_level
        self.position = (0, 0)  # Ajouter un attribut position avec une valeur par défaut
        self.image_path = image_path  # Ajouter l'attribut image_path

        # Charger l'image avec gestion des erreurs
        try:
            self.image = pygame.image.load(image_path)
            self.image = self.image.convert_alpha()  # Convertir en 32 bits avec alpha
            self.image = pygame.transform.smoothscale(self.image, (400, 400))  # Redimensionner avec lissage
        except pygame.error as e:
            print(f"Erreur lors du chargement de l'image {image_path}: {e}")
            self.image = None  # Ou une image par défaut

    def subir_degats(self, degats):
        print('va subir degats')
        degats_final = max(0, degats - self.defense)  # La défense réduit les dégâts
        self.pv -= degats_final
        self.pv = max(0, self.pv)  # Empêche les PV d'être négatifs

    def attaquer(self, adversaire):
        if random.random() > 0.1:  # 10% de chance de louper l’attaque
            degats = self.attaque * self.multiplicateur_type(adversaire.type_)
            adversaire.subir_degats(degats)
            print(f"{self.nom} attaque {adversaire.nom} et inflige {degats} dégâts !")
        else:
            print(f"{self.nom} a raté son attaque !")

    def est_vivant(self):
        return self.pv > 0

    def multiplicateur_type(self, type_adversaire):
        """ Retourne le multiplicateur de dégâts selon le type """
        table_types = {
            "eau": {"feu": 2, "terre": 0.5, "normal": 1},
            "feu": {"terre": 2, "eau": 0.5, "normal": 1},
            "terre": {"eau": 2, "feu": 0.5, "normal": 1},
            "normal": {"eau": 1, "feu": 1, "terre": 1}
        }
        return table_types.get(self.type_, {}).get(type_adversaire, 1)

    def gain_xp(self, xp_gagne):
        """Ajoute de l'XP au Pokémon et vérifie s'il monte de niveau."""
        self.xp += xp_gagne
        print(f"{self.nom} a gagné {xp_gagne} XP !")

        if self.xp >= self.xp_to_next_level:
            self.niveau_up()

    def niveau_up(self):
        """Augmente le niveau du Pokémon et ajuste ses statistiques."""
        self.niveau += 1
        self.xp = self.xp - self.xp_to_next_level  # Réinitialiser l'XP au-delà du niveau
        self.xp_to_next_level += 100  # Augmenter l'XP nécessaire pour le prochain niveau
        self.pv = 100  # Réinitialiser les PV à 100
        self.attaque += 5  # Augmenter l'attaque
        self.defense += 5  # Augmenter la défense
        print(f"{self.nom} est monté au niveau {self.niveau} !")

    def to_dict(self):
        """Convertit l'objet Pokémon en dictionnaire pour la sérialisation."""
        return {
            'nom': self.nom,
            'type_': self.type_,
            'pv': self.pv,
            'niveau': self.niveau,
            'attaque': self.attaque,
            'defense': self.defense,
            'image_path': self.image_path,  # Assurez-vous que cet attribut est inclus
            'xp': self.xp,
            'xp_to_next_level': self.xp_to_next_level
        }

    @staticmethod
    def from_dict(pokemon_data):
        """Crée un objet Pokémon à partir d'un dictionnaire."""
        return Pokemon(
            nom=pokemon_data['nom'],
            type_=pokemon_data['type_'],
            pv=pokemon_data['pv'],
            niveau=pokemon_data['niveau'],
            attaque=pokemon_data['attaque'],
            defense=pokemon_data['defense'],
            image_path=pokemon_data['image_path'],
            xp=pokemon_data['xp'],
            xp_to_next_level=pokemon_data['xp_to_next_level']
        )
