#import re
import entity as en
import utils as ut
import numpy as np
import spacy
from spacy.lang.en.stop_words import STOP_WORDS


#nlp = spacy.load("en_core_web_sm")


nlp = spacy.load("en_core_web_sm", exclude = ["attribute_ruler" , \
                                                "tok2vec","parser","senter","ner"])


#nlp = spacy.load("fr_dep_news_trf")

# Retourne la similarité consine entre le vect_a et vect_b
def cosine_similarity(vect_a, vect_b):
    return np.dot(vect_a, vect_b) / (np.linalg.norm(vect_a)*np.linalg.norm(vect_b))

"""----------------------------------------------------------------------------------------------------------------
                                            CODE PRINCIPAL
------------------------------------------------------------------------------------------------------------- """

liste_de_documents_et_caracteristiques = open("CISI\CISI.ALL" , "r" , encoding="utf-8")

point = "."
grandI = "I"
grandT = "T"
grandA = "A"
grandW = "W"

documents_list = []
 
## Parcours du fichier

while True :
    line = liste_de_documents_et_caracteristiques.readline()
    if not line :
        break

    if line[0] == point:
        ## ON VERIFIE SI ON A UN GRAND I
        if line[1] == grandI :
            identifiant = line[3:].strip()
            print(identifiant)
            document = en.Document(identifiant)
            documents_list.append(document)
        
        elif line[1] == grandT :
            titre = ut.read_paragraph(liste_de_documents_et_caracteristiques)
            document.titre = titre
        
        elif line[1] == grandA :
            auteur = ut.read_paragraph(liste_de_documents_et_caracteristiques)
            document.auteur = auteur

        elif line[1] == grandW :
            resume = ut.read_paragraph(liste_de_documents_et_caracteristiques)
            document.resume = resume
    


##CONSTRUCTION DU VOCABULAIRE ET CELUI DES DOCUMENTS

vocab = []
for doc in documents_list :
    if (documents_list.index(doc) < len(documents_list)) :
        # ON TROUVE LES MOTS DE CE DOCUMENT
        vocab_doc , vocab = ut.vocabular_of_a_document("resume", doc , vocab, nlp)
        doc.vocab_resume = vocab_doc
        print(len(doc.vocab_resume), " :  " , documents_list.index(doc))
    else :
        break

print(" \n \n " , len(vocab))
#print(vocab)


vocab_size = len(vocab)
word_docs_frequency = np.zeros(vocab_size)
for doc in documents_list :
    if (documents_list.index(doc) < len(documents_list)) :
        doc.representative_vector_resume = np.zeros(vocab_size)
        for word in doc.vocab_resume :
            doc.representative_vector_resume[vocab.index(word)] = doc.vocab_resume[word]
            #nombre dapparitions du mot dans le document
            word_docs_frequency[vocab.index(word)] += 1
    else :
        break

print ("\n \n \n")
print("\n \n \n")
#print(word_docs_frequency.shape)
print ("\n \n \n")
print("\n \n \n")





##FONCTION DE LECTURE DU CONTENU DE FICHIER DES REQUETES

fichier_requetes = open("CISI\CISI.QRY" , "r" , encoding="utf-8")

requete_list = []
 
## Parcours du fichier des requêtes
while True :
    line = fichier_requetes.readline()

    if not line :
        break
    if line[0] == point:

        ## Lecture de l'identifiant
        if line[1] == grandI :
            identifiant = line[3:].strip()
            requete = en.Requete(identifiant)
            requete_list.append(requete)

        ## Lecture du contenu
        elif line[1] == grandW :
            requete.contenu = ut.read_paragraph(fichier_requetes)


"""for requete in requete_list:
     print ( f"{requete.identifiant} : {requete.contenu})"""

requete_vectors = {}
j=0
for req in requete_list:
    vocab_requete = ut.vocabular_of_a_request("contenu", req, {},nlp)
    vector_req = np.zeros(vocab_size)
    i = 0
    for word in vocab_requete :
        # Si le mot de la requête est présent dans le vocab
        if word in vocab :
            vector_req[vocab.index(word)] = vocab_requete[word]

        # Sinon : à faire plus tard
        else :
            i+=1
    
    requete_vectors[req.identifiant] = vector_req

## RECHERCHE 
req_vector = requete_vectors['1']
results = {}
#print(f"\n \n \n {[i for i in req_vector if i != 0]}")
"""for doc_id in len(documents_list):
    #print(doc_vector_key)
    results[doc_id] = cosine_similarity(req_vector, documents_index[doc_id])"""

for doc in documents_list :
    #if documents_list.index(doc) < 20 :
    results[documents_list.index(doc)] = cosine_similarity (req_vector , doc.representative_vector_resume)    
    ##else :
        #break

print(results)

# trier par ordre décroissant
sorted_results = dict(sorted(results.items(), key=lambda item: item[1], reverse = True))
#print(list(sorted_results.keys())[1:10])

for doc_id in list(sorted_results.keys())[1:10] :
    print(documents_list[doc_id].titre)
    print(print(documents_list[doc_id].resume))
    print("\n \n \n")

    """for document in documents_list:
        if document.identifiant == doc_id :
            print(document.titre)
            print("\n")
            print(document.resume)
            print("\n \n \n")
            break"""

#print(sorted_results)
#print(vocab)
#print(len(vocab))"""
