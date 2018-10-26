class Joueur:
    def __init__(self):
        self.position = ()

    def position_x(self,dic):
        """fonction pour déterminer les coordonnées du robot à partir d'un dictionnaire"""
        for i,u in dic.items():
            if u == "X":
                self.position = i

"""*************************"""
class Carte:
    def __init__(self):
        self.fichier = "en_cours.txt"
        self.texte = ""
        self.dic = {}

    def charger(self):
        """fonction pour charger les cartes à partir des fichiers txt"""
        with open("cartes/"+self.fichier,"r") as f:
            self.texte = f.read()

    def enregistrer_carte(self):
        """fonction pour enregistrer les cartes dans des fichiers txt"""
        self.fichier = "en_cours.txt"
        with open("cartes/"+self.fichier,"w") as f:
            f.write(self.texte)

    def generer_carte(self):
        """fonction pour générer des cartes (chaine de charactaires) à partir de dictionnaires"""
        self.texte=""
        liste=self.dic.keys()
        list_max=list(map(max,zip(*liste))) #déterminer le nombre de ligne et de colonne à partir des clés du dictionnaire (tuples)
        for i in range(list_max[0]+1):
            for j in range(list_max[1]+1):
                elm = self.dic[(i,j)] #
                self.texte += elm #générer la carte sous forme de chaine de charactaires
            self.texte += "\n"


    def decouper_carte(self):
        """fonction pour générer un dictionnaire contenant les coordonées de chaque élément de la carte"""
        dic = {}
        with open("cartes/"+self.fichier,"r") as f:
            for i, l in enumerate(f):
                for j in range(len(l)):
                    if l[j] in {"O","X"," ","U","."}: #pour éviter les retours en ligne je pense
                        dic[(i,j)]=l[j] #sauvegarder les coordonnés (key) de chaque élémént(value) dans un dictionnaire exemple : (2,5):'O'
            self.dic = dic
