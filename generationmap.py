import numpy as np
import tkinter as tk
from perlin_noise import PerlinNoise
import random
from Case import Case
from TYPE import TYPE 
from math import sqrt
from Seigneur import Seigneur
import matplotlib.pyplot as plt

# Générer la grille de bruit de Perlin
def generate_perlin_noise(width, height, seed=None):
    noise1 = PerlinNoise(octaves=3, seed = seed)
    noise2 = PerlinNoise(octaves=6, seed= seed)
    noise3 = PerlinNoise(octaves=12, seed=seed)
    noise4 = PerlinNoise(octaves=24, seed=seed)

    
    pic = []
    for i in range(height):
        row = []
        for j in range(width):
            noise_val = noise1([i/height, j/width])
            noise_val += 0.5 *noise2([i/height, j/width])
            noise_val += 0.25 * noise3([i/height, j/width])
            noise_val += 0.125 * noise4([i/height, j/width])

            row.append(noise_val)
        pic.append(row)
    # plt.imshow(pic, cmap='gray')
    # plt.show()
    return pic
    

# Fonction pour placer les villages
def place_villages(map, nb_village, width, height, liste_joueur, seed = None):
    if seed is not None:
        random.seed(seed)
    lvillage=[] #liste des tuples des pos des villages
    for _ in range(nb_village):
        # Choisir des coordonnées aléatoires pour le village
        x_central = random.randint(3, height - 4)
        y_central = random.randint(3, width - 4) # pas de village trop au bord
        for i in lvillage:
            while sqrt(((x_central-i[0])**2)+((y_central-i[1])**2)) < 4 : 
                x_central = random.randint(3, height - 4)
                y_central = random.randint(3, width - 4)

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
def generate_map(width, height, nb_village, liste_joueur, seed):
    
    # Générer le bruit de Perlin
    perlin_noise = generate_perlin_noise(width, height,seed )
    map = []
    # Parcourir la grille de bruit et assigner les types de terrain
    for j in range(height):
        row = []
        for i in range(width):
            noise_value = perlin_noise[j][i]

            # Traitement du bruit
            if noise_value < -0.4:
                row.append(Case(i, j, TYPE.montagneclair))
            elif noise_value < -0.25:
                row.append(Case(i, j, TYPE.montagne))
            elif -0.1 <= noise_value < 0:
                row.append(Case(i, j, TYPE.foret))
            elif -0.15<= noise_value < -0.1 or 0 < noise_value <= 0.05:
                row.append(Case(i, j, TYPE.foretclair))
            elif noise_value > 0.3:
                row.append(Case(i, j, TYPE.eau))
            elif noise_value > 0.25:
                row.append(Case(i, j, TYPE.eauclair))
            else:
                row.append(Case(i, j, TYPE.plaine))
        map.append(row)

    place_villages(map, nb_village, width, height, liste_joueur,seed )
    return map

# Affichage de la carte avec tkinter
def show_map(map, width , height, cell_size):
    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Carte")
    
    # Créer un Canvas pour dessiner la carte
    canvas = tk.Canvas(root , height=height * cell_size , width=width * cell_size)
    canvas.pack()
    
    # Définir les couleurs pour chaque type de terrain
    colors = {
        TYPE.plaine: "palegoldenrod",
        TYPE.montagne: "gray",
        TYPE.montagneclair: "lightgray",
        TYPE.eau: "steelblue",
        TYPE.eauclair: "lightskyblue",
        TYPE.foret: "darkgreen",
        TYPE.foretclair: "forestgreen",
        TYPE.village: "brown"
    }
    print(map)
    # Dessiner chaque cellule de la carte
    for h in map:
        for c in h:
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
width= 60
height = 40
nb_village = 2
seed = 15153
cell_size = 10 # Taille de chaque cellule dans la fenêtre
P1= Seigneur("main","cara",18,120,5,200,"red")
P2= Seigneur("bot","cara",18,120,5,200,"violet")
liste_joueur=[P1,P2]
map = generate_map(width, height, nb_village, liste_joueur, seed)    
show_map(map,width,height, cell_size)
