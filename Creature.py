import os
script_dir = os.path.dirname(__file__)
image_dir = os.path.join(script_dir, 'Images')
image_objet_dir = os.path.join(image_dir, 'Objet')
import pygame
import random


types = {
    "Normal": {
        "Faiblesses": ["Combat"],
        "Résistances": [],
        "Immunites": ["Spectre"]
    },
    "Feu": {
        "Faiblesses": ["Eau", "Roche", "Sol"],
        "Résistances": ["Feu", "Plante", "Glace", "Insecte", "Acier", "Fée"],
        "Immunites": []
    },
    "Eau": {
        "Faiblesses": ["Électrik", "Plante"],
        "Résistances": ["Feu", "Eau", "Glace", "Acier"],
        "Immunites": []
    },
    "Électrik": {
        "Faiblesses": ["Sol"],
        "Résistances": ["Électrik", "Vol", "Acier"],
        "Immunites": []
    },
    "Plante": {
        "Faiblesses": ["Feu", "Glace", "Poison", "Vol", "Insecte"],
        "Résistances": ["Eau", "Électrik", "Plante", "Sol"],
        "Immunites": []
    },
    "Glace": {
        "Faiblesses": ["Feu", "Combat", "Roche", "Acier"],
        "Résistances": ["Glace"],
        "Immunites": []
    },
    "Combat": {
        "Faiblesses": ["Vol", "Psy", "Fée"],
        "Résistances": ["Roche", "Acier"],
        "Immunites": ["Spectre"]
    },
    "Poison": {
        "Faiblesses": ["Sol", "Psy"],
        "Résistances": ["Combat", "Poison", "Insecte", "Fée"],
        "Immunites": []
    },
    "Sol": {
        "Faiblesses": ["Eau", "Plante", "Glace"],
        "Résistances": ["Poison", "Roche"],
        "Immunites": ["Électrik"]
    },
    "Vol": {
        "Faiblesses": ["Électrik", "Roche", "Glace"],
        "Résistances": ["Plante", "Combat", "Insecte"],
        "Immunites": ["Sol"]
    },
    "Psy": {
        "Faiblesses": ["Insecte", "Ténèbres", "Spectre"],
        "Résistances": ["Combat", "Psy"],
        "Immunites": []
    },
    "Insecte": {
        "Faiblesses": ["Feu", "Vol", "Roche"],
        "Résistances": ["Plante", "Combat", "Sol"],
        "Immunites": []
    },
    "Roche": {
        "Faiblesses": ["Eau", "Plante", "Combat", "Sol", "Acier"],
        "Résistances": ["Normal", "Feu", "Poison", "Vol"],
        "Immunites": []
    },
    "Spectre": {
        "Faiblesses": ["Ténèbres"],
        "Résistances": ["Insecte", "Poison"],
        "Immunites": ["Normal", "Combat"]
    },
    "Dragon": {
        "Faiblesses": ["Glace", "Fée", "Dragon"],
        "Résistances": ["Feu", "Eau", "Plante", "Électrik"],
        "Immunites": []
    },
    "Ténèbres": {
        "Faiblesses": ["Combat", "Insecte", "Fée"],
        "Résistances": ["Spectre", "Ténèbres"],
        "Immunites": ["Psy"]
    },
    "Acier": {
        "Faiblesses": ["Feu", "Combat", "Sol"],
        "Résistances": ["Normal", "Plante", "Glace", "Vol", "Roche", "Dragon", "Acier", "Fée"],
        "Immunites": ["Poison"]
    },
    "Aucun": {
        "Faiblesses": [],
        "Résistances": [],
        "Immunites": []
    },
    "Fée": {
        "Faiblesses": ["Poison", "Acier"],
        "Résistances": ["Combat", "Insecte", "Ténèbres"],
        "Immunites": ["Dragon"]
    }
}


def calcFaiblesse(typeattaque,typedefense,Efficacite):

    multipl_type = 1
    if typeattaque in types[typedefense]["Faiblesses"]:
        multipl_type = 2
    
    elif typeattaque in types[typedefense]["Résistances"]:
        multipl_type = 0.5

    elif typeattaque in types[typedefense]["Immunites"]:
        multipl_type = 0
    if multipl_type<2 and Efficacite:
        multipl_type *=2
    return multipl_type



class Attaque():
     def __init__(self,nom,categorie,puissance,precision,type):
          self.nom = nom
          self.categorie = categorie
          self.puissance = puissance
          self.precision = precision
          self.type = type


class Objet():
    def __init__(self,nom,modifatt,modifdef,modifspa,modifspdef,modifvit,modifvie,modifvoldevie,modifchanceCritique,modifdegatCritique,couleurRarete):
        self.nom = nom
        self.modifatt = modifatt
        self.modifdef = modifdef
        self.modifspa = modifspa
        self.modifspdef = modifspdef
        self.modifvit = modifvit
        self.modifvie = modifvie
        self.modifvoldevie = modifvoldevie
        self.modifchanceCritique = modifchanceCritique
        self.modifdegatCritique = modifdegatCritique
        self.couleurRarete = couleurRarete
        self.image = pygame.image.load(os.path.join(image_objet_dir,self.nom+'.png'))
    def copy(self):
        return Objet(self.nom,self.modifatt,self.modifdef,self.modifspa,self.modifspdef,self.modifvit,self.modifvie,self.modifvoldevie,self.modifchanceCritique,self.modifdegatCritique,self.couleurRarete)

class Pokemon():
    def __init__(self,nom,pv,pvmax,bouclier,boucliermax,attaque,defense,attaquespe,defensespe,vitesse,chanceCritique,degatCritique,type1,type2,c1,c2,c3):
        self.nom = nom
        self.pv = pv
        self.pvmax = pvmax
        self.bouclier = bouclier
        self.boucliermax = boucliermax
        self.attaque = attaque
        self.defense = defense
        self.attaquespe = attaquespe
        self.defensespe = defensespe
        self.vitesse = vitesse
        self.modifatt = 1
        self.modifdef = 1
        self.modifspa = 1
        self.modifspdef = 1
        self.modifvit = 1
        self.voldevie = 0
        self.chanceCritique = chanceCritique
        self.degatCritique = degatCritique
        self.type1 = type1
        self.type2 = type2
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.vivant = True
        self.image = pygame.image.load(os.path.join(image_dir,self.nom+'.png'))
        self.imagetype1 = pygame.image.load(os.path.join(image_dir,'SpriteType'+self.type1+'.png'))
        self.imagetype2 = pygame.image.load(os.path.join(image_dir,'SpriteType'+self.type2+'.png')) 
        self.rect = self.image.get_rect()
    

    def copy(self):
        return Pokemon(self.nom, self.pv, self.pvmax, self.bouclier, self.boucliermax, self.attaque, self.defense, self.attaquespe, self.defensespe, self.vitesse, self.chanceCritique, self.degatCritique, self.type1, self.type2, self.c1, self.c2, self.c3)

    def combat(self, adversaire, choixatt, Stabilisateur, Efficacite):
        if not isinstance(adversaire, Pokemon):
            raise TypeError("L'adversaire doit être une instance de Pokemon.")
        else:
            actions = {
                1: self.c1,
                2: self.c2,
                3: self.c3,
                # Ajoutez d'autres actions selon vos besoins
            }
    
            if choixatt in actions:
                action = actions[choixatt]
                efficace1 = calcFaiblesse(action.type,adversaire.type1,Efficacite)
                efficace2 = calcFaiblesse(action.type,adversaire.type2,Efficacite)
                if action.type==self.type1 or action.type==self.type2 or Stabilisateur:
                    stab = 1.5
                else : stab = 1
                if action.categorie == "Physique":
                    degat = ((((((42 * action.puissance * self.attaque * self.modifatt)/ (adversaire.defense * adversaire.modifdef) )/ 50)+2)  + 2) * ((random.randint(217, 255) * 100) / 255) / 100) * stab * efficace1 * efficace2
                elif action.categorie == "Special":
                    degat = ((((((42 * action.puissance * self.attaquespe * self.modifspa)/ (adversaire.defensespe * adversaire.modifspdef) )/ 50)+2)  + 2) * ((random.randint(217, 255) * 100) / 255) / 100) * stab * efficace1 * efficace2
            else:
                raise ValueError("Choix d'attaque invalide.")
            return degat
    def reset(self):
        self.vivant = True
        self.pv=self.pvmax




#Capacités des Créatures
speFeu = Attaque("Feu Special","Special",90,100,"Feu")
phyFeu = Attaque("Feu Physique","Physique",90,100,"Feu")

spePlante = Attaque("Plante Special","Special",90,100,"Plante")
phyPlante = Attaque("Plante Physique","Physique",90,100,"Plante")

speFee = Attaque("Fee Special","Special",90,100,"Fée")
phyFee = Attaque("Fee Physique","Physique",90,100,"Fée")

speEau = Attaque("Eau Special","Special",90,100,"Eau")
phyEau = Attaque("Eau Physique","Physique",90,100,"Eau")

speRoche = Attaque("Roche Special","Special",90,100,"Roche")
phyRoche = Attaque("Roche Physique","Physique",90,100,"Roche")

speNormal = Attaque("Normal Special","Special",90,100,"Normal")
phyNormal = Attaque("Normal Physique","Physique",90,100,"Normal")

speVol = Attaque("Vol Special","Special",90,100,"Vol")
phyVol = Attaque("Vol Physique","Physique",90,100,"Vol")

speSol = Attaque("Sol Special","Special",90,100,"Sol")
phySol = Attaque("Sol Physique","Physique",90,100,"Sol")

speInsecte = Attaque("Insecte Special","Special",90,100,"Insecte")
phyInsecte = Attaque("Insecte Physique","Physique",90,100,"Insecte")

speElectrik = Attaque("Electrik Special","Special",90,100,"Électrik")
phyElectrik = Attaque("Electrik Physique","Physique",90,100,"Électrik")

spePoison = Attaque("Poison Special","Special",90,100,"Poison")
phyPoison = Attaque("Poison Physique","Physique",90,100,"Poison")

speTenebres = Attaque("Tenebres Special","Special",90,100,"Ténèbres")
phyTenebres = Attaque("Tenebres Physique","Physique",90,100,"Ténèbres")

speAcier = Attaque("Acier Special","Special",90,100,"Acier")
phyAcier = Attaque("Acier Physique","Physique",90,100,"Acier")

speDragon = Attaque("Dragon Special","Special",90,100,"Dragon")
phyDragon = Attaque("Dragon Physique","Physique",90,100,"Dragon")

speCombat = Attaque("Combat Special","Special",90,100,"Combat")
phyCombat = Attaque("Combat Physique","Physique",90,100,"Combat")

spePsy = Attaque("Psy Special","Special",90,100,"Psy")
phyPsy = Attaque("Psy Physique","Physique",90,100,"Psy")

speGlace = Attaque("Glace Special","Special",90,100,"Glace")
phyGlace = Attaque("Glace Physique","Physique",90,100,"Glace")

speSpectre = Attaque("Spectre Special","Special",90,100,"Spectre")
phySpectre = Attaque("Spectre Physique","Physique",90,100,"Spectre")

#Objets 
BandeauAttaque = Objet("Bandeau Attaque",0.1,0,0,0,0,0,0,0,0,(142,142,142))
BandeauDefense = Objet("Bandeau Defense",0,0.1,0,0,0,0,0,0,0,(142,142,142))
BandeauAttaqueSpe = Objet("Bandeau Attaque Spe",0,0,0.1,0,0,0,0,0,0,(142,142,142))
BandeauDefenseSpe = Objet("Bandeau Defense Spe",0,0,0,0.1,0,0,0,0,0,(142,142,142))
BandeauVitesse = Objet("Bandeau Vitesse",0,0,0,0,0.1,0,0,0,0,(142,142,142))
BandeauVie = Objet("Bandeau Vie",0,0,0,0,0,25,0,0,0,(142,142,142))
BandeauCritique = Objet("Bandeau Critique",0,0,0,0,0,0,0,2,0,(142,142,142))
BandeauDegatCrit = Objet("Bandeau Degat Crit",0,0,0,0,0,0,0,0,0.05,(142,142,142))
BandeauVoldeVie = Objet("Bandeau Vol de Vie",0,0,0,0,0,0,1,0,0,(142,142,142))

MouchoirOffensif = Objet("Mouchoir Offensif",0.1,0,0.1,0,0,0,0,0,0,(66,122,213))
MouchoirDefensif = Objet("Mouchoir Defensif",0,0.1,0,0.1,0,0,0,0,0,(66,122,213))
MouchoirVitesse = Objet("Mouchoir Vitesse",0,0,0,0,0.2,0,0,0,0,(66,122,213))
MouchoirVie = Objet("Mouchoir Vie",0,0,0,0,0,100,0,0,0,(66,122,213))
MouchoirCritique = Objet("Mouchoir Critique",0,0,0,0,0,0,0,5,0,(66,122,213))
MouchoirDegatCrit = Objet("Mouchoir Degat Crit",0,0,0,0,0,0,0,0,0.1,(66,122,213))
MouchoirVoldeVie = Objet("Mouchoir Vol de Vie",0,0,0,0,0,0,4,0,0,(66,122,213))

Stabilisateur = Objet("Stabilisateur",0,0,0,0,0,0,0,0,0,(173,66,213))
Cameleon = Objet("Cameleon",0,0,0,0,0,0,0,0,0,(173,66,213))
Equilibre = Objet("Equilibre",0.1,0.1,0.1,0.1,0.1,100,0,0,0,(173,66,213))
Critique = Objet("Critique",0,0,0,0,0,0,0,5,0.1,(173,66,213))
Vitalite = Objet("Vitalite",0,0,0,0,0,250,3,0,0,(173,66,213))

Efficacite = Objet("Efficacite",0,0,0,0,0,0,0,0,0,(236,230,43))
StatsSecondes = Objet("StatsSecondes",0,0,0,0,0,500,4,5,0.1,(236,230,43))
StatsPrimaires = Objet("StatsPrimaires",0.2,0.2,0.2,0.2,0.2,250,0,0,0,(236,230,43))




##Création des Créatures##
StarterVitesse = Pokemon("StarterVitesse",1300,1300,100,100,300,100,500,100,120,10,1.5,"Normal","Vol",phyNormal,phyVol,phyFee)
StarterAttaque = Pokemon("StarterAttaque",130,130,100,100,500,300,500,300,600,10,1.5,"Normal","Vol",phyNormal,phyVol,phyFee)
StarterDefense = Pokemon("StarterDefense",1800,1800,100,100,300,400,500,400,100,10,1.5,"Normal","Vol",phyNormal,phyVol,phyFee)

SbirePlante1 = Pokemon("SbirePlante1",400,400,100,100,750,200,0,250,400,10,1.5,"Plante","Aucun",phyNormal,phyPlante,phyEau)
SbirePlante2 = Pokemon("SbirePlante2",800,800,100,100,0,300,400,200,300,10,1.5,"Plante","Fée",speNormal,spePlante,speFee)
BossPlante = Pokemon("BossPlante",5000,5000,100,100,0,700,750,700,850,10,1.5,"Plante","Aucun",speNormal,spePlante,speEau)

SbireFeu1 = Pokemon("SbireFeu1",400,400,100,100,0,200,800,200,400,10,1.5,"Feu","Électrik",speNormal,speFeu,speElectrik)
SbireFeu2 = Pokemon("SbireFeu2",450,450,100,100,650,300,0,300,300,10,1.5,"Feu","Vol",phyNormal,phyFeu,phyVol)
BossFeu = Pokemon("BossFeu",3500,3500,100,100,0,200,2500,200,1600,10,1.5,"Feu","Aucun",speNormal,speFeu,speVol)

SbireEau1 = Pokemon("SbireEau1",700,700,100,100,200,400,0,400,300,10,1.5,"Eau","Roche",phyNormal,phyEau,phyRoche)
SbireEau2 = Pokemon("SbireEau2",450,450,100,100,450,350,0,350,400,10,1.5,"Eau","Combat",phyNormal,phyEau,phyRoche)
BossEau = Pokemon("BossEau",4000,4000,100,100,0,800,1400,800,100,10,1.5,"Eau","Aucun",speNormal,speEau,speRoche)

SbireFee1 = Pokemon("SbireFee1",700,700,100,100,0,250,300,500,250,10,1.5,"Fée","Insecte",speFee,speInsecte,speElectrik)
SbireFee2 = Pokemon("SbireFee2",500,500,100,100,450,400,0,300,350,10,1.5,"Fée","Électrik",speNormal,speFee,speElectrik)
BossFee = Pokemon("BossFee",4500,4500,100,100,800,1000,0,600,1100,10,1.5,"Fée","Aucun",phyFee,phySol,phyRoche)

SbireNormal1 = Pokemon("SbireNormal1",550,500,100,100,0,300,600,600,450,10,1.5,"Normal","Psy",speNormal,spePsy,speRoche)
SbireNormal2 = Pokemon("SbireNormal2",550,550,100,100,700,500,0,300,450,10,1.5,"Normal","Combat",phyNormal,phyCombat,phySol)
BossNormal = Pokemon("BossNormal",2500,2500,100,100,2300,1100,1000,1100,1000,10,1.5,"Normal","Aucun",speNormal,phyNormal,phyCombat)

SbireVol1 = Pokemon("SbireVol1",250,250,100,100,600,75,0,75,1500,10,1.5,"Vol","Feu",phyNormal,phyVol,phyFeu)
SbireVol2 = Pokemon("SbireVol2",500,500,100,100,750,500,0,350,400,10,1.5,"Vol","Combat",phyNormal,phyVol,phyCombat)
BossVol = Pokemon("BossVol",1500,1500,100,100,1500,1500,1500,1500,100,10,1.5,"Vol","Aucun",speVol,phyNormal,phyVol)

SbireSol1 = Pokemon("SbireSol1",500,500,100,100,500,500,0,500,500,10,1.5,"Sol","Aucun",phyNormal,phySol,phyRoche)
SbireSol2 = Pokemon("SbireSol2",250,250,100,100,350,250,400,250,1000,10,1.5,"Sol","Vol",speVol,speSol,phySol)
BossSol = Pokemon("BossSol",2300,2300,100,100,2400,2450,0,1000,850,10,1.5,"Sol","Aucun",phySol,phySpectre,phyRoche)

SbireInsecte1 = Pokemon("SbireInsecte1",1000,1000,100,100,600,600,0,200,100,10,1.5,"Insecte","Roche",phyRoche,phyInsecte,phyCombat)
SbireInsecte2 = Pokemon("SbireInsecte2",450,450,100,100,0,100,550,400,500,10,1.5,"Insecte","Psy",spePsy,speInsecte,speFee)
BossInsecte = Pokemon("BossInsecte",2500,2500,100,100,3000,1000,0,1000,1500,10,1.5,"Insecte","Aucun",phyVol,phyInsecte,phyDragon)

SbirePoison1 = Pokemon("SbirePoison1",550,550,100,100,0,550,400,550,450,10,1.5,"Poison","Fée",speFee,spePoison,speInsecte)
SbirePoison2 = Pokemon("SbirePoison2",550,550,100,100,0,150,750,700,350,10,1.5,"Poison","Psy",spePsy,spePoison,speEau)
BossPoison = Pokemon("BossPoison",3000,3000,100,100,3000,1500,0,500,1000,10,1.5,"Poison","Aucun",phyPoison,phySol,phyPlante)

SbireElectrik1 = Pokemon("SbireElectrik1",500,500,100,100,900,450,0,350,800,10,1.5,"Électrik","Insecte",phyPlante,phyElectrik,phyInsecte)
SbireElectrik2 = Pokemon("SbireElectrik2",400,400,100,100,0,300,1000,300,1000,10,1.5,"Électrik","Aucun",speNormal,speElectrik,speCombat)
BossElectrik = Pokemon("BossElectrik",3500,3500,100,100,0,1550,2000,1550,140,10,1.5,"Électrik","Aucun",speVol,speElectrik,speTenebres)

SbireAcier1 = Pokemon("SbireAcier1",500,500,100,100,875,325,0,400,900,10,1.5,"Acier","Vol",phyRoche,phyAcier,phyVol)
SbireAcier2 = Pokemon("SbireAcier2",1200,1200,100,100,700,650,0,250,200,10,1.5,"Acier","Électrik",speDragon,speAcier,speElectrik)
BossAcier = Pokemon("BossAcier",4000,4000,100,100,1200,2000,0,2000,800,10,1.5,"Acier","Aucun",phyAcier,phyRoche,phyElectrik)

SbireRoche1 = Pokemon("SbireRoche1",400,400,100,100,650,1100,0,400,450,10,1.5,"Roche","Vol",phySol,phyRoche,phyVol)
SbireRoche2 = Pokemon("SbireRoche2",1000,1000,100,100,500,600,0,600,300,10,1.5,"Roche","Aucun",phyCombat,phyRoche,phyRoche)
BossRoche = Pokemon("BossRoche",3000,3000,100,100,700,3000,0,3000,300,10,1.5,"Roche","Aucun",phyRoche,phyPlante,phyAcier)

SbireGlace1 = Pokemon("SbireGlace1",700,700,100,100,650,500,0,400,750,10,1.5,"Glace","Combat",phyCombat,phyGlace,phyElectrik)
SbireGlace2 = Pokemon("SbireGlace2",500,500,100,100,0,300,800,600,800,10,1.5,"Glace","Psy",speVol,speGlace,spePsy)
BossGlace = Pokemon("BossGlace",3500,3500,100,100,2500,2000,0,950,1050,10,1.5,"Glace","Aucun",phyVol,phyGlace,phyDragon)

SbireSpectre1 = Pokemon("SbireSpectre1",350,350,100,100,0,150,1100,300,1100,10,1.5,"Spectre","Psy",speTenebres,speSpectre,spePsy)
SbireSpectre2 = Pokemon("SbireSpectre2",500,500,100,100,650,500,350,500,500,10,1.5,"Spectre","Sol",phySol,phySpectre,speSpectre)
BossSpectre = Pokemon("BossSpectre",2150,2150,100,100,0,650,5000,750,1450,10,1.5,"Spectre","Aucun",speTenebres,speSpectre,speFeu)

SbireDragon1 = Pokemon("SbireDragon1",700,700,100,100,1000,400,0,400,1500,10,1.5,"Dragon","Vol",phyVol,phyDragon,phyElectrik)
SbireDragon2 = Pokemon("SbireDragon2",800,800,100,100,1500,550,0,500,650,10,1.5,"Dragon","Aucun",phyFeu,phyDragon,phyVol)
BossDragon = Pokemon("BossDragon",3500,3500,100,100,0,3200,2000,3200,1100,10,1.5,"Dragon","Aucun",spePsy,speDragon,spePoison)

SbirePsy1 = Pokemon("SbirePsy1",450,450,100,100,0,150,1500,500,1400,10,1.5,"Psy","Insecte",speInsecte,spePsy,speVol)
SbirePsy2 = Pokemon("SbirePsy2",900,900,100,100,0,400,1200,950,550,10,1.5,"Psy","Dragon",speDragon,spePsy,speGlace)
BossPsy = Pokemon("BossPsy",2550,2550,100,100,0,2000,5000,2400,1050,10,1.5,"Psy","Aucun",speCombat,spePsy,speFeu)

SbireTenebres1 = Pokemon("SbireTenebres1",850,850,100,100,850,850,0,450,1000,10,1.5,"Ténèbres","Vol",phyVol,phyTenebres,phyCombat)
SbireTenebres2 = Pokemon("SbireTenebres2",900,900,100,100,450,700,450,700,800,10,1.5,"Ténèbres","Eau",phyEau,phyTenebres,phyDragon)
BossTenebres = Pokemon("BossTenebres",5100,5100,100,100,0,1400,3500,1850,1150,10,1.5,"Ténèbres","Aucun",spePsy,speTenebres,speFee)

SbireCombat1 = Pokemon("SbireCombat1",1100,1100,100,100,800,800,0,800,500,10,1.5,"Combat","Aucun",phyElectrik,phyCombat,phyPsy)
SbireCombat2 = Pokemon("SbireCombat2",1100,1100,100,100,1200,600,0,600,500,10,1.5,"Combat","Aucun",phyEau,phyCombat,phyRoche)
BossCombat = Pokemon("BossCombat",4000,4000,100,100,3000,3000,0,3000,1000,10,1.5,"Combat","Aucun",phyTenebres,phyCombat,phyFee)