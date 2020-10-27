#from lxml import etree
import json
import requests
import sys
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from gensim.models import TfidfModel
from gensim import corpora
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from collections import defaultdict
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import WordNetLemmatizer


#Realise une requete sur la BDD de Marvel et construit un json contenant les descriptions des comics dans lesquels un personnage donné apparait
def create_text(id,nom_fichier):

    #declaration de la chaine de caracteres et requete
    string_descript = {}
    query_total = requests.get('https://gateway.marvel.com:443/v1/public/characters/'+ str(id) +'/comics?limit=100&apikey=0de024649f971af7cbb0729ac0bb16a1', headers={'referer': 'localhost'})

    print("Code de retour=>",query_total.status_code)

    #recuperation du resultat de la requete
    if query_total.status_code == 200:
             data_reply = query_total.json()
             total = data_reply["data"]["total"]
             print('total=',str(total))
    else:
             print("Erreur de telechargement")

    #boucle pour remplir la chaine des descriptions
    for i in range (0,total+100,100):
        query_descript = requests.get('https://gateway.marvel.com:443/v1/public/characters/' + str(id) + '/comics?limit=100&offset=' + str(i) + '&apikey=0de024649f971af7cbb0729ac0bb16a1', headers={'referer': 'localhost'})
        print("Code de retour=>",query_descript.status_code)
        print(i)
        if query_descript.status_code == 200:
                 data_reply_descript = query_descript.json()
                 for data in data_reply_descript["data"]["results"]:
                    if(data["description"] and data["description"] is not None):
                        string_descript[data["title"]]=data["description"]

        else:
                 print("Erreur de telechargement étape descript")

    print('taille finale : ',len(string_descript))

    #on remplit le nouveau json avec les descriptions des comics
    with open('static/' + nom_fichier + '.json', 'w') as outfile:
        json.dump(string_descript, outfile)

#CREATION DES JSON DE NOS PERSONNAGES CHOISIS
#create_text(1009504,'PrX_original')
#create_text(1009664,'Thor_original')
#create_text(1009662,'Thing_original')
# create_text(1009368,'IronMan_original')
# create_text(1009220,'CaptainAmerica_original')
# create_text(1009189,'BW_original')
# create_text(1009356,'Torch_original')
# create_text(1009366,'InvisibleW_original')
# create_text(1009459,'MrF_original')
# create_text(1009718,'Wolverine_original')
# create_text(1009629,'Storm_original')
# create_text(1009465,'Mystique_original')



#Nettoie une chaine de caractere pour qu'elle soit mise en forme pour le WordCloud
def clean_text(mystring,perso):

    tokens = word_tokenize(mystring)
    #on met le texte en minuscules
    tokens=[w.lower() for w in tokens]

    #on sort la ponctuation
    table=str.maketrans('','', string.punctuation)
    stripped=[w.translate(table) for w in tokens]

    #enlever les elements non alphabétiques
    words=[word for word in stripped if word.isalpha()]

    #enlever les caracteres codant les sauts de ligne
    unwanted_words = {"\n"}

    #pour chaque json d'un perso donné, on enlève son nom de la chaine de caractere descriptive (car inutilement redondante)
    perso=perso.split(" ")
    for i in range (0,len(perso)) :
        unwanted_words.add(perso[i])

    #on enleve les mots "vides"
    stop_words = set(stopwords.words('english'))
    new_sentence = ""


    #declaration d'un lemmatizer
    lemmatizer = WordNetLemmatizer()


    #On stem les mots qu'on a retenu
    for word in words :
        if (word not in stop_words and word not in unwanted_words and len(word)>2):
            if(len(lemmatizer.lemmatize(word))>2):
                new_sentence = new_sentence + " " + lemmatizer.lemmatize(word)

    #print(new_sentence)
    return new_sentence




#Utilise la fonction précédente pour nettoyer un dictionnaire (qu'on appliquera sur les json de nos personnages)
def clean_dico(file, perso):

    #charge le fichier spécifié
    with open(file + '_original.json') as json_file:
        data=json.load(json_file)

    dico_temp={}

    #nettoie le contenu de ce fichier
    for title,descript in data.items():
            dico_temp[title]=clean_text(str(descript),str(perso))

    #ecrit le dictionnaire nettoyé dans un nouveau json
    with open(file+'.json', 'w') as outfile:
        json.dump(dico_temp, outfile)


#NETTOYAGE DES JSON DE NOS PERSONNAGES
# clean_dico("static/PrX","professor xavier")
# clean_dico("static/Thing","thing")
# clean_dico("static/Thor","thor")
# clean_dico("static/IronMan","iron man")
# clean_dico("static/CaptainAmerica","captain america")
# clean_dico("static/BW","black widow")
# clean_dico("static/Torch","human torch")
# clean_dico("static/InvisibleW","invisble woman")
# clean_dico("static/MrF","mr fantastic")
# clean_dico("static/Wolverine","wolverine")
# clean_dico("static/Storm","storm")
# clean_dico("static/Mystique","mystique")


