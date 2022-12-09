

"""
    THIS FILE CONTAINS A LIST OF 
    USEFUL FUNCTIONS FOR OUR PROGRAM
"""

##THIS FUNCTION READS A PARAGRAPH
def read_paragraph(file) :
    paragraph = ""
    last_pos = file.tell()
    while True:
        ## On sauvegarde la position sur le fichier avant de lire la ligne suivante
        last_pos = file.tell()
        line = file.readline()
        if line[0] == ".":
            ## Si on a atteind le champ suivant on revient a la ligne precedente
            file = file.seek(last_pos)
            break
        paragraph += line.strip()

    return paragraph




# Afficher chaque document contenu dans la liste documents (liste d objets de la classe Document)
def print_all_docs(documents):
    for doc in documents:
        print("id:"+doc.identifiant)
        print("titre:"+doc.titre)
        print("auteur:"+doc.auteur)
        print("resume:"+doc.resume)


"""## Renvoie une liste des mots contenus dans une string, separes par un espace ou un caractere special
def get_words_from_string(input_string):
    word_list=re.split(" |:|,|\.|\?|!|\(|\)|\"|-",input_string);    
    return word_list"""

def get_words_from_string(input_string , nlp):
    #WE TRANSFORM THE INPUT STRING IN DOC SPACY
    new_input_string = nlp(input_string)
    
    #WE RETURN THE LEMMAS OF ALL THE WORDS AND ONLY IF THE WORD ISN'T A STOP
    return [i.lemma_.lower() for i in  new_input_string if i.is_stop == False]


def vocabular_of_a_document(element, doc , total_vocab, nlp) :
    vocab_doc = {}
    for word in get_words_from_string(getattr(doc , element),nlp) :
        if word in vocab_doc :
            vocab_doc[word] += 1
        else :
            vocab_doc[word] = 1

        ##ON VERIFIE SI LE MOT EXISTE DANS LE TOTAL VOCAB
        if word not in total_vocab :
            total_vocab.append(word)

    return vocab_doc , total_vocab
        


"""#cette fonction construit un vocab pour un document
def vocabular_of_the_document(element, doc, vocab, nlp, is_principal_vocab = False) :
    
    position = 0
    for word in get_words_from_string(getattr(doc, element),nlp):
        if word in vocab :
            if is_principal_vocab == False :
                vocab[word] = vocab[word]+1
        else:
            if is_principal_vocab :
                vocab[word] = position
                position += 1
            else :
                vocab[word] = 1
                #SI LE MOT EST PAS DANS VOCAB
                #ET ON EST PAS EN PRINCIPAL VOCAB
                #ON CREE A 1 LE NBRE DE DOCUMENTS OU IL APPARAIT

                #SI LE MOT EST DANS VOCAB
                #ET EST DEJA APPRARU : pas de +1
                #SI OUI , UN PLUS +1
    
    return vocab"""




"""#cette fonction construit un vocabulaire en fonction de l'élement constitutif d'une document (titre , resume...)
#Creation du vocabulaire : enregistrement de tous les mots differents dans le dictionnaire vocab avec leur nombre d occurences
def vocabular_of_the_element(element, documents_list, vocab) :
    
    for doc in documents_list:
        vocab = vocabular_of_the_document(element, doc, vocab ,True)
    return vocab"""


def vocabular_of_a_request(element, doc, vocab, nlp) :
    for word in get_words_from_string(getattr(doc , element),nlp) :
        if word in vocab :
            vocab[word] += 1
        else :
            vocab[word] = 1

    return vocab