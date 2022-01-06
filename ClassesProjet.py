#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 00:23:01 2021

@author: ameliedumoulin
"""

#Classe Mère qui récupère le nom de l'artiste et la chanson figurant dans le TOP50
class Musique:

    def __init__(self,titre,artiste,genre,classement):
        self.titre = titre 
        self.artiste = artiste
        self.classement = classement
        self.genre = genre
           
    # =============== 2.2 : REPRESENTATIONS ===============
    # Fonction qui renvoie le texte à afficher lorsqu'on tape repr(classe)
    def __repr__(self):
        print("La chanson "+ self.titre + " par "+ self.artiste)
    # Fonction qui renvoie le texte à afficher lorsqu'on tape str(classe)
    def __str__(self):
        print (f"{self.titre}, par {self.artiste}"    )  


class Repartition:
    
    def __init__(self,dic,dicgenre,genre):

        self.dic=dic
        self.dicgenre=dicgenre
        self.genre=genre
    
    def get(self,Musique):
        
        import pandas as pd
 
        #On met tout les genres présents dans une liste
        for valeur in Musique.genre:
            if valeur not in self.genre:
                self.genre.append(valeur)    
        
        #Pour chaque genre, on ajoute les chansons de ce genre
        genremusique=[]    
        for i in range(len(self.genre)):
            genremusique.append([])
            for j in range(len(Musique.titre)):
                if self.genre[i] == Musique.genre[j]:
                    genremusique[i].append([Musique.titre[j],Musique.artiste[j]])
                    self.dicgenre[self.genre[i]]= pd.DataFrame(genremusique[i])
        return(self.genre,self.dicgenre,self.dic)  
    
         
class stopword:
    
    def __init__(self):
        self.stopword=[]
        
    def get(self):
        import re
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        from stop_words import get_stop_words
        
        #Mot français
        self.stopword = stopwords.words('french')
        self.stopword.extend(list(get_stop_words('fr')))
        #Mot anglais
        self.stopword.extend(stopwords.words('english'))
        self.stopword.extend(list(get_stop_words('en')))
        
        #Mise en forme des accents pour que ça corresponde aux paroles
        for i in range(len(self.stopword)):
            self.stopword[i] = re.sub("[éèê]", 'e', self.stopword[i])
            self.stopword[i] = re.sub("[àâ]", 'a', self.stopword[i])
            self.stopword[i] = re.sub("[ù]", 'u', self.stopword[i])
            self.stopword[i] = re.sub("[î]", 'i', self.stopword[i])
        return(self.stopword)


class GenrePopulaire(Repartition):
    
    def __init__(self,dicfinale,dic,genre,dicgenre,genremax,nbmotsmax,nbchansonmax):
        Repartition.__init__(self,dic,dicgenre,genre)
        
        self.dicfinale=dicfinale
        self.genremax=genremax
        self.nbmotsmax=nbmotsmax
        self.nbchansonmax = nbchansonmax
        
    def Maximum(self):
             
            for valeur in self.genre:
               if self.nbmotsmax < len(self.dicfinale[valeur]):
                   self.nbmotsmax = len(self.dicfinale[valeur])
               if self.nbchansonmax < len(self.dicgenre[valeur]):
                   self.nbchansonmax = len(self.dicgenre[valeur])
                   self.genremax = valeur
            print("Le genre le plus populaire de la playlist est "+ self.genremax + " avec "+ str(self.nbchansonmax) + " chansons")

            return(self.genremax,self.nbchansonmax,self.nbmotsmax)
        
    def getType(self):
        return "PlusPopulaire"    
        
    
        
class MoinsPopulaire(Repartition):
    
     def __init__(self,dicfinale,dic,genre,dicgenre,genremin,nbmotsmin,nbchansonmin):
        Repartition.__init__(self,dic,dicgenre,genre)
        
        self.dicfinale=dicfinale
        self.genremin=""
        self.nbmotsmin=2
        self.nbchansonmin = 2
        
     def Minimum(self):

        for valeur in self.genre:
            if self.nbmotsmin > len(self.dicfinale[valeur]):
                self.nbmotsmin = len(self.dicfinale[valeur])
            if self.nbchansonmin > len(self.dicgenre[valeur]):
               self.nbchansonmin = len(self.dicgenre[valeur])
               self.genremin = valeur 
        print("Le genre le moins populaire de la playlist est "+ self.genremin + " avec "+ str(self.nbchansonmin) + " chansons")
        return(self.genremin,self.nbchansonmin,self.nbmotsmin)
    
     def getType(self):
        return "MoinsPopulaire"

