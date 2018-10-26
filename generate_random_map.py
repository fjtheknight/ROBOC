def generate_map(x,y):
    """fonction pour générer des cartes aléatoires: non documentée"""
    from random import randrange #fonction de génération de nombres aléatoires
    porte='U'
    robot='X'
    espace=' '
    mur='O'
    dic=dict()#dictionnaire ou on va sauvegarder les coordonnées des éléments de la carte
    list1=[] #liste des coordonnées générées selon la longeur et la largeur de la carte
    list2=[] #liste des coordonnées générées lors de la recherche de la sortie
    listlat=[] #liste contenant les murs latéraux

    for i in range(x):
        for j in range (y):
            list1.append((i,j)) #si x==2 et y==2, list1 contiendra (0,0),(0,1),(1,0) et (1,1)

#génération des murs latéraux de la carte et sauvegarde dans listlat
    for i in range(x):
        listlat.append((i,0))
        listlat.append((i,y-1))
    for i in range(y):
        listlat.append((0,i))
        listlat.append((x-1,i))

    def randxy(x,y): #fonction pour générer les coordonnées de la porte de sortie
        randx = 0
        randy = 0
        rand_side=randrange(4)
        if rand_side == 0:
            randx = 0
            randy = randrange(1,y-1)
        elif rand_side == 1:
            randx = x-1
            randy = randrange(1,y-1)
        elif rand_side == 2:
            randx = randrange(1,x-1)
            randy = 0
        elif rand_side == 3:
            randx = randrange(1,x-1)
            randy = y-1
        return (randx,randy)

    position_porte=randxy(x,y) #génération des coordonnées de la porte de sortie


# ce morceau de code et pour être sur que le robot se trouve toujours du côté opposé à la porte de sortie donc si les dimensions sont 10 sur 10 et la position_porte==(0,6) alors on est sur que le robot sera dans l'intervalle (5->9,0->5)
    xr=0
    yr=0
    position_robot=()#coordonnées robot

    if position_porte[0] in range (x//2):
        xr = randrange(x//2,x-1+x%2)
    elif position_porte[0] in range (x//2,x):
        xr = randrange(1,x//2)
    if position_porte[1] in range (y//2):
        yr = randrange(y//2,y-1+y%2)
    elif position_porte[1] in range (y//2,y):
        yr = randrange(1,y//2)
    position_robot=(xr,yr)
#------------------------------------

#donc on a maintenant la position de la porte de sortie et du robot ainsi que les dimensions de la carte. On va maintenant chercher le chemin que doit prendre le robot pour atteindre la sortie

#pour cela, le robot doit atteindre la case juste devant la porte de sortie (si coordonnées sortie == (0,9), alors le robot doit atteinde (1,9) pour pouvoir sortir)
    list_port=()
    if position_porte[0]==0:
        list_port=(1,position_porte[1])
    if position_porte[0]==x-1 :
        list_port=(x-2,position_porte[1])
    if position_porte[1]==0:
        list_port=(position_porte[0],1)
    if position_porte[1]==y-1:
        list_port=(position_porte[0],y-2)

#on va maintenant déplacer le robot d'un pas dans une direction aléatoire, jusqu'à ce qu'il atteint la case qu'on a cherché (si position_robot==(3,8) par exemple, il doit se déplacer vers (1,9) pour sortir, donc il passe par (2,8) puis par (1,8) puis par (1,9) dans le meilleur des cas)
    def lol():
        listlol=[(-1,0),(0,1),(1,0),(0,-1)]
        return listlol[randrange(4)]

    randpos2= position_robot

    while randpos2 != list_port: #tant que le robot n'a pas atteint la position voulue
        loli=lol()#générer un pas aléatoire
        while (loli[0]+randpos2[0],loli[1]+randpos2[1]) in listlat or loli[0]+randpos2[0] == 0 or loli[0]+randpos2[0] == x-1 or loli[1]+randpos2[1] == 0 or loli[1]+randpos2[1] == y-1 :#si ce pas mene vers un obstacle
            loli=lol() #on génère un autre pas aléatoire et on compare de nouveau
        randpos2 = (loli[0]+randpos2[0],loli[1]+randpos2[1])#sinon on avance par un pas
        if randpos2 not in list2:
            list2.append(randpos2)# et on sauvegarde les coordées des mouvements qu'on a fait

#on va maintenant sauvegarder les coordonnées de tous les éléments dans un dictionnaire:
    for i in listlat:#mur latéral
        dic[i]=mur
    for i in list2:#espace = pas effectués pour atteindre la sortie = chemain passable
        dic[i]=espace
    dic[position_porte]=porte#porte de sortie
    dic[position_robot]=robot#robot

    for i in list1:#maitenant, on va générer les murs de l'interieur à partir des coordonnées pour lesquelles on n'a pas fourni de valeur=symbole=mur latéral,robot,sortie ou espace
        if i not in dic:
            dic[i]=mur

    return(dic) #et enfin on renvoie le dictionnaire
