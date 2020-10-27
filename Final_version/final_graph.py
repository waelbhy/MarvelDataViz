import re
import requests
import json
import requests
import sys
import nltk
import string
import pandas as pd










def create_list_comic(id):

    year_list =[]


    #recuperation du resultat de la requete sur les comics d'un personage defini par id
    query_total = requests.get('https://gateway.marvel.com:443/v1/public/characters/'+ str(id) +'/comics?limit=100&apikey=0de024649f971af7cbb0729ac0bb16a1', headers={'referer': 'localhost'})

    print("Code de retour=>",query_total.status_code)

    if query_total.status_code == 200:
             data_reply = query_total.json()
             total = data_reply["data"]["total"]
             print('total=',str(total))
    else:
             print("Erreur de telechargement")


    #on joue sur le offset pour prendre tous les resultats
    for i in range (0,total+100,100):
        query_list= requests.get('https://gateway.marvel.com:443/v1/public/characters/' + str(id) + '/comics?limit=100&offset=' + str(i) + '&apikey=0de024649f971af7cbb0729ac0bb16a1', headers={'referer': 'localhost'})
        print("Code de retour=>",query_list.status_code)
        unwanted_word=['MDCU']
        #remplissage de notre liste d'annees
        if query_list.status_code == 200:
                 data_reply= query_list.json()
                 for data in data_reply["data"]["results"]:
                     s=re.findall(r'\(([^()]+)\)', data["title"])

                     if(data["title"] is not None and s!=[] and len(s[0])==4 and s[0] not in unwanted_word):
                         year_list.append(int(s[0]))


        else:
                 print("Erreur de telechargement étape descript")

    return year_list



#retourne l'ensemble des annees avec le cumul du nombre de comics a chaque annee
def count_per_year(liste):

    #variable qui contiendra le cumul de comics au fil des annees
    cumul=0
    #tri par ordre croissant de nos annees
    liste=sorted(liste)
    tab_comic=[]
    #on demarre notre animation a partir de l'annee 1920
    tab_comic.append([1920,0])
    tab_year=[]
    #pour chaque annee dans la liste
    for valeur in liste:
        tab_temp=[]
        if(valeur not in tab_year):
            #augmentation du cumul
            cumul += liste.count(valeur)
            #ajout de l'annee dans le tableau d'annees
            tab_year.append(valeur)
            tab_temp.append(valeur)
            #ajout du cumul pour cet annee
            tab_temp.append(cumul)
            #retour de notre structure finale
            tab_comic.append(tab_temp)

    return(tab_comic)




#SERIES
def create_list_series(id):

    year_list_serie=[]

    #recuperation du resultat de la requete
    query_total = requests.get('https://gateway.marvel.com:443/v1/public/characters/' + str(id) + '/series?apikey=4dff50d15e38e094affa81c7191ac0bd', headers={'referer': 'localhost'})

    print("Code de retour=>",query_total.status_code)

    #informations sur la requete
    if query_total.status_code == 200:
             data_reply = query_total.json()
             total = data_reply["data"]["total"]
             print('total=',str(total))
    else:
             print("Erreur de telechargement")

    #recuperation de toutes les annees de sorties de series en jouant sur l'offset
    for i in range (0,total+100,100):
        query_list= requests.get('https://gateway.marvel.com:443/v1/public/characters/' + str(id) +'/series?offset=' + str(i) + '&apikey=4dff50d15e38e094affa81c7191ac0bd', headers={'referer': 'localhost'})
        print("Code de retour=>",query_list.status_code)
        #print(i)
        if query_list.status_code == 200:
                 data_reply_series= query_list.json()
                 for annee in data_reply_series["data"]["results"]:
                        year_list_serie.append(int(annee["startYear"]))




        else:
                 print("Erreur de telechargement étape descript")

    return year_list_serie




#permet de creer un dictionaire d'un perso identifie par id, de nom nom_perso, dans l'univers monde, et de le stocker dans nom_fichier
def create_dico(id,nom_perso,monde,nom_fichier):
    #creation de la liste contenant les annees de parution des comics
    liste_comic=create_list_comic(id)
    #comptage cumulé de comics du personage au fil des annees
    tab_comic = count_per_year(liste_comic)
    print("comics OK")
    #creation de la liste contenant les annees de parution des series
    liste_series=create_list_series(id)
    #comptage cumulé des series du personage au fil des annees
    tab_series=count_per_year(liste_series)
    print("series OK")
    min_year=min(tab_series[0][0], tab_comic[0][0])
    tab_population = [[min_year,3*10**7]]

    #construction du dictionaire
    dico={"name": str(nom_perso),"region": str(monde), "income": tab_comic, "population": tab_population, "lifeExpectancy" : tab_series}

   
    #enregistrement dans un fhichier pour eviter les temps d'execution trop longs
    with open('static/graphJson/' + nom_fichier + '.json', 'w') as outfile:
        json.dump(dico, outfile)


    return dico


#GENERATION DE NOS DONNEES
#spiderMan=create_dico(1009610,"Spider-Man","Avengers","SM")
#tab_global = []
#tab_global.append(spiderMan)
#DoctorStrange=create_dico(1009282,"Doctor Strange","Avengers","DrStrange")
#tab_global.append(DoctorStrange)
#wolverine=create_dico(1009718,"Wolverine","X-Men","Wolverine")
#tab_global.append(wolverine)
#magneto=create_dico(1009417,"Magneto","X-Men","Magneto")
#tab_global.append(magneto)
#thanos=create_dico(1009652,"Thanos","Avengers","Thanos")
#tab_global.append(thanos)
#hulk=create_dico(1009351,"Hulk","Avengers","Hulk")
#tab_global.append(hulk)
#daredevil=create_dico(1009262,"Daredevil","Marvel","Daredevil")
#tab_global.append(daredevil)
#BP=create_dico(1009187,"Black Panther","4-Fantastic","BlackPanther")
#tab_global.append(BP)
#JJ=create_dico(1009378,"Jessica Jones","Marvel","JessicaJones")
#tab_global.append(JJ)
#IR=create_dico(1009368,"Iron Man","Avengers","IronMan")
#tab_global.append(IR)
#CM=create_dico(1010338,"Captain Marvel","Avengers","CaptainM")
#tab_global.append(CM)
#cyclopes=create_dico(1009257,"Cyclopes","X-Men","Cyclopes")
#tab_global.append(cyclopes)
#cyclopes=create_dico(1009257,"Cyclopes","X-Men","Cyclopes")
#tab_global.append(cyclopes)
#gambit=create_dico(1009313,"Gambit","X-Men","Gambit")
#tab_global.append(gambit)
#jg=create_dico(1009496,"Jean Grey","X-Men","JeanGrey")
#tab_global.append(jg)
#beast=create_dico(1009175,"Beast","X-Men","Beast")
#tab_global.append(beast)
#thing=create_dico(1009662,"The Thing","4-Fantastic","Thing")
#tab_global.append(thing)
# Fantastic=create_dico(1009459,"Mr. Fanstastic","4-Fantastic","MrFantastic")
# tab_global.append(Fantastic)
# invisible=create_dico(1009366,"Invisible Woman","4-Fantastic","InvisibleW")
# tab_global.append(invisible)
#torch=create_dico(1009356,"Human Torch","4-Fantastic","Torch")
#tab_global.append(torch)
#print(tab_global)
#CA=create_dico(1009220,"Captain America","Avengers","CaptainA")
#tab_global.append(CA)
#print(tab_global)

# with open('static/graphJson/final_graph.json', 'w') as outfile:
#     json.dump(tab_global, outfile)
