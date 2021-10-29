# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 00:04:20 2021

@author: Martin
"""
import math
import random
import time

#%% temperature sample
def Sample(filename):
    f = open(filename, "r")
    lines = f.readlines()
    cleanSample=[]
    for i in range(1,len(lines)):
        string=""
        a=0
        b=0
        for j in range(len(lines[i])):
            if lines[i][j]!=';': 
                string=string+lines[i][j]
            else:
                a=float(string)
                string=''
        b=float(string)
        cleanSample.append((a,b))
    f.close()
    return cleanSample    

sample=Sample("temperature_sample.csv")
        
#%% fonction de Weierstrass
def Weier(a,b,c,i):
    result = 0
    for n in range (c+1):
        result = result + (a**n)*math.cos((b**n)*math.pi*i)
    return result

#%% géneration d'une population
def Population(count):
    population = []
    for i in range((count)):
        a = random.randint(1,99)/100.00
        b = random.randint(1,20)
        c = random.randint(1,20)
        f = 999
        population.append([a,b,c,f])
    return population

#%% fonction fitness        
def Fitness(a,b,c):
    somme_ecart = 0
    for i in range(len(sample)):
        ecart = abs(Weier(a, b, c, sample[i][0])-sample[i][1])
        somme_ecart = somme_ecart + ecart
    return (somme_ecart/len(sample))

#%% sélection individu
def Selection(pop,hcount,lcount):
    def takeFit(elem):
        return elem[3]
    pop.sort(key=takeFit)
    souspop=[]
    for i in range(hcount):
        souspop.append(pop[i])
    for i in range(lcount):
        souspop.append(pop[len(pop)-1-i])
    return souspop

#%% croisement
def Croisement(pop):
    l = len(pop)
    for i in range (0,l,2):
        rand_parent = random.choice([0,1])
        a = pop[i+rand_parent][0]
        a1 = pop[i+(1-rand_parent)][0]
        b = pop[i+(1-rand_parent)][1]
        b1 = pop[i+(rand_parent)][1]
        c = pop[i+(1-rand_parent)][2]
        c1 = pop[i+(rand_parent)][2]
        f=999
        f1=999
        pop.append([a,b,c,f])
        pop.append([a1,b1,c1,f1])
    return pop
    
#%% mutation 
def Mutation(pop):
    for i in range(len(pop)//3):
        n = random.randint(0,len(pop)-1)
        i = random.randint(0,5)
        if (i == 0 or i==1 or i==2):
            pop[n][0] = random.randint(1,99)/100.00
        if (i == 3):
            pop[n][1] = random.randint(1,20)
        if (i == 4):
            pop[n][2] = random.randint(1,20)
    return pop

def AffichageResultat(pop):
    print("RESULTAT")
    print("a =",pop[0][0])
    print("b =",pop[0][1])
    print("c =",pop[0][2])
    
#%% algo génetique
def Algo(j_max):
    j=0
    tempsTotal = 0
    win = 0
    while (j<j_max):
        j=j+1
        bestindiv=0
        n=0
        start = time.time()
        pop  = Population((26)) #géneration de la population d'individus
        while (True):
            #2-calcul de la fonction fitness pour chaque individu
            for i in range (len(pop)): 
                pop[i][3] = Fitness(pop[i][0],pop[i][1],pop[i][2])
            #3-sélection des individus
            pop = Selection(pop,10,3)
            #test si le meileur indiv est le même que lors du dernier process
            if bestindiv != (pop[0][0],pop[0][1],pop[0][2]):
                n=0
                bestindiv = (pop[0][0],pop[0][1],pop[0][2])
            else: n=n+1
            if n==100: break #si le meilleur individu est le même pour 100 runs, break
            #4-croisement 
            pop = Croisement(pop)
            #5-mutation
            pop = Mutation(pop)
        AffichageResultat(pop)
        end = time.time()
        temps=end-start
        tempsTotal=tempsTotal+temps
        if pop[0][0]==0.35 and pop[0][1]==15 and pop[0][2]==2: win=win+1
    print("TEMPS MOYEN SUR",j,"RUNS:" ,round(tempsTotal/j,2), "SECONDES")
    print("TAUX DE REUSSITE CONVERGENCE: ",round(win/j,2)*100,"%",sep='')
    
#%%test annexe
def TestApprox():
    sample=Sample("temperature_sample_calibrate2.csv")
    mwins=0
    cwins=0
    for i in range(len(sample)):
        r_martin = abs(Weier(0.14,19,2,sample[i][0])-sample[i][1])
        r_cr = abs(Weier(0.14,19,5,sample[i][0])-sample[i][1])
        if r_martin < r_cr:
            print("MARTIN",r_martin)
            mwins = mwins+1
        else: 
            print("M.RODRIGUES",r_cr)
            cwins=cwins+1
    print("/////")
    print("SCORE FINAL: MARTIN",mwins,"-",cwins,"M.RODRIGUES")
    