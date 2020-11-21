#working on heatmap
import csv 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ast

with open('data_by_genres.csv', newline='') as csvfile:
    genre_data=csv.DictReader(csvfile)
    genres_list=["pop", 'traditional country', "jazz", 'metal']
    attribute_list=['acousticness', 'energy', 'danceability', 'liviness']
    acousticness=[]
    energy=[]
    danceability=[]
    liviness=[]

    for genre in genres_list:
        acousticness.append(0)
        energy.append(0)
        danceability.append(0)
        liviness.append(0)
    
    for row in genre_data:
        len_genres_list=len(genres_list)
        for i in range(len_genres_list):
            genre=genres_list[i]
            if genre==row['genres']:
                acousticness[i]= row['acousticness']
                danceability[i]=row['danceability']
                energy[i]=row['energy']
                liviness[i]=row['liveness']
    
    acousticness=list(map(float, acousticness))
    energy = list(map(float, energy))
    danceability = list(map(float, danceability))
    liviness = list(map(float, liviness))
    new_a=[acousticness, danceability,energy, liviness]
    
    print(danceability)
    print(new_a)
    #new_a= list(map(float,a))
    
    fig, ax=plt.subplots()
    im=ax.imshow(new_a)
    plt.colorbar(im)
    
    ax.set_xticks(np.arange(len(genres_list)))
    ax.set_yticks(np.arange(len(attribute_list)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(genres_list)
    ax.set_yticklabels(attribute_list)
    
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    
    # Loop over data dimensions and create text annotations.
    for i in range(len(attribute_list)):
        for j in range(len(genres_list)):
            x=float(f"{new_a[i][j]:.3f}")
            text = ax.text(j, i, x,
                           ha="center", va="center", color="w")

    ax.set_title("Genre Comparison")
    fig.tight_layout()
    plt.show()
        