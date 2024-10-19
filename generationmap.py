import numpy as np
import tkinter as tk
from perlin_noise import PerlinNoise
from random import randint
from Case import Case
from TYPE import TYPE 
from math import sqrt
from Seigneur import Seigneur

# Générer la grille de bruit de Perlin
def generate_perlin_noise(width, height, scale):
    noise = PerlinNoise(octaves=6)
    noise_grid = np.zeros((height, width))
    for i in range(height):
        for j in range(width):
            x = i / scale
            y = j / scale
            noise_value = noise([x, y])
            noise_grid[i][j] = noise_value
    return noise_grid

# Fonction pour placer les villages
def place_villages(map, nb_village, width, height, liste_joueur):
    lvillage=[] #liste des tuples des pos des villages
    for _ in range(nb_village):
        # Choisir des coordonnées aléatoires pour le village
        x_central = randint(3, height - 4)
        y_central = randint(3, width - 4) # pas de village trop au bord
        for i in lvillage:
            while sqrt(((x_central-i[0])**2)+((y_central-i[1])**2)) < 4 : 
                x_central = randint(3, height - 4)
                y_central = randint(3, width - 4)

        lvillage.append((x_central,y_central))
        proprio = liste_joueur.pop()
        map[x_central][y_central].type = TYPE.village
        
        map[x_central][y_central].proprio = proprio

        for i in range(-2, 3):
            for j in range(-2, 3):
                # Condition pour un village en diamand
                if abs(i) + abs(j) <= 2 and abs(i) + abs(j) !=0: #Manhattan distance ≤ 2 (merci gpt) et pas le centre
                    new_x = x_central + i
                    new_y = y_central + j
                    map[new_x][new_y].type = TYPE.plaine
                    map[new_x][new_y].proprio = proprio #a implementerx    



# Générer la carte avec les types de terrain
def generate_map(width, height, scale, nb_village, liste_joueur):
    # Générer le bruit de Perlin
    perlin_noise = generate_perlin_noise(width, height, scale)
    map = []
    # Parcourir la grille de bruit et assigner les types de terrain
    for i in range(height):
        row = []
        for j in range(width):
            noise_value = perlin_noise[i][j]

            # Traitement du bruit
            if noise_value < -0.3:
                row.append(Case(i, j, TYPE.montagne))
            elif -0.1 <= noise_value < 0:
                row.append(Case(i, j, TYPE.foret))
            elif noise_value > 0.3:
                row.append(Case(i, j, TYPE.eau))
            else:
                row.append(Case(i, j, TYPE.plaine))
        map.append(row)

    place_villages(map, nb_village, width, height, liste_joueur)
    return map

# Affichage de la carte avec tkinter
def show_map(map, cell_size):
    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Carte")
    
    # Créer un Canvas pour dessiner la carte
    canvas = tk.Canvas(root, width=width * cell_size, height=height * cell_size)
    canvas.pack()
    
    # Définir les couleurs pour chaque type de terrain
    colors = {
        TYPE.plaine: "lightgreen",
        TYPE.montagne: "gray",
        TYPE.eau: "blue",
        TYPE.foret: "darkgreen",
        TYPE.village: "brown"
    }
    
    # Dessiner chaque cellule de la carte
    for l in map:
        for c in l:
            color = colors.get(c.type, "white")  # Obtenir la couleur correspondante sinon white
            x0 = c.x * cell_size
            y0 = c.y * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size


            # Dessiner un rectangle rempli avec la couleur du terrain
            canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

            # Ajouter des rayures pour indiquer le territoire
            if c.proprio and c.type != TYPE.village:
                # Dessiner des lignes diagonales (rayures)
                step = 10
                for k in range(0, cell_size+1, step):  # Lignes espacées de 10 pixels                   
                    canvas.create_line(x0 + k, y0, x0, y0 + k, fill=c.proprio.couleur, width=1)  # Diagonale de haut à gauche vers bas à droite
                    canvas.create_line(x1 - k, y1, x1, y1 - k, fill=c.proprio.couleur, width=1)  # Diagonale de haut à gauche vers bas à droite
    # Lancer la boucle principale de l'interface Tkinter
    root.mainloop()

# Exemple d'utilisation
width, height, scale, nb_village = 15, 15, 10.0, 2
cell_size = 50  # Taille de chaque cellule dans la fenêtre
P1= Seigneur("main","cara",18,120,5,200,"red")
P2= Seigneur("bot","cara",18,120,5,200,"violet")
liste_joueur=[P1,P2]
map = generate_map(width, height, scale, nb_village, liste_joueur)    
show_map(map, cell_size)
