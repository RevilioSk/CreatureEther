from tempfile import tempdir
import Creature
import pygame
import random
import os
script_dir = os.path.dirname(__file__)
image_dir = os.path.join(script_dir, 'Images')
musique_dir = os.path.join(script_dir, 'Musiques')
font_dir = os.path.join(script_dir, 'Fonts')
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption('Créature Éther')

my_font = pygame.font.Font(os.path.join(font_dir,'PokemonGb-RAeo.ttf'), 20)

#Chargement des images
imageBackground = pygame.image.load(os.path.join(image_dir,'bg.png'))
imageBackground = pygame.transform.scale(imageBackground,(1280,720))

imageBackgroundTitre = pygame.image.load(os.path.join(image_dir,'bgTitre.png'))
imageBackgroundTitre = pygame.transform.scale(imageBackgroundTitre,(1280,720))

imBouclier = pygame.image.load(os.path.join(image_dir,'Bouclier.png'))
imBouclier = pygame.transform.scale(imBouclier,(350,300))

imDegat = pygame.image.load(os.path.join(image_dir,'Hit.png'))
imDegat = pygame.transform.scale(imDegat,(50,50))

imTitre = pygame.image.load(os.path.join(image_dir,'Titre.png'))
#imTitre = pygame.transform.scale(imTitre,(150,150))

imDegatCrit = pygame.image.load(os.path.join(image_dir,'HitCrit.png'))
imDegatCrit = pygame.transform.scale(imDegatCrit,(50,50))

imAuraRouge = pygame.image.load(os.path.join(image_dir,'auraRouge.png'))
imAuraRouge = pygame.transform.scale(imAuraRouge,(460,400))
imAuraOrange = pygame.image.load(os.path.join(image_dir,'auraOrange.png'))
imAuraOrange = pygame.transform.scale(imAuraOrange,(460,400))
imAuraViolette = pygame.image.load(os.path.join(image_dir,'auraViolette.png'))
imAuraViolette = pygame.transform.scale(imAuraViolette,(460,400))

    


running = True
dt = 0
tourfini = True






    
    # def draw(self):
    #      screen.blit(self.image, self.rect)

class HealthBar():
	def __init__(self, x, y, pv, pv_max):
		self.x = x
		self.y = y
		self.pv = pv
		self.pv_max = pv_max

	def draw(self, pv):
		#update with new health
		self.pv = pv
		#calculate health ratio
		ratio = self.pv / self.pv_max   
		pygame.draw.rect(screen, "black", (self.x-2, self.y-2, 204, 24))
		pygame.draw.rect(screen, "green", (self.x, self.y, 200 * ratio, 20))


class ShieldBar():
	def __init__(self, x, y, shield, shield_max):
		self.x = x
		self.y = y
		self.shield = shield
		self.shield_max = shield_max

	def draw(self, shield):
		#update with new health
		self.shield = shield
		#calculate health ratio
		ratio = self.shield / self.shield_max   
		pygame.draw.rect(screen, "black", (self.x-2, self.y, 24, 204))
		pygame.draw.rect(screen, "blue", (self.x, (self.y+200*(1-ratio))+2, 20, 200*ratio))


StarterNumero = 2





PokemonActifIA = Creature.SbirePlante1.copy()


pokeB_health_bar = HealthBar(971,370,PokemonActifIA.pv,PokemonActifIA.pvmax)



#Temps des cooldowns du joueur
timeCdC1=0
timeCdC2=0
timeCdC3=0

#Temps des cooldowns de l'IA
timeCdbot=0


#Valeur des cooldowns de l'IA en ms
Cdbot=(random.randint(3,6)*1000)-(PokemonActifIA.vitesse)

#Bools pour les capacités (Prête ou non)
C1Prete = False
C2Prete = False
C3Prete = False

#Bool pour la parade
Parade = False

#Bools pour l'aura de l'attaque du bot
prepaAtt1 = False
prepaAtt2 = False
prepaAtt3 = False

#Variables diverses
CompteurMort = 0

#Numéro de l'attaque du bot
NumAttBot = 1

#Variables pour l'affichage
AffichageAide = True
ecran = "Écran Titre"

#Gestion de la musique
pygame.mixer.music.load(os.path.join(musique_dir,"The Adventure Begins.mp3"))
pygame.mixer.music.play(loops=0)
pygame.mixer.music.set_volume(0.7)


#On créer les textes

cooldownC1Texte = my_font.render("A",True,(0, 0, 0))
cooldownC2Texte = my_font.render("Z",True,(0, 0, 0))
cooldownC3Texte = my_font.render("E",True,(0, 0, 0))



PokemonActifIA.imagetype1 = pygame.transform.scale(PokemonActifIA.imagetype1,(100,20))
PokemonActifIA.imagetype2 = pygame.transform.scale(PokemonActifIA.imagetype2,(100,20))

commencerLaPartie = my_font.render("Pour commencer appuyez sur 'Espace' ", True,(0, 255, 255))
bestiaire = my_font.render("Pour accéder aux commandes appuyez sur 'C' ", True,(255, 255, 0))
selectionStarter = my_font.render("Séléctionez votre starter avec les flèches directionnelles", True,(200, 200, 125))

textCommandeFlecheGD1 = my_font.render("Flèches directionnelles gauche et droite : ", True,(0, 0, 0))
textCommandeFlecheGD2 = my_font.render("Changer le type/la capacité qui sera remplacé(e)", True,(0, 0, 0))
textCommandeFlecheHB1 = my_font.render("Flèches directionnelles haut et bas : ", True,(0, 0, 0))
textCommandeFlecheHB2 = my_font.render("Changer la sélection de la nouvelle capacité à apprendre", True,(0, 0, 0))
textCommandeA = my_font.render("A : Utiliser la capacité numéro 1", True,(0, 0, 0))
textCommandeZ = my_font.render("Z : Utiliser la capacité numéro 2", True,(0, 0, 0))
textCommandeE = my_font.render("E : Utiliser la capacité numéro 3", True,(0, 0, 0))
textCommandeQ = my_font.render("Q : Sélectionner l'objet/la capacité le/la plus à gauche", True,(0, 0, 0))
textCommandeS = my_font.render("S : Sélectionner l'objet/la capacité au centre", True,(0, 0, 0))
textCommandeD = my_font.render("D : Sélectionner l'objet/la capacité le/la plus à droite", True,(0, 0, 0))
textCommandeX = my_font.render("X : Continuer sans sélectionner de changement / Retour arrière", True,(0, 0, 0))
textCommandeEspace = my_font.render("Espace : Valider un changement", True,(0, 0, 0))

s1 = pygame.Surface((1140,40), pygame.SRCALPHA)
s1.fill((0,0,0,200))  

s2 = pygame.Surface((813,40), pygame.SRCALPHA)
s2.fill((0,0,0,200))  

s3 = pygame.Surface((674,40), pygame.SRCALPHA)
s3.fill((0,0,0,200))  

debutJeu = True
attaqueEnCours = False


#Tableau des Sbires et des Boss
tabcrea = {
    1: (Creature.SbirePlante1,Creature.SbirePlante2,Creature.BossPlante),
    2: (Creature.SbireFeu1,Creature.SbireFeu2,Creature.BossFeu),
    3: (Creature.SbireEau1,Creature.SbireEau2,Creature.BossEau),
    4: (Creature.SbireFee1,Creature.SbireFee2,Creature.BossFee),
    5: (Creature.SbireNormal1,Creature.SbireNormal2,Creature.BossNormal),
    6: (Creature.SbireVol1,Creature.SbireVol2,Creature.BossVol),
    7: (Creature.SbireSol1,Creature.SbireSol2,Creature.BossSol),
    8: (Creature.SbireInsecte1,Creature.SbireInsecte2,Creature.BossInsecte),
    9: (Creature.SbirePoison1,Creature.SbirePoison2,Creature.BossPoison),
    10: (Creature.SbireElectrik1,Creature.SbireElectrik2,Creature.BossElectrik),
    11: (Creature.SbireAcier1,Creature.SbireAcier2,Creature.BossAcier),
    12: (Creature.SbireRoche1,Creature.SbireRoche2,Creature.BossRoche),
    13: (Creature.SbireGlace1,Creature.SbireGlace2,Creature.BossGlace),
    14: (Creature.SbireSpectre1,Creature.SbireSpectre2,Creature.BossSpectre),
    15: (Creature.SbireDragon1,Creature.SbireDragon2,Creature.BossDragon),
    16: (Creature.SbirePsy1,Creature.SbirePsy2,Creature.BossPsy),
    17: (Creature.SbireTenebres1,Creature.SbireTenebres2,Creature.BossTenebres),
    18: (Creature.SbireCombat1,Creature.SbireCombat2,Creature.BossCombat),
}


tabobjetglobal = {
    1: Creature.BandeauAttaque.copy(),
    2: Creature.BandeauDefense.copy(),
    3: Creature.BandeauAttaqueSpe.copy(),
    4: Creature.BandeauDefenseSpe.copy(),
    5: Creature.BandeauVitesse.copy(),
    6: Creature.BandeauVie.copy(),
    7: Creature.BandeauCritique.copy(),
    8: Creature.BandeauDegatCrit.copy(),
    9: Creature.BandeauVoldeVie.copy(),
    10: Creature.MouchoirOffensif.copy(),
    11: Creature.MouchoirDefensif.copy(),
    12: Creature.MouchoirVitesse.copy(),
    13: Creature.MouchoirVie.copy(),
    14: Creature.MouchoirCritique.copy(),
    15: Creature.MouchoirDegatCrit.copy(),
    16: Creature.MouchoirVoldeVie.copy(),
    17: Creature.Stabilisateur.copy(),
    18: Creature.Cameleon.copy(),
    19: Creature.Equilibre.copy(),
    20: Creature.Critique.copy(),
    21: Creature.Vitalite.copy(),
    22: Creature.Efficacite.copy(),
    23: Creature.StatsPrimaires.copy(),
    24: Creature.StatsSecondes.copy(),
}

objetselection = {

}

nomObjetTexte = {

}

nomTypesTexte ={

}

typesselection = {

}

typeachanger = 1

capaciteaChanger = 1


StabilisateurActif = False
EfficaciteActif = False
selectionTypeCameleon = False



tabtypecameleon = {
    1: "Acier",
    2: "Combat",
    3: "Dragon",
    4: "Eau",
    5: "Électrik",
    6: "Fée",
    7: "Feu",
    8: "Glace",
    9: "Insecte",
    10: "Normal",
    11: "Plante",
    12: "Poison",
    13: "Psy",
    14: "Roche",
    15: "Sol",
    16: "Spectre",
    17: "Ténèbres",
    18: "Vol",
}



tabobjetjoueur = {
    1: "Vide",
    2: "Vide",
    3: "Vide",
    4: "Vide",
    5: "Vide",
    6: "Vide",
    7: "Vide",
    8: "Vide",
    9: "Vide",
    10: "Vide",
    11: "Vide",
    12: "Vide",
    13: "Vide",
    14: "Vide",
    15: "Vide",
    16: "Vide",
    17: "Vide",
    18: "Vide",
}

#Boucle principale
while running:

    if ecran=="Écran Titre":
        match StarterNumero:
            case 1: Starter = Creature.StarterVitesse.copy()
            case 2: Starter = Creature.StarterAttaque.copy()
            case 3: Starter = Creature.StarterDefense.copy()
        screen.blit(imageBackgroundTitre,(0,0))
        screen.blit(imTitre,(350,100))
        screen.blit(Starter.image,(500,200))
        screen.blit(s3,(296,490))
        screen.blit(commencerLaPartie,(300,500))
        screen.blit(s2,(266,590))
        screen.blit(bestiaire,(270,600))
        screen.blit(s1,(76,680))
        screen.blit(selectionStarter,(80,690))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if event.key==pygame.K_SPACE:
                    #Setup de la creature du joueur 
                    PokemonActifJoueur = Starter.copy()
                    pokeJ_health_bar = HealthBar(131,370,PokemonActifJoueur.pv,PokemonActifJoueur.pvmax)
                    pokeJ_shield_bar = ShieldBar(20,400,PokemonActifJoueur.bouclier,PokemonActifJoueur.boucliermax)
                    CdC1=50000/((PokemonActifJoueur.vitesse*PokemonActifJoueur.modifvit)/10)
                    CdC2=50000/((PokemonActifJoueur.vitesse*PokemonActifJoueur.modifvit)/10)
                    CdC3=50000/((PokemonActifJoueur.vitesse*PokemonActifJoueur.modifvit)/10)
                    PokemonActifJoueur.image = pygame.transform.flip(PokemonActifJoueur.image, 180,0)
                    attaque1texte = my_font.render("A : "+PokemonActifJoueur.c1.nom, True,(0, 0, 0))
                    attaque2texte = my_font.render("Z : "+PokemonActifJoueur.c2.nom, True,(0, 0, 0))
                    attaque3texte = my_font.render("E : "+PokemonActifJoueur.c3.nom, True,(0, 0, 0))
                    PokemonActifJoueur.imagetype1 = pygame.transform.scale(PokemonActifJoueur.imagetype1,(100,20))
                    PokemonActifJoueur.imagetype2 = pygame.transform.scale(PokemonActifJoueur.imagetype2,(100,20))
                    ecran="Écran Jeu" 
                
                if event.key==pygame.K_RIGHT:
                    StarterNumero+=1
                    if StarterNumero>3:StarterNumero=1

                if event.key==pygame.K_LEFT:
                    StarterNumero-=1
                    if StarterNumero<1:StarterNumero=3

                if event.key==pygame.K_c:
                    ecran = "Écran Commandes"
    
    elif ecran == "Écran Commandes": 
        screen.blit(imageBackground,(0,0))
        screen.blit(textCommandeFlecheGD1,(20,10))
        screen.blit(textCommandeFlecheGD2,(20,30))
        screen.blit(textCommandeFlecheHB1,(20,80))
        screen.blit(textCommandeFlecheHB2,(20,100))
        screen.blit(textCommandeA,(20,150))
        screen.blit(textCommandeZ,(20,200))
        screen.blit(textCommandeE,(20,250))
        screen.blit(textCommandeQ,(20,300))
        screen.blit(textCommandeS,(20,350))
        screen.blit(textCommandeD,(20,400))
        screen.blit(textCommandeX,(20,450))
        screen.blit(textCommandeEspace,(20,500))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_x:
                    ecran = "Écran Titre"

    elif ecran=="Écran Jeu":
        #Gestion de la musique
        if debutJeu:
            pygame.mixer.music.load(os.path.join(musique_dir,"Battle! Wild Pokémon.mp3"))
            pygame.mixer.music.play(loops=0)
            pygame.mixer.music.set_volume(0.5)
            PokemonActifJoueur.pv=PokemonActifJoueur.pvmax
            timeCdbot=0
            tempsApresEcranTitre = pygame.time.get_ticks()
            debutJeu = False
        #Etat vivant ou non des créatures
        if PokemonActifIA.pv<=0:
            intAnimMort = 100
            PokemonActifIA.vivant=False

            if CompteurMort % 10 == 0 and CompteurMort>1:
                selectionCapacite = True
                selectionItem = True
                capaselec1 = True
                match CompteurMort/10:
                    case 1 : 
                        capaciteaApprendre1 = Creature.phyPlante
                        capaciteaApprendre2 = Creature.spePlante
                    case 2 : 
                        capaciteaApprendre1 = Creature.phyFeu
                        capaciteaApprendre2 = Creature.speFeu
                    case 3 : 
                        capaciteaApprendre1 = Creature.phyEau
                        capaciteaApprendre2 = Creature.speEau
                    case 4 : 
                        capaciteaApprendre1 = Creature.phyFee
                        capaciteaApprendre2 = Creature.speFee
                    case 5 : 
                        capaciteaApprendre1 = Creature.phyNormal
                        capaciteaApprendre2 = Creature.speNormal
                    case 6 : 
                        capaciteaApprendre1 = Creature.phyVol
                        capaciteaApprendre2 = Creature.speVol
                    case 7 : 
                        capaciteaApprendre1 = Creature.phySol
                        capaciteaApprendre2 = Creature.speSol
                    case 8 : 
                        capaciteaApprendre1 = Creature.phyInsecte
                        capaciteaApprendre2 = Creature.speInsecte
                    case 9 : 
                        capaciteaApprendre1 = Creature.phyPoison
                        capaciteaApprendre2 = Creature.spePoison
                    case 10 : 
                        capaciteaApprendre1 = Creature.phyElectrik
                        capaciteaApprendre2 = Creature.speElectrik
                    case 11 : 
                        capaciteaApprendre1 = Creature.phyAcier
                        capaciteaApprendre2 = Creature.speAcier
                    case 12 : 
                        capaciteaApprendre1 = Creature.phyRoche
                        capaciteaApprendre2 = Creature.speRoche
                    case 13 : 
                        capaciteaApprendre1 = Creature.phyGlace
                        capaciteaApprendre2 = Creature.speGlace
                    case 14 : 
                        capaciteaApprendre1 = Creature.phySpectre
                        capaciteaApprendre2 = Creature.speSpectre
                    case 15 : 
                        capaciteaApprendre1 = Creature.phyDragon
                        capaciteaApprendre2 = Creature.speDragon
                    case 16 : 
                        capaciteaApprendre1 = Creature.phyPsy
                        capaciteaApprendre2 = Creature.spePsy
                    case 17 : 
                        capaciteaApprendre1 = Creature.phyTenebres
                        capaciteaApprendre2 = Creature.speTenebres
                    case 18 : 
                        capaciteaApprendre1 = Creature.phyCombat
                        capaciteaApprendre2 = Creature.speCombat

                while selectionCapacite:
                    screen.blit(imageBackground,(0,0))
                    tempsDeJeu = my_font.render(str(round((pygame.time.get_ticks()-tempsApresEcranTitre)/1000,1)), True,(0, 0, 0))
                    screen.blit(tempsDeJeu, (1190,5))
                    capaselection = my_font.render("La capacitée numéro "+str(capaciteaChanger)+" va changer",True,(0,0,0))
                    Cap1Texte = my_font.render(capaciteaApprendre1.nom,True,(0,0,0))
                    Cap2Texte = my_font.render(capaciteaApprendre2.nom,True,(0,0,0))
                    if capaselec1:
                        pygame.draw.rect(screen,(0,0,0),(400,280,20,20))
                    else: pygame.draw.rect(screen,(0,0,0),(400,350,20,20))
                    screen.blit(attaque1texte, (0,5))
                    screen.blit(attaque2texte, (0,35))
                    screen.blit(attaque3texte, (0,65))
                    screen.blit(Cap1Texte,(425,280))
                    screen.blit(Cap2Texte,(425,350))
                    screen.blit(capaselection,(300,480))

                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                            selectionCapacite = False
                            selectionItem = False
                        if event.type == pygame.KEYDOWN:
                            if event.key==pygame.K_x:
                                selectionCapacite = False
                            if event.key==pygame.K_RIGHT:
                                capaciteaChanger+=1
                                if capaciteaChanger>3: capaciteaChanger=1
                            if event.key==pygame.K_LEFT:
                                capaciteaChanger-=1
                                if capaciteaChanger<1: capaciteaChanger=3
                            if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                                if capaselec1:
                                    capaselec1 = False
                                else: capaselec1 = True
                            if event.key==pygame.K_SPACE:
                                selectionCapacite = False
                                if capaselec1:
                                    match capaciteaChanger:
                                        case 1: PokemonActifJoueur.c1 = capaciteaApprendre1
                                        case 2: PokemonActifJoueur.c2 = capaciteaApprendre1
                                        case 3: PokemonActifJoueur.c3 = capaciteaApprendre1
                                else:
                                    match capaciteaChanger:
                                        case 1: PokemonActifJoueur.c1 = capaciteaApprendre2
                                        case 2: PokemonActifJoueur.c2 = capaciteaApprendre2
                                        case 3: PokemonActifJoueur.c3 = capaciteaApprendre2
                                
                attaque1texte = my_font.render("A : "+PokemonActifJoueur.c1.nom, True,(0, 0, 0))
                attaque2texte = my_font.render("Z : "+PokemonActifJoueur.c2.nom, True,(0, 0, 0))
                attaque3texte = my_font.render("E : "+PokemonActifJoueur.c3.nom, True,(0, 0, 0))

                
                for i in range(3):
                        rareteObjet = random.randint(85,85)
                        if rareteObjet>95:
                            if not EfficaciteActif:
                                objetselection[i]=tabobjetglobal[random.randint(22,24)]
                            else: objetselection[i]=tabobjetglobal[random.randint(23,24)]
                        elif 80<rareteObjet<=95:
                            if not StabilisateurActif:
                                objetselection[i]=tabobjetglobal[random.randint(18,18)]
                            else:
                                objetselection[i]=tabobjetglobal[random.randint(18,21)]
                        elif 50<rareteObjet<=80:
                            objetselection[i]=tabobjetglobal[random.randint(10,16)]
                        else: objetselection[i]=tabobjetglobal[random.randint(1,9)] #Objet -> classe avec toutes les stats, et un if qui vérifie si item stat ou autre (parce que très peu d'autres item) et applique stat
                        objetselection[i].image = pygame.transform.scale(objetselection[i].image,(100,100))

                while selectionItem:
                    screen.blit(imageBackground,(0,0))
                    tempsDeJeu = my_font.render(str(round((pygame.time.get_ticks()-tempsApresEcranTitre)/1000,1)), True,(0, 0, 0))
                    screen.blit(tempsDeJeu, (1190,5))
                    for i in range(3):
                        nomObjetTexte[i] = my_font.render(objetselection[i].nom,True,objetselection[i].couleurRarete)
                        screen.blit(nomObjetTexte[i],((40*(i*10))+150,280))
                        screen.blit(objetselection[i].image,((40*(i*10))+200,350))
                        pygame.draw.rect(screen,objetselection[i].couleurRarete,((40*(i*10))+200,350,107,107),7)

                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            selectionItem = False
                            running = False
                        if event.type == pygame.KEYDOWN:
                            if event.key==pygame.K_q:
                                selectionItem = False
                                if objetselection[0].nom == "Stabilisateur":
                                    StabilisateurActif = True
                                elif objetselection[0].nom == "Efficacite":
                                    EfficaciteActif = True
                                elif objetselection[0].nom == "Cameleon":
                                    selectionTypeCameleon = True   
                                else:
                                    PokemonActifJoueur.modifatt += objetselection[0].modifatt
                                    PokemonActifJoueur.modifdef += objetselection[0].modifdef
                                    PokemonActifJoueur.modifspa += objetselection[0].modifspa
                                    PokemonActifJoueur.modifspdef += objetselection[0].modifspdef
                                    PokemonActifJoueur.modifvit += objetselection[0].modifvit
                                    PokemonActifJoueur.pv += objetselection[0].modifvie
                                    PokemonActifJoueur.pvmax += objetselection[0].modifvie
                                    PokemonActifJoueur.voldevie += objetselection[0].modifvoldevie
                                    PokemonActifJoueur.degatCritique += objetselection[0].modifdegatCritique
                                    PokemonActifJoueur.chanceCritique += objetselection[0].modifchanceCritique
                            if event.key==pygame.K_s:
                                selectionItem = False
                                if objetselection[1].nom == "Stabilisateur":
                                    StabilisateurActif = True
                                elif objetselection[1].nom == "Efficacite":
                                    EfficaciteActif = True
                                elif objetselection[1].nom == "Cameleon":
                                    selectionTypeCameleon = True
                                        
                                else:
                                    PokemonActifJoueur.modifatt += objetselection[1].modifatt
                                    PokemonActifJoueur.modifdef += objetselection[1].modifdef
                                    PokemonActifJoueur.modifspa += objetselection[1].modifspa
                                    PokemonActifJoueur.modifspdef += objetselection[1].modifspdef
                                    PokemonActifJoueur.modifvit += objetselection[1].modifvit
                                    PokemonActifJoueur.pv += objetselection[1].modifvie
                                    PokemonActifJoueur.pvmax += objetselection[1].modifvie
                                    PokemonActifJoueur.voldevie += objetselection[1].modifvoldevie
                                    PokemonActifJoueur.degatCritique += objetselection[1].modifdegatCritique
                                    PokemonActifJoueur.chanceCritique += objetselection[1].modifchanceCritique
                            if event.key==pygame.K_d:
                                selectionItem = False
                                if objetselection[2].nom == "Stabilisateur":
                                    StabilisateurActif = True
                                elif objetselection[2].nom == "Efficacite":
                                    EfficaciteActif = True
                                elif objetselection[2].nom == "Cameleon":
                                    selectionTypeCameleon = True 

                                        
                                else:
                                    PokemonActifJoueur.modifatt += objetselection[2].modifatt
                                    PokemonActifJoueur.modifdef += objetselection[2].modifdef
                                    PokemonActifJoueur.modifspa += objetselection[2].modifspa
                                    PokemonActifJoueur.modifspdef += objetselection[2].modifspdef
                                    PokemonActifJoueur.modifvit += objetselection[2].modifvit
                                    PokemonActifJoueur.pv += objetselection[2].modifvie
                                    PokemonActifJoueur.pvmax += objetselection[2].modifvie 
                                    PokemonActifJoueur.voldevie += objetselection[2].modifvoldevie
                                    PokemonActifJoueur.degatCritique += objetselection[2].modifdegatCritique
                                    PokemonActifJoueur.chanceCritique += objetselection[2].modifchanceCritique

                for i in range(3):
                    typesselection[i]=tabtypecameleon[random.randint(1,18)]
                while selectionTypeCameleon:
                    screen.blit(imageBackground,(0,0))
                    tempsDeJeu = my_font.render(str(round((pygame.time.get_ticks()-tempsApresEcranTitre)/1000,1)), True,(0, 0, 0))
                    screen.blit(tempsDeJeu, (1190,5))
                    for i in range(3):
                        nomTypesTexte[i] = my_font.render(str(i+1)+" : "+typesselection[i],True,(0,0,0))
                        type1ou2selection = my_font.render("Le type numéro "+str(typeachanger)+" va changer",True,(0,0,0))
                        screen.blit(nomTypesTexte[i],((40*(i*10))+150,280))
                        screen.blit(type1ou2selection,(375,500))
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            selectionTypeCameleon = False
                            running = False
                        if event.type == pygame.KEYDOWN:

                            if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                                if typeachanger == 1:
                                    typeachanger = 2
                                else : 
                                    typeachanger = 1
                                print(typeachanger)
                                
                            
                            if event.key==pygame.K_q:
                                selectionTypeCameleon = False
                                if typeachanger == 1:
                                    PokemonActifJoueur.type1 = typesselection[0]
                                else: 
                                    PokemonActifJoueur.type2 = typesselection[0]

                            if event.key==pygame.K_s:
                                selectionTypeCameleon = False
                                if typeachanger == 1:
                                    PokemonActifJoueur.type1 = typesselection[1]
                                else: 
                                    PokemonActifJoueur.type2 = typesselection[1]

                            if event.key==pygame.K_d:
                                selectionTypeCameleon = False
                                if typeachanger == 1:
                                    PokemonActifJoueur.type1 = typesselection[2]
                                else: 
                                    PokemonActifJoueur.type2 = typesselection[2]
                            
                            if event.key==pygame.K_x:
                                selectionTypeCameleon = False


            pokeJ_health_bar = HealthBar(131,370,PokemonActifJoueur.pv,PokemonActifJoueur.pvmax)
            CompteurMort +=1

            prepaAtt1 = False
            prepaAtt2 = False
            prepaAtt3 = False

            while intAnimMort>0:
                intAnimMort-=10
                screen.blit(imageBackground,(0,0))
                pokeJ_health_bar.draw(PokemonActifJoueur.pv)
                pokeB_health_bar.draw(PokemonActifIA.pv)
                pokeJ_shield_bar.draw(PokemonActifJoueur.bouclier)
                if AffichageAide:
                    screen.blit(attaque1texte, (0,5))
                    screen.blit(attaque2texte, (0,35))
                    screen.blit(attaque3texte, (0,65))

                    screen.blit(tempsDeJeu, (1190,5))
                    screen.blit(texteCompteurMort, (1190,25))
                pygame.draw.rect(screen,'grey',(130,670,50,50))
                pygame.draw.rect(screen,'green',(130,670,TauxCdC1,50))
                if C1Prete:
                    pygame.draw.rect(screen,'gold',(130,665,55,55),5)
                else: pygame.draw.rect(screen,'black',(130,665,55,55),5)
                screen.blit(cooldownC1Texte, (140,680))

                pygame.draw.rect(screen,'grey',(200,670,50,50))
                pygame.draw.rect(screen,'green',(200,670,TauxCdC2,50))
                if C2Prete:
                    pygame.draw.rect(screen,'gold',(200,665,55,55),5)
                else: pygame.draw.rect(screen,'black',(200,665,55,55),5)
                screen.blit(cooldownC2Texte, (210,680))

                pygame.draw.rect(screen,'grey',(270,670,50,50))
                pygame.draw.rect(screen,'green',(270,670,TauxCdC3,50))
                if C3Prete:
                    pygame.draw.rect(screen,'gold',(270,665,55,55),5)
                else: pygame.draw.rect(screen,'black',(270,665,55,55),5)

                screen.blit(PokemonActifJoueur.imagetype1,(130,347))
                screen.blit(PokemonActifJoueur.imagetype2,(233,347))

                screen.blit(PokemonActifIA.imagetype1,(970,347))
                screen.blit(PokemonActifIA.imagetype2,(1073,347))

                screen.blit(cooldownC3Texte, (280,680))
                screen.blit(PokemonActifJoueur.image,(100,380))
                screen.blit(PokemonActifIA.image,(950,400+(100-intAnimMort)))
                pygame.display.flip()
                pygame.time.wait(2)

            sbireAlea = random.randint(1,2)
            if CompteurMort % 10 == 0:
                PokemonActifJoueur.pv += 400
                PokemonActifJoueur.bouclier += 10
                PokemonActifIA = tabcrea[CompteurMort // 10][2].copy()
            else:
                PokemonActifJoueur.pv += 150
                PokemonActifJoueur.bouclier += 2
                PokemonActifIA = tabcrea[(CompteurMort // 10)+1][sbireAlea - 1].copy()

            PokemonActifJoueur.imagetype1 = pygame.image.load(os.path.join(image_dir,'SpriteType'+PokemonActifJoueur.type1+'.png'))
            PokemonActifJoueur.imagetype2 = pygame.image.load(os.path.join(image_dir,'SpriteType'+PokemonActifJoueur.type2+'.png')) 

            PokemonActifIA.imagetype1 = pygame.transform.scale(PokemonActifIA.imagetype1,(100,20))
            PokemonActifIA.imagetype2 = pygame.transform.scale(PokemonActifIA.imagetype2,(100,20))

            PokemonActifJoueur.imagetype1 = pygame.transform.scale(PokemonActifJoueur.imagetype1,(100,20))
            PokemonActifJoueur.imagetype2 = pygame.transform.scale(PokemonActifJoueur.imagetype2,(100,20))

            if PokemonActifJoueur.bouclier>PokemonActifJoueur.boucliermax:
                PokemonActifJoueur.bouclier=PokemonActifJoueur.boucliermax

            if PokemonActifJoueur.pv>PokemonActifJoueur.pvmax:
                PokemonActifJoueur.pv=PokemonActifJoueur.pvmax

            pokeB_health_bar = HealthBar(971,370,PokemonActifIA.pv,PokemonActifIA.pvmax)
            pokeB_health_bar.draw(PokemonActifIA.pv)
            pokeJ_health_bar.draw(PokemonActifJoueur.pv)
            pokeJ_shield_bar.draw(PokemonActifJoueur.bouclier)

            Cdbot=(random.randint(2,4)*1000)-(PokemonActifIA.vitesse)
            NumAttBot = random.randint(1,3)



        elif PokemonActifIA.vivant and PokemonActifIA.pv>0:
            if pygame.time.get_ticks()-tempsApresEcranTitre>timeCdbot+Cdbot-750 and NumAttBot==1:
                prepaAtt1 = True

            if pygame.time.get_ticks()-tempsApresEcranTitre>timeCdbot+Cdbot and not Parade and NumAttBot==1 and prepaAtt1:
                prepaAtt1 = False
                PokemonActifJoueur.pv-=PokemonActifIA.combat(PokemonActifJoueur,1,False,False)
                pokeJ_health_bar.draw(PokemonActifJoueur.pv)
                pygame.display.flip()
                Cdbot=(random.randint(2,4)*1000)-(PokemonActifIA.vitesse)
                timeCdbot=pygame.time.get_ticks()
                NumAttBot = random.randint(1,3)
            elif Parade and NumAttBot==1:
                prepaAtt1 = False
                Cdbot=(random.randint(2,4)*1000)-(PokemonActifIA.vitesse)
                timeCdbot=pygame.time.get_ticks()
                NumAttBot = random.randint(1,3)


            

            if pygame.time.get_ticks()-tempsApresEcranTitre>timeCdbot+Cdbot-750 and NumAttBot==2:
                prepaAtt2 = True

            if pygame.time.get_ticks()-tempsApresEcranTitre>timeCdbot+Cdbot and not Parade and NumAttBot==2 and prepaAtt2:
                prepaAtt2 = False
                PokemonActifJoueur.pv-=PokemonActifIA.combat(PokemonActifJoueur,2,False,False)
                pokeJ_health_bar.draw(PokemonActifJoueur.pv)
                pygame.display.flip()
                timeCdbot=pygame.time.get_ticks()
                Cdbot=(random.randint(2,4)*1000)-(PokemonActifIA.vitesse)
                NumAttBot = random.randint(1,3)
            elif Parade and NumAttBot==2:
                prepaAtt2 = False
                timeCdbot=pygame.time.get_ticks()
                Cdbot=(random.randint(2,4)*1000)-(PokemonActifIA.vitesse)
                NumAttBot = random.randint(1,3)


            

            if pygame.time.get_ticks()-tempsApresEcranTitre>timeCdbot+Cdbot-750 and NumAttBot==3:
                prepaAtt3 = True

            if pygame.time.get_ticks()-tempsApresEcranTitre>timeCdbot+Cdbot and not Parade and NumAttBot==3 and prepaAtt3:
                prepaAtt3 = False
                PokemonActifJoueur.pv-=PokemonActifIA.combat(PokemonActifJoueur,3,False,False)
                pokeJ_health_bar.draw(PokemonActifJoueur.pv)
                pygame.display.flip()
                timeCdbot=pygame.time.get_ticks()
                Cdbot=(random.randint(2,4)*1000)-(PokemonActifIA.vitesse)
                NumAttBot = random.randint(1,3)
            elif Parade and NumAttBot==3:
                prepaAtt3 = False
                timeCdbot=pygame.time.get_ticks()
                Cdbot=(random.randint(2,4)*1000)-(PokemonActifIA.vitesse)
                NumAttBot = random.randint(1,3)

        




        # Gesttion des events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                if event.key==pygame.K_o:
                    if AffichageAide:
                        AffichageAide=False
                    else:AffichageAide=True

                if PokemonActifJoueur.vivant and PokemonActifIA.vivant:
                    #Si la touche a est enfoncée et que le temps est supérieur au temps du cooldown on lance la compétence 1
                    if event.key==pygame.K_a and pygame.time.get_ticks()>timeCdC1+CdC1 and not attaqueEnCours:
                        attaqueEnCours = True
                        Degat = PokemonActifJoueur.combat(PokemonActifIA,1,StabilisateurActif,EfficaciteActif)
                        PokemonActifIA.pv-=Degat
                        VieVolee = (Degat*PokemonActifJoueur.voldevie)/100
                        pokeB_health_bar.draw(PokemonActifIA.pv)
                        PokemonActifJoueur.pv += VieVolee
                        if PokemonActifJoueur.pv>PokemonActifJoueur.pvmax:PokemonActifJoueur.pv=PokemonActifJoueur.pvmax
                        pokeJ_health_bar.draw(PokemonActifJoueur.pv)
                        pygame.display.flip()
                        timeCdC1=pygame.time.get_ticks()
                        C1Prete = False
                        attaqueEnCours = False
                
                    elif event.key==pygame.K_a and pygame.time.get_ticks()<timeCdC1+CdC1:print("Compétence 1 pas rechargée : " + str((round(((timeCdC1+CdC1)-pygame.time.get_ticks())/1000, 1))))

                    #Si la touche z est enfoncée et que le temps est supérieur au temps du cooldown on lance la compétence 2
                    if event.key==pygame.K_z and pygame.time.get_ticks()>timeCdC2+CdC2 and not attaqueEnCours:
                        attaqueEnCours = True
                        Degat = PokemonActifJoueur.combat(PokemonActifIA,2,StabilisateurActif,EfficaciteActif)
                        PokemonActifIA.pv-=Degat
                        VieVolee = (Degat*PokemonActifJoueur.voldevie)/100
                        pokeB_health_bar.draw(PokemonActifIA.pv)
                        PokemonActifJoueur.pv += VieVolee
                        if PokemonActifJoueur.pv>PokemonActifJoueur.pvmax:PokemonActifJoueur.pv=PokemonActifJoueur.pvmax
                        pokeJ_health_bar.draw(PokemonActifJoueur.pv)
                        pygame.display.flip()
                        timeCdC2=pygame.time.get_ticks()
                        C2Prete = False
                        attaqueEnCours = False
                
                    elif event.key==pygame.K_z and pygame.time.get_ticks()<timeCdC2+CdC2:print("Compétence 2 pas rechargée: " + str((round(((timeCdC2+CdC2)-pygame.time.get_ticks())/1000,1))))

                    #Si la touche e est enfoncée et que le temps est supérieur au temps du cooldown on lance la compétence 3
                    if event.key==pygame.K_e and pygame.time.get_ticks()>timeCdC3+CdC3 and not attaqueEnCours:
                        attaqueEnCours = True
                        Degat = PokemonActifJoueur.combat(PokemonActifIA,3,StabilisateurActif,EfficaciteActif)
                        PokemonActifIA.pv-=Degat
                        VieVolee = (Degat*PokemonActifJoueur.voldevie)/100
                        pokeB_health_bar.draw(PokemonActifIA.pv)
                        PokemonActifJoueur.pv += VieVolee
                        if PokemonActifJoueur.pv>PokemonActifJoueur.pvmax:PokemonActifJoueur.pv=PokemonActifJoueur.pvmax
                        pokeJ_health_bar.draw(PokemonActifJoueur.pv)
                        pygame.display.flip()
                        timeCdC3=pygame.time.get_ticks()
                        C3Prete = False
                        attaqueEnCours = False
                
                    elif event.key==pygame.K_e and pygame.time.get_ticks()<timeCdC3+CdC3:print("Compétence 3 pas rechargée: " + str((round(((timeCdC3+CdC3)-pygame.time.get_ticks())/1000,1))))



                    if event.key==pygame.K_SPACE:
                        if PokemonActifJoueur.bouclier>0.5:
                            Parade=True
                    
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_SPACE:
                    Parade=False
            

            if PokemonActifJoueur.vivant and PokemonActifIA.vivant:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                    if random.randint(1,100)<PokemonActifJoueur.chanceCritique:
                        Degat = ((PokemonActifJoueur.attaque/40)*PokemonActifJoueur.degatCritique)-PokemonActifIA.defense/100
                        PokemonActifIA.pv-=Degat
                        VieVolee = (Degat*PokemonActifJoueur.voldevie)/100
                        screen.blit(imDegatCrit,(1050,540))
                    else:
                        Degat = (PokemonActifJoueur.attaque/40)-PokemonActifIA.defense/100
                        PokemonActifIA.pv-=Degat
                        VieVolee = (Degat*PokemonActifJoueur.voldevie)/100
                        screen.blit(imDegat,(1050,540))
                    PokemonActifJoueur.pv += VieVolee
                    if PokemonActifJoueur.pv>PokemonActifJoueur.pvmax:PokemonActifJoueur.pv=PokemonActifJoueur.pvmax
                    pokeJ_health_bar.draw(PokemonActifJoueur.pv)
                    pygame.display.flip()
                    pygame.time.wait(5)

        if PokemonActifJoueur.vivant:
            if Parade:
                if PokemonActifJoueur.bouclier>0.5:
                    PokemonActifJoueur.bouclier-=0.5
                    pokeJ_shield_bar.draw(PokemonActifJoueur.bouclier)
                    pygame.display.flip()
                else:
                    PokemonActifJoueur.bouclier=0
                    Parade=False

            


                    

        

        # Remplie l'écran d'une couleur, puis pose l'image de fond
        screen.fill("cyan")
        screen.blit(imageBackground,(0,0))

        
        

        
        # Calcule des cooldowns
        RatioCdC1 = ((timeCdC1+CdC1-pygame.time.get_ticks())/CdC1)*100
        RatioCdC2 = ((timeCdC2+CdC2-pygame.time.get_ticks())/CdC2)*100
        RatioCdC3 = ((timeCdC3+CdC3-pygame.time.get_ticks())/CdC3)*100
        if RatioCdC1<0:
            RatioCdC1=0
            C1Prete = True
        if RatioCdC2<0:
            RatioCdC2=0
            C2Prete = True
        if RatioCdC3<0:
            RatioCdC3=0
            C3Prete = True
        TauxCdC1 = (100-RatioCdC1)/2
        TauxCdC2 = (100-RatioCdC2)/2
        TauxCdC3 = (100-RatioCdC3)/2


        
        screen.blit(PokemonActifJoueur.imagetype1,(130,347))
        screen.blit(PokemonActifJoueur.imagetype2,(233,347))

        screen.blit(PokemonActifIA.imagetype1,(970,347))
        screen.blit(PokemonActifIA.imagetype2,(1073,347))


        #On dessine les barres de vie et de bouclier
        pokeJ_health_bar.draw(PokemonActifJoueur.pv)
        pokeB_health_bar.draw(PokemonActifIA.pv)
        pokeJ_shield_bar.draw(PokemonActifJoueur.bouclier)


        #Texte
        tempsDeJeu = my_font.render(str(round((pygame.time.get_ticks()-tempsApresEcranTitre)/1000,1)), True,(0, 0, 0))
        texteCompteurMort = my_font.render(str(CompteurMort),True,(0, 0, 0))

        #On affiche les différents éléments à l'écran
        screen.blit(PokemonActifJoueur.image,(100,380))
        screen.blit(PokemonActifIA.image,(950,400))

        if AffichageAide:
            screen.blit(attaque1texte, (0,5))
            screen.blit(attaque2texte, (0,35))
            screen.blit(attaque3texte, (0,65))

            screen.blit(tempsDeJeu, (1190,5))
            screen.blit(texteCompteurMort, (1190,25))

        pygame.draw.rect(screen,'grey',(130,670,50,50))
        pygame.draw.rect(screen,'green',(130,670,TauxCdC1,50))
        if C1Prete:
            pygame.draw.rect(screen,'gold',(130,665,55,55),5)
        else: pygame.draw.rect(screen,'black',(130,665,55,55),5)
        screen.blit(cooldownC1Texte, (140,680))

        pygame.draw.rect(screen,'grey',(200,670,50,50))
        pygame.draw.rect(screen,'green',(200,670,TauxCdC2,50))
        if C2Prete:
            pygame.draw.rect(screen,'gold',(200,665,55,55),5)
        else: pygame.draw.rect(screen,'black',(200,665,55,55),5)
        screen.blit(cooldownC2Texte, (210,680))

        pygame.draw.rect(screen,'grey',(270,670,50,50))
        pygame.draw.rect(screen,'green',(270,670,TauxCdC3,50))
        if C3Prete:
            pygame.draw.rect(screen,'gold',(270,665,55,55),5)
        else: pygame.draw.rect(screen,'black',(270,665,55,55),5)
        screen.blit(cooldownC3Texte, (280,680))


        
        if PokemonActifJoueur.pv<=0:
            PokemonActifJoueur.vivant=False

        if prepaAtt1:
            screen.blit(imAuraRouge,(870,325))
        elif prepaAtt2:
            screen.blit(imAuraOrange,(870,325))
        elif prepaAtt3:
            screen.blit(imAuraViolette,(870,325))
        
        if Parade:
            screen.blit(imBouclier,(65,380))
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
