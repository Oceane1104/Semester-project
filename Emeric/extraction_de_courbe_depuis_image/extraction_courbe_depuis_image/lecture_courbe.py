# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 10:37:13 2024

@author: emeri
"""

import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image
import os

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

plt.close('all')

#Programme pour transformer une image de courbe (extraite d'un article par exemple) en valeur float et les stocker en fichier texte
#Enregistrer l'image de la courbe à exploiter dans le même dossier que ce programme, avec un titre au format suivant : {echelle_x}{echalle_y}_{nom}_{x_min}_{x_max}_{y_min}_{y_max}.png
#{echelle_x} et {echelle_y} doivent prendre les valeurs lin ou log, selon que les échelles sont linéaires ou logarithmiques. {nom} est le nom que vous voulez donner à la courbe. Les 4 valeurs suivantes sont les débuts et fins des axes d'abscisses et d'ordonnées sur l'image de la courbe
#Rien ne doit apparaitre "au-dessus" de la courbe sur l'image (gommé sur Paint avec un pinceau blanc).
#Mettez dans la variable curve_name le nom qui permet d'identifier de manière unique votre courbe dans le dossier (il suffit que ce nom fasse parti du nom completer de l'image à traiter, et qu'aucune autre image ne comporte morceau de nom)
#Si votre courbe n'est pas noire sur fond blanc (courbe grise ou colorée par exemple), il peut être utile d'abaisser la valeur de la variable thres qui est une variable de seuil pour la detection des pixels de courbes sur l'image.
#Il est possible de normaliser les valeurs de sortie pour que leur intégrale fasse 1 en passant la variable normalization en 'on'. Cela peut-etre utile pour les courbes en unité arbitraire, notamment les spectres en optique.
#Il est également possible d'analyser une courbe de couleur parmi plusieurs courbe colorée, il suffit de rentrer les composantes RGB ou RGBA dans la variable couleur_a_traiter.

#Exemple 1 donné avec une image de conductivité thermique de silicium. Image originale, puis image mise en forme sur Paint (gommage de ce qui est au dessus de la courbe au pinceau blanc et extrapolation de la courbe au pinceau noir) et fichier texte de sortie. Couleur en 'off'.
#Exemple 2 donné avec une image d'indice d'extinction de TiN. Plusieurs courbes de couleur sur le graphique. On peut soit lancer le programme en indiquant deja la couleur nous interressant dans couleur_a_traiter, ou lancer le programme avec couleur_a_traiter = [] pour que le programme nous propose de lui-meme les couleurs apparaissant au moins 'threshold_couleur_presente' fois et choisir ensuite la couleur a etudier. On indique la plage de certitude de cette couleur a l'aide de threshold color.

curve_name = "TiN"
thres = 100
threshold_color = 50      # limite permises de somme des ecarts des composantes RGB entre la couleur demandee et les pixels de l'image, pour être considere comme faisant parti de la courbe etudiee
threshold_couleur_presente = 3     # nombre seuil de pixel d'une même couleur apparus pour proposer cette couleur parmi les couleur disponible
no_blanc = 'on'  # enleve le blanc et ses nuances proches des couleurs de courbe proposees
normalization = 'off'
couleur = 'on'     #off si courbe noire sur fond blanc seule 
couleur_a_traiter = [] #si la couleur est deja connue, ici au format [R,G,B], selon le format d'image utilisé il est parfois nécéssaire d'utiliser le format de couleur RGBA avec 4 parametres


nom_image_curve = [image for image in os.listdir() if ((curve_name in image) and ('extracted' not in image))][0]

print(nom_image_curve)

indice = 0
liste_nombre = ['0','1','2','3','4','5','6','7','8','9']
liste_coor = []
nom_save = ''

lin_log = ''
while nom_image_curve[indice] != '_':
    lin_log += nom_image_curve[indice]
    indice += 1
    
echelle_x = lin_log[:3]
echelle_y = lin_log[3:]

indice += 1
while nom_image_curve[indice] not in liste_nombre:
    nom_save += nom_image_curve[indice]
    indice += 1
nom_save = nom_save[:-1]

indice = 0
while len(liste_coor) != 4:
    if nom_image_curve[indice] in liste_nombre:
        nombre = ''
        while nom_image_curve[indice] in liste_nombre:
            nombre += nom_image_curve[indice]
            indice += 1
        if nombre[0] == '0':
            nombre = '0.' + nombre[1:]
        liste_coor.append(float(nombre))
    else:
        indice += 1
        
vrai_x_debut = liste_coor[0]
vrai_x_fin = liste_coor[1]
vrai_y_debut = liste_coor[2]
vrai_y_fin = liste_coor[3]

file_curve = Image.open(nom_image_curve)
if couleur == 'off':
    file_curve_gray = file_curve.convert('L')
    array_curve = np.array(file_curve_gray)
    for i in range(len(array_curve)):
        for j in range(len(array_curve[i])):
            if array_curve[i,j] < thres:
                array_curve[i,j] = 0
            else :
                array_curve[i,j] = 255
    
                
elif couleur == 'on':
    file_curve_color = np.array(file_curve)
    if couleur_a_traiter == [] :
        toute_couleur_dispo = []
        occurance_couleur = []
        for i in range(len(file_curve_color)):
            for j in range(len(file_curve_color[i])):
                
                if no_blanc == 'on':
                    if sum(list(file_curve_color[i,j])) < (255*len(list(file_curve_color[i,j])) - threshold_color) :
                        if list(file_curve_color[i,j]) not in toute_couleur_dispo :
                            toute_couleur_dispo.append(list(file_curve_color[i,j]))
                            occurance_couleur.append(1)
                        else:
                            occurance_couleur[toute_couleur_dispo.index(list(file_curve_color[i,j]))] = occurance_couleur[toute_couleur_dispo.index(list(file_curve_color[i,j]))] +1            
                else:
                    if list(file_curve_color[i,j]) not in toute_couleur_dispo :
                        toute_couleur_dispo.append(list(file_curve_color[i,j]))
                        occurance_couleur.append(1)
                    else:
                        occurance_couleur[toute_couleur_dispo.index(list(file_curve_color[i,j]))] = occurance_couleur[toute_couleur_dispo.index(list(file_curve_color[i,j]))] +1
        couleur_dispo = []
        for i in range(len(occurance_couleur)):
            if occurance_couleur[i] > threshold_couleur_presente:
                couleur_dispo.append(toute_couleur_dispo[i])
        print('couleurs des courbes présentes : ' )
        print(couleur_dispo)
        print('Quelle couleur de courbe analyser? Format R,G,B')
        couleur_a_traiter = input()
        couleur_a_traiter = couleur_a_traiter.split(',')
        couleur_a_traiter = [int(couleur) for couleur in couleur_a_traiter]
    array_curve = np.array(file_curve_color)
    array_curve_copy = np.zeros(np.shape(array_curve)[:2])
    for i in range(len(array_curve)):
        for j in range(len(array_curve[i])):
            if sum([abs(list(array_curve[i,j])[k] - couleur_a_traiter[k]) for k in range(len(couleur_a_traiter))]) < threshold_color :
                array_curve_copy[i,j] = 0
            else :
                array_curve_copy[i,j] = 255
    array_curve = array_curve_copy



liste_point = []
transposee = array_curve.T
for i in range(len(transposee)):
    j = 0
    while transposee[i,j] != 0:
        j += 1 
        if j == len(transposee[i]):
            print("pas de point trouvé en x = " + str(i))
            break
    if j < len(transposee[i]):
        liste_point.append([i,j])

taille = np.shape(array_curve)
taille_x = taille[1]
taille_y = taille[0]

liste_vraie_point = [[],[]]

if echelle_x == 'lin':
    for point in liste_point:
        liste_vraie_point[0].append(vrai_x_debut+point[0]/taille_x*(vrai_x_fin-vrai_x_debut))

elif echelle_x == 'log':
    for point in liste_point:
        liste_vraie_point[0].append(vrai_x_debut*(vrai_x_fin/vrai_x_debut)**(point[0]/taille_x))
        
if echelle_y == 'lin':
    for point in liste_point:
        liste_vraie_point[1].append(vrai_y_debut+(taille_y-point[1])/taille_y*(vrai_y_fin-vrai_y_debut))
        
elif echelle_y == 'log':
    for point in liste_point:
        liste_vraie_point[1].append(vrai_y_debut*(vrai_y_fin/vrai_y_debut)**((taille_y-point[1])/taille_y))
    
if normalization == 'on':
    coef_normalization = sum(liste_vraie_point[1])
    
    for i in range(len(liste_vraie_point[1])):
        liste_vraie_point[1][i] = liste_vraie_point[1][i]/coef_normalization
        
if couleur == 'on':
    plt.plot(liste_vraie_point[0],liste_vraie_point[1], color=rgb_to_hex(couleur_a_traiter))
else:
    plt.plot(liste_vraie_point[0],liste_vraie_point[1], color='black')

if echelle_x == 'log':
    plt.xscale('log')
if echelle_y == 'log':
    plt.yscale('log')
plt.show()

file_save = open(nom_save+'_extracted','w')
file_save.write(str(liste_vraie_point[0])[1:-1])
file_save.write('\n')
file_save.write(str(liste_vraie_point[1])[1:-1])

        

