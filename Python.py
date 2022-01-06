#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  3 15:58:53 2021

@author: ameliedumoulin

"""

#IMPORTATION DES LIBRAIRIES NECESSAIRES
import spotipy
import pandas as pd
import lyricsgenius as lg
import ClassesProjet
from ClassesProjet import *
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data

# =================== GENIUS ================= #
#Authentification à Genius , API qui récupère les paroles de chanson
genius = lg.Genius('J0Mx3P3fHokEswefcn3T0zSuMOa5vL8VM7I4DRXG2_W34canTkZO3k8mC3wOAW9u')

# =================== SPOTIFY ================= #
#Authentification à Spotipy , API qui nous permet de récupérer le TOP 50 FRANCE
client_id = "78ef759cd12c49b89be0cb60a814569f"
client_secret = "1e988937a84e4df69d446ea96a949c15"
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API


#========= 1er interface graphique ========#
# ========== Fonctions =========#

#Permet de faire deux fonctions
def two_funcs(*funcs):
    def two_funcs(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return two_funcs

#Permet de fermer la fenetre
def destroy():
    global window
    window.destroy()
#Renvoie la playlist URI saisie par l'utilisateur    
def afficher():
    global playlist_uri 
    playlist_uri = e.get() #Récupère la valeur de l'entrée
    print(playlist_uri)

# ======= Interface =======#
from tkinter import *
from tkinter.ttk import Combobox
#Initialisation
window=Tk()

l = Label(window,text="Playlist URI")
l.pack(side=LEFT) 

#permet l'entrée de la playlist
e= Entry(window)
e.pack(side=RIGHT)

#Quand on appuie sur ll e botuon, execution de quit et afficher
fermer = Button(window,text="OK",command = two_funcs(afficher,destroy)).pack(side=RIGHT) 

window.title('Playlist')
window.geometry("300x200+10+10")
#Lancement de l'interface
window.mainloop()


#==================== Requête Spotify ============#
#Récupération de la playlist - TOP 50 FRANCE dans l'exemple

playlist = sp.playlist(playlist_uri) 

pd.json_normalize(playlist)#On transforme le dictionnaire en dataframe
playlist_items = sp.playlist_items(playlist_uri)

df = pd.json_normalize(playlist_items['items']) #On transforme le dictionnaire en dataframe
filter_cols = [col for col in df if col.startswith('track')] #On prend les colonnes qui commencent par 'track'
df = df[filter_cols] #On ne garde que ces colonnes
df.columns = [col.replace("track.","") for col in df] #On remplace le mot track par un espace pour mieux lire les colonnes

data = [] 

titre = df['name'] # Récupère le titre dans le dataframe df 


for a in df['artists']: #Pour chaque élement de df[artist] (df[artist] = dictionnaire)
    
        result = pd.json_normalize(a) #On transforme le dictionnaire en dataframe
        name = result['name'] #Nom de l'artiste
        uri = result['uri'] # Uri de l'artiste sur spotify    
        artist_info = sp.artist(uri[0])
        followers = artist_info['followers']['total'] #Nombre de followers
        try:  
            genres = artist_info['genres'][0] #Genre de l'artiste  
        except:
            genres = "undefined"
        popularity = artist_info['popularity'] #Popularité       
        data.append((name[0],genres, popularity)) # On ajoute les 3 éléments à un tableau
    
        
        
#DF1 = tableau clair avec classement, titre, artiste, genre...    
df1 = pd.DataFrame(data, columns = ('artist', 'genres', 'artist_popularity'))
df1.insert(0,"Classement",df1.index+1)
df1.insert(2,"Titre",titre) #On ajoute les titres au DataFrame

artiste=df1.artist

#Classe Musique
Musique = Musique(df1['Titre'],artiste,df1['genres'],df1['Classement']) 

#On instancie les dictionnaire et la liste des genres
dic=dict()
dicgenre=dict()
genre=[]

#On utilise la classe Repartition et sa fonction get pour les récupérer
#A partir des genre récupérer
genre,dicgenre,dic = Repartition(dic,dicgenre,genre).get(Musique)

#On récupère les paroles
paroles=""  
#for cle in dicgenre: 
for i in range(len(genre)):
    paroles=""
    for j in range(len(dicgenre[genre[i]])):
        try:
            songs = genius.search_song(dicgenre[genre[i]][0][j], dicgenre[genre[i]][1][j]) #On cherche les paroles de la chanson du bon chanteur
            paroles = paroles + str(songs.lyrics.split("\n")) + "\n"
            dic[genre[i]]= paroles.lower() #On ajoute les paroles à la clé ( = chanson correspondante)
            # print(songs.lyrics) #Paroles           
        except:
            print("exception ")#Si problème, on écrit exception et on continue

#Mise en forme des paroles
import re

#On enlève les symboles et accent et on split au ' - et ,
for i in range (len(genre)):
    dic[genre[i]] = re.sub("[!@#$:()/\.?]", '',dic[genre[i]])
    dic[genre[i]] = re.sub('[""]', '', dic[genre[i]])
    dic[genre[i]]= re.sub("[0-9]", '', dic[genre[i]])
    dic[genre[i]] = re.sub("[éèê]", 'e', dic[genre[i]])
    dic[genre[i]] = re.sub("[àâ]", 'a', dic[genre[i]])
    dic[genre[i]] = re.sub("[ù]", 'u', dic[genre[i]])
    dic[genre[i]]= re.sub("[î]", 'i', dic[genre[i]]) 
    dic[genre[i]] = re.sub(r"[\([{})\]]", "", dic[genre[i]])
    dic[genre[i]] = re.split("[ '-,]",dic[genre[i]])


#On crée les liste de mot
liste_mots=[]


#On stocke les stopword grace à la classe stopword
stopword = stopword().get()

#On garde les mots qui ne sont pas des stopword et qui ont + de 4 lettres
dic2=dict()
for i in range(len(dic)):
    liste_mots.append([])
    for j in range(len(dic[genre[i]])):
        if ((dic[genre[i]][j] not in stopword) and (len(dic[genre[i]][j])>4)):
            liste_mots[i].append(dic[genre[i]][j])
            dic2[genre[i]]=list(set(liste_mots[i])) 
    
#On crée la matrice genre - terme pour chaque genre              
import numpy

for i in range(len(genre)):
    ncol=len(dic2[genre[i]])
    nrow=1 #1 seul ligne car par genre 
    M=numpy.zeros((nrow,ncol)) #Création du tableau rempli de 0
    for j in range(ncol):
        for k in range(len(liste_mots[i])):
            if dic2[genre[i]][j] == liste_mots[i][k]: #Si le mot apparait dans la liste
                M[0,j]=M[0,j]+1  #On ajoute 1             
    M = pd.DataFrame(M,index = [genre[i]],columns=dic2[genre[i]])#Transformation en DF
    dic[genre[i]]=M
 
    
dicfinale=dict()
liste_finale=[]


for i in range(len(genre)):
    liste_finale.append([])
    for j in dic[genre[i]]:
        if int(dic[genre[i]][j]) > 3:
          liste_finale[i].append(j)
    dicfinale[genre[i]]=liste_finale[i]


genremax=""
nbmotsmax=0
nbchansonmax = 0
genremin=""
nbmotsmin=0
nbchansonmin = 0
#r = GenrePopulaire(dicfinale,dic,genre,dicgenre,genremax,nbmotsmax,nbchansonmax).Maximum()
#m = MoinsPopulaire(dicfinale,dic,genre,dicgenre,genremin,nbmotsmin,nbchansonmin).Minimum()
  
#=============== Interface graphique ===========#
#=============== Fonctions =============== #

def plot():
    
    newWindow = Toplevel(window2)
    newWindow.title("Nuage de mots du genre " + str(cb.get()))
    import wordcloud
    from wordcloud import WordCloud, STOPWORDS 
    import matplotlib.pyplot as plt
    
    wordcloud = WordCloud(width = 800, height = 800, 
                    background_color ='white',
                    min_font_size = 10).generate(str(dicfinale[cb.get()])) 
      
    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')
    plt.title("Mots les plus récurrents : " + str(cb.get()))
    plt.imshow(wordcloud)
    plt.show()
    canvas = FigureCanvasTkAgg(fig,master = newWindow)   
    canvas.draw() 
  
    
    canvas.get_tk_widget().pack() 
  
    
    toolbar = NavigationToolbar2Tk(canvas, newWindow) 
    toolbar.update() 
  
    
    canvas.get_tk_widget().pack() 
    
 
def Table():
    newWindow = Toplevel(window2)
    newWindow.title(cb.get())
    for i in range(len(dicfinale[cb.get()])): 
                  
                e = Entry(newWindow, width=20, fg='black', 
                               font=('Arial',16,'bold')) 
                  
                e.grid(row=i) 
                e.insert(END, dicfinale[cb.get()][i]) 
 
def Polymorphisme():
    
    if cb2.get()=="Plus populaire":
        newWindow = Toplevel(window2)
        newWindow.title ("Plus populaire")
        var = StringVar()
        label = Label(newWindow, textvariable=var, relief=RAISED)
        x = GenrePopulaire(dicfinale,dic,genre,dicgenre,genremax,nbmotsmax,nbchansonmax).Maximum()
        var.set("Le genre le plus écouté est "+str(x[0])+" avec "+str(x[1])+" chansons et "+ str(x[2])+" mots.")
        label.pack()
        
    elif cb2.get() == "Moins Populaire":
        newWindow = Toplevel(window2)
        newWindow.title("Moins populaire")
        var = StringVar()
        label = Label(newWindow, textvariable=var, relief=RAISED)
        x = MoinsPopulaire(dicfinale,dic,genre,dicgenre,genremax,nbmotsmax,nbchansonmax).Minimum()
        var.set("Le genre le moins écouté est "+str(x[0])+" avec "+str(x[1])+" chansons et "+ str(x[2])+" mots.")
        label.pack()
                
  
#============= Interface ==== #

from tkinter import *
from tkinter.ttk import Combobox
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
window2=Tk()

cb=Combobox(window2, values=genre)
cb.current(1)
cb.place(x=60, y=150)

cb2 = Combobox(window2,values=["Plus populaire","Moins Populaire"])
cb2.current(0)
cb2.place(x=60, y = 75)

Afficher = Button(master = window2, text ="Afficher", command = Table)
Afficher.place(x=275,y=150)


Afficher = Button(master = window2, text ="Afficher", command = Polymorphisme)
Afficher.place(x=275,y=75)

plot_button = Button(master = window2,command = plot, text = "Nuage de mots") 
plot_button.place(x=275,y=190) 



window2.title("Genre")
window2.geometry("400x300+10+10")
window2.mainloop()



 