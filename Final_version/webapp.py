#-*- coding: utf-8 -*-
import time
from flask import *
from json import *
from tulip import tlp
import requests
import sys
from jinja2 import Environment, PackageLoader
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

env = Environment(loader=PackageLoader('webapp','templates'))



app = Flask(__name__)
#app = Flask("Mon serveur")

#Fonction qui revoie vers le template qui gère notre accueil
@app.route('/')
def welcome():
         return render_template("welcome.html")

#Fonction qui revoie vers le template qui gère notre accueil
@app.route('/choix_visu')
def accueil():
         return render_template("accueil.html")

#Route vers la page accueil de notre graphe
@app.route('/accueil_graph')
def accueil_graph():
        return render_template("accueil_graph.html")

#Route vers la page qui permet de choisir l'univers du héro qu'on voudra étudier
@app.route('/choix_monde')
def choix_monde():
    return render_template("Choix_monde.html")

#Route vers la page permettant la séléction d'un personnage d'Avengers pour la visualisation de sonn WordCloud
@app.route('/avengers')
def avengers():
    return render_template("avengers.html")

#Route vers la page permettant la séléction d'un personnage des Fantastic-Four pour la visualisation de sonn WordCloud
@app.route('/ff')
def ff():
    return render_template("ff.html")

#Route vers la page permettant la séléction d'un personnage des X-Men pour la visualisation de sonn WordCloud
@app.route('/xmen')
def xmen():
    return render_template("xmen.html")


#Route vers le graphe interactif du personnage en question
@app.route('/affiche')
def aff():
        heros=request.args.get("heros")
        print("recup :"+heros)
        return render_template("mongraphe.html",hero=heros)


#Fonction qui crée et genère le graphe
@app.route('/graph')
def generate_graph():
        #creation d'un nouveau graphe vide
         graph=tlp.newGraph()

         comic = graph.getStringProperty("comic")
         hero = graph.getStringProperty("hero")
         type_ = graph.getStringProperty("type")
         viewBorderColor = graph.getColorProperty("viewBorderColor")
         viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
         viewColor = graph.getColorProperty("viewColor")
         viewFont = graph.getStringProperty("viewFont")
         viewFontSize = graph.getIntegerProperty("viewFontSize")
         viewIcon = graph.getStringProperty("viewIcon")
         viewLabel = graph.getStringProperty("viewLabel")
         viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
         viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
         viewLabelColor = graph.getColorProperty("viewLabelColor")
         viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
         viewLayout = graph.getLayoutProperty("viewLayout")
         viewShape = graph.getIntegerProperty("viewShape")
         viewSize = graph.getSizeProperty("viewSize")
         type_node=graph.getIntegerProperty("Type")

         #Fonction qui crée les noeuds en leur affectant le nom du comic ou du personnage, le type de noeud (noeud du personnage central, d'un comic, d'un personnage autre) et le graphe auquel ça s'applique
         def create_node(nom, type, graph):
             n1=graph.addNode()
             viewLabel[n1]=nom
             type_node[n1]=type
             return n1

         name=request.args.get("name")

         char_hash= {}
         comic_hash={}

         #on récupère les données sur le personnage central depuis le site Marvel
         r= requests.get('https://gateway.marvel.com:443/v1/public/characters?name='+name+'&limit=100&apikey=4dff50d15e38e094affa81c7191ac0bd', headers={'referer': 'localhost'})

         id_hero=-1
         print("Code de retour=>",r.status_code)

         if r.status_code == 200:
                  data_reply = r.json()
                  print("Nombre de personnages trouve : ", len(data_reply["data"]["results"]));
                  for character in data_reply["data"]["results"]:
                           print("id personnage=>", character['id'], " xx nom personnage=>", character['name'])
                           id_hero=character['id']
         else:
                  print("Erreur de telechargement")

        #On récupère les données sur les comics dans lesquels apparaît notre personnage central ainsi que les autres personnages qui apparaissent dans ces comics.
         r2= requests.get('https://gateway.marvel.com:443/v1/public/characters/'+str(id_hero)+'/comics?limit=100&apikey=4dff50d15e38e094affa81c7191ac0bd', headers={'referer': 'localhost'})

         if r2.status_code == 200:
                  data_reply2 = r2.json()

        #Boucle qui crée le noeud central et rempli le dictionnaire json
         for character in data_reply["data"]["results"]:
                n1=create_node(character["name"],0,graph)
                char_hash[character["name"]]=n1


        #Boucle qui crée les noeuds des comics et rempli le dictionnaire json
         for comic in data_reply2["data"]["results"]:
             node= create_node(comic["title"],1,graph)
             comic_hash[comic["title"]]=node

        #Création des arrêtes
         for target in graph.getNodes() :
                  if type_node[target]==0:
                           source=target
         graph.addEdge(source,target)

         #Boucle qui crée les noeuds des autres personnages et rempli le dictionnaire json
         for comic in data_reply2["data"]["results"]:
                  for name in comic["characters"]["items"]:
                           if name["name"] in char_hash.keys():
                                    n=char_hash[name["name"]]
                           else:
                                    n=create_node(name["name"],2,graph)
                                    char_hash[name["name"]]=n

                           destination=comic_hash[comic["title"]]
                           graph.addEdge(n,destination)

        #Création du json
         gjson={'nodes':[],'links':[]}
         for n in graph.getNodes():
                  gjson['nodes'].append({'id':viewLabel[n],'group':type_node[n]})
         for e in graph.getEdges():
                  gjson['links'].append({'source':viewLabel[graph.source(e)],'target':viewLabel[graph.target(e)],'value':1})


         return jsonify(gjson)





@app.route('/tfidf', methods=['GET','POST'])
def our_tfidf():

    #recuperation du personnage selectioné
    perso=request.args.get("perso")

    #chargement du fichier en question
    if (perso=='Professor X'):
        file = 'PrX'
    elif (perso=='Thor'):
        file = 'Thor'
    elif (perso=='Iron Man'):
        file = 'IronMan'
    elif (perso=='Captain America'):
        file = 'CaptainAmerica'
    elif (perso=='Black Widow'):
        file = 'BW'
    elif (perso=='Human Torch'):
        file = 'Torch'
    elif (perso=='Invisible Woman'):
        file = 'InvisibleW'
    elif (perso=='Mr. Fantastic'):
        file = 'MrF'
    elif (perso=='Wolverine'):
        file = 'Wolverine'
    elif (perso=='Storm'):
        file = 'Storm'
    elif (perso=='Mystique'):
        file = 'Mystique'
    elif(perso=='The Thing'):
        file = 'Thing'

    #nombre de mots par defaut
    if request.method=='GET' :
        nb_saisi=200
    #si l'utilisateur choisit un autre nombre de mots    
    else :
        nb_saisi=request.form['nombre']
        nb_saisi=abs(int(nb_saisi))

    #wael_path = 'C:/Users/waelb/Documents/GitHub/VizuFinal/Final_version/static/'+file+'.json'
    #with open(wael_path) as json_file:
    with open('static/'+file+'.json') as json_file:
        dico=json.load(json_file)

    string_descript=""

    #pour ne pas avoir d'espaces ni au debut ni a la fin
    i=True
    for t in dico.values():
        if i==True :
            string_descript+=str(t)
            i=False
        else :
            string_descript+= " "+ str(t)



    print(len(dico))
    list=[]
    list.append(string_descript)

    #calcul de poids de mots
    vectorizer = TfidfVectorizer(max_features=nb_saisi)
    vectors = vectorizer.fit_transform(list,y=146)
    feature_names = vectorizer.get_feature_names()
    dense = vectors.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)

    list_test = []


    #traitement necessaire pour eviter que les mots trop grands n'apparaissent pas quand on choisit un nombre de mots trop petit
    for i in range (0,len(feature_names)) :
        if (nb_saisi==1):
            list_test.append({'word': feature_names[i] , 'size': 150*denselist[0][i]})
        elif nb_saisi<=10:
            list_test.append({'word': feature_names[i] , 'size': 200*denselist[0][i]})
        else:
            list_test.append({'word': feature_names[i] , 'size': 300*denselist[0][i]})

    #creation du WordCloud
    template = env.get_template('wordcloud.html')
    output = template.render(dico=list_test,perso=perso).encode("utf-8")



    return output

#route permettant la visualisation de notre wordcloud
@app.route('/accueil_wordcloud')
def accueil_wordcloud():
    return render_template('accueil_wordcloud.html')

#route permettant la generation des donnees du graphique chronologique
@app.route('/json_final_graph')
def fjson():
    #wael_path = 'C:/Users/waelb/Documents/GitHub/VizuFinal/Final_version/static/graphJson/final_graph.json'
    #with open(wael_path) as json_data:
    with open('static/graphJson/final_graph.json') as json_data:
        data= json.load(json_data)
    return jsonify(data)

#route permettant d'acceder a la description de notre graphique chronologique
@app.route('/accueil_final_graph')
def accueil_final_graph():
    return render_template('accueil_final_graph.html')

#route permettant la visualisation de notre graphique chronologique
@app.route('/final_graph')
def final_graph():
    return render_template('final_graph.html')

if __name__ == '__main__':
	app.run(debug=True)
