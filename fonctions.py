import sys


"""*************************"""

def lire_deplacement():
    """fonction pour lire la commande de l'utilisateur et déterminer entre autres les pas du robot"""
    coeff = 1
    condition = False
    while condition ==  False:
        direction = input("Donnez vos ordres!: ") #j'étais incapable de vérifier cet input pour des chaines de plus de 2 charactaires
        if len(direction)==1 and direction in ["o","e","s","n","q"]:
            condition = True
            di = direction[0]
        elif len(direction)==2 and direction[0] in ["o","e","s","n"] and direction[1] in("1234567890"):
            di = direction[0]
            rection = direction[1]
            condition=True
            coeff=int(rection)
        else:
            print("Veuillez saisir une commande valide! ")
    translation = (0,0)
    if di == 'n': # calculer les pas à effectuer selon la direction
        translation = (-1*coeff,0)
    elif di == 's':
        translation = (1*coeff,0)
    elif di == 'e':
        translation = (0,1*coeff)
    elif di == 'o':
        translation = (0,-1*coeff)
    elif di == 'q':
        translation = "q"
    return translation

def quitter_enregistrer(lab):
    """fonction pour appeler la fonction d'enregistrement de cartes dans des fichiers txt"""
    lab.enregistrer_carte()
    print("Votre partie a été enregistrée!")
    print("Vous avez quitté la partie.")
    sys.exit()


def deplacer(dic,position,direction):
    """fonction pour déterminer la position du robot après commande de l'utilisateur"""
    pas = []
    peut_passer=True
    for a in range(direction[0]+1): #pour déterminer s'il n'y a pas d'obstacle entre la position actuelle et la position envisagée
        for b in range(direction[1]+1):
            pas.append((position[0]+a,position[1]+b))
    position_futur = (position[0]+direction[0],position[1]+direction[1])
    for i in pas:
        if i in dic.keys() and dic[i]=="O":
            peut_passer=False
    if position_futur in dic.keys() and dic[position_futur] != "O" and peut_passer:
        return position_futur
    else:
        print("Déplacement impossible!")
        return position

def liste_carte():
    """fonction pour déterminer les cartes sous forme de fichiers txt"""
    import glob
    liste=glob.glob("cartes/*.txt")
    for p,elm in enumerate(liste):
        x=elm.rfind("\\")
        liste[p]=elm[x+1:-4] #pour ne garder que le nom de la carte
    return (liste)


def intro():
    """fonction pour charger un texte d'introduction à partir d'un fichier txt"""
    with open("intro.txt","r") as f:
        print( f.read())


def demarrer(lab):
    """fonction à éxécuter lors du démarrage"""
    intro()
    liste = liste_carte()
    en_cours="en_cours" #nom de la carte sauvegardée de la dernière fois = partie en cours
    if en_cours in liste: #s'il existe une telle carte
        del liste[0]
        condition = False
        while condition ==  False:
            reponse = input("Vous avez une partie en cours. Voulez-vous la charger? (O/N): ")#demander s'il faut la charger
            if reponse in ["o","O","n","N"]:
                condition = True
                if reponse in ["o","O"]:
                    print("Chargement en cours...")
                    lab.fichier = en_cours+".txt"
                    return

            else:
                print("Veuillez saisir une commande valide! ")

    print("Veuillez choisir une carte: ") #sinon charger les cartes usuelles de jeu
    print("'r' => Carte générée aléatoirement")
    liste2 = []
    for p,elm in enumerate(liste):
        liste2.append(str(p))
        print("'{}' => Carte '{}'".format(p,elm))#print les cartes disponibles dans le dossier cartes
    condition = False
    condition2 = False
    while condition ==  False:
        reponse = (input(""))
        if reponse in liste2 or reponse == 'r':
            condition = True
            if reponse == 'r':
                while condition2 ==  False:
                    reponse2 = (input("Choisir longeur de la carte (10->80): "))
                    reponse3 = (input("Choisir largeur de la carte (10->80): "))
                    if reponse2.isnumeric() and  reponse3.isnumeric() and int(reponse2) in range(10,81) and int(reponse3) in range(10,81):
                        condition2 = True
                    else:
                        print("Veuillez choisir des valeurs valides! ")
                print("Génération de carte aléatoire en cours ...")
                from generate_random_map import generate_map
                lab.dic =  generate_map(int(reponse2),int(reponse3))
                lab.generer_carte()
                lab.enregistrer_carte()

                return
            lab.fichier =  liste[int(reponse)]+".txt"
            lab.charger()

            return
        else:
            print("Veuillez choisir une carte valide! ")


def jouer (c,c2,rob):
    """fonction à exécuter après chaque mouvement"""
    x=lire_deplacement() # lire la commande ed l'utilisateur
    rob.position_x(c.dic)
    z = rob.position #déterminer la posisition du robot
    if x != "q": #si la commande est différente de 'q'=quitter
        cond = deplacer(c.dic,z,x) # vérifier si le robot peut se déplacer vers la postion voulue
    else:
        quitter_enregistrer(c) # sinon enregistrer et quitter
    if cond != z: # si les coordonnées du robot peuvent changer
        c.dic[cond]="X" #changer les coordonnées du robot
        c.dic[z]=c2.dic[z] #remplacer la valeur ('X') des coordonnées anciennes du robot par l'élément d'origine (importé de la copie du dictionnaire de carte vierge)
    c.generer_carte()
    print(c.texte) #générer la carte et la renvoyer
    if c2.dic[cond] == "U": #si le robot atteint la porte
        gagner(c,c2,rob) #afficher le message de victoire



def gagner(c,c2,rob):
    """fonction pour afficher un message lorsque le joueur gagne"""
    with open("outro.txt","r") as f:
        print( f.read())
    fonction_principale(c,c2,rob)

"""---------------------------
-------------------------------
-------------------------------
--------------------------------"""
def fonction_principale(lab,copie_lab,rob):
    """fonction principale"""
    demarrer(lab) #démarrager le jeu et charger la carte
    lab.decouper_carte()  #enregistrer les coordonnées de chaque élément de la carte dans un premier dictionnaire
    copie_lab.dic=lab.dic.copy() #enregistrer les coordonnées de chaque élément de la carte dans un deuxième dictionnaire = celui qui sera utilisé pour générer la carte
    rob.position_x(copie_lab.dic) #enregistrer les coordonnées du robot X
    z=rob.position
    copie_lab.dic[z]=" " #et le remplacer par " " => carte vierge sans robot
    lab.generer_carte()#génération et renvoi de la carte
    print(lab.texte)
    while  True:
        jouer(lab,copie_lab,rob)#jouer tant qu'on le veut
        #print("latexé",lab.texte)
    quitter_enregistrer(lab.texte)#sinon enregistrer et quitter
