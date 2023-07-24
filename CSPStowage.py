
from collections import Counter
from typing import Container, List
from constraint import *
import random
import sys
import os


###################DATA EXTRACTION FROM FILES####################

#Comprueba que los archivos de entrada existen

def Read_Contenedores(path, name): 
    
    with open(path+"/"+name, 'r') as f:
         lineas = [linea.split() for linea in f]
         contenedores = lineas
   
    return contenedores 

def Read_Map(path ,name):

    with open(path+"/"+name, 'r') as f:
         lineas = [linea.split() for linea in f]
         Mapa = lineas

    
    return Mapa  


#CreamosLa lista con los objetos tipo Contenedores
def CreateObjects(contenedores):
    c =[]
    for i in range(len(contenedores)) :
        c.append([contenedores[i][0], contenedores[i][1], contenedores[i][2]])
    return c
   
#Creamos La lista con los objetos tipo Celda
def CreateCeldasObjects(Mapa):
    c = []
    for i in range (len(Mapa)):      
        for j in range(len(Mapa[0])):   
            c.append([j,i,Mapa[i][j]])

    return c
                

#########################MAIN########################

if(len(sys.argv)!= 4 ):
    print("Invalid number of arguenedores del archivo y lo guardamos en una listametns, please insert the following structure: program.py Fullpath Mapfile ContainerFIle")
    exit(-1)

Path = str(sys.argv[1])
Mapafile = str(sys.argv[2])
Contenedoresfile = str(sys.argv[3])


#Comprobamos que el archivo eenedores del archivo y lo guardamos en una listaxiste dentro de la ruta especificada
#sacamos los contenedores del archivo y lo guardamos en una lista
contenedores = Read_Contenedores(Path,Contenedoresfile)

#sacamos las caracteristicas de la bahía de carga y las guardamos en una lista
Mapa = Read_Map(Path,Mapafile)

#Creamos La lista de objetos contenedores con los que vamos a trabajar
ListaContenedores = CreateObjects(contenedores)



ContenedoresR = []
ContenedoresS = []

ContenedoresTotales = []
for i in range(len(ListaContenedores)):
    if(ListaContenedores[i][1] == 'S'):
        ContenedoresS.append([ListaContenedores[i][0],ListaContenedores[i][2]])
       
    if(ListaContenedores[i][1] == 'R'):
        ContenedoresR.append([ListaContenedores[i][0],ListaContenedores[i][2]])
        


ContenedoresR_puerto1 = []
ContenedoresR_puerto2 = []

for i in range(len(ContenedoresR)):
    if(ContenedoresR[i][1] == '1'):
        ContenedoresR_puerto1.append(ContenedoresR[i][0])
    if(ContenedoresR[i][1] == '2'):
        ContenedoresR_puerto2.append(ContenedoresR[i][0])


ContenedoresR_Ambos =  ContenedoresR_puerto2 + ContenedoresR_puerto1 



ContenedoresS_puerto1 = []
ContenedoresS_puerto2 = []
for i in range(len(ContenedoresS)):
    if(ContenedoresS[i][1]=='1'):
        ContenedoresS_puerto1.append(ContenedoresS[i][0])
    if(ContenedoresS[i][1]=='2'):
        ContenedoresS_puerto2.append(ContenedoresS[i][0])

ContenedoresS_Ambos =  ContenedoresS_puerto2 +ContenedoresS_puerto1 




#Creamos La lista de objetos celdas con las que vamos a trabajar
ListaCeldas =CreateCeldasObjects(Mapa)



ListaCeldasConEnergia = []
ListaCeldasDepurada =[]
profundidad = 0
Npila = 0

for i in range(len(ListaCeldas)):
    
    if(ListaCeldas[i][2] == 'N'):
        ListaCeldasDepurada.append((ListaCeldas[i][0],ListaCeldas[i][1]))
    if(ListaCeldas[i][2] == 'E'):
        ListaCeldasConEnergia.append((ListaCeldas[i][0],ListaCeldas[i][1]))
        ListaCeldasDepurada.append((ListaCeldas[i][0],ListaCeldas[i][1]))
    if(ListaCeldas[i][2] != 'X'):
        if(ListaCeldas[i][1] > profundidad):
            profundidad = ListaCeldas[i][1]
        if(ListaCeldas[i][0] > Npila):
            Npila = ListaCeldas[i][0]
           
        
    
if(len(ListaCeldasDepurada)< len(ListaContenedores)):
    print("Not enough cells: ",len(ListaCeldasDepurada)," for all the containers: ",len(ListaContenedores), " please change the Mapa.txt file and add more cells, or change the amount of containers")
    exit(-1)


Contenedores_Puerto1 = ContenedoresS_puerto1 + ContenedoresR_puerto1
Contenedores_Puerto2 = ContenedoresS_puerto2 + ContenedoresR_puerto2
Contenedores_Todos = Contenedores_Puerto1 + Contenedores_Puerto2

############CONSTRAINT SATISFACTION PROBLEM####################


problem= Problem()

problem.addVariables(ContenedoresS_Ambos, ListaCeldasDepurada)
problem.addVariables(ContenedoresR_Ambos, ListaCeldasConEnergia)


problem.addConstraint(AllDifferentConstraint())



def Check (*ListaContenedorez):
    i=0
    for Contenedor in ListaContenedorez:
        ListaAuxContenedores = []
        for j in range(0,Npila+1):   
             for k in range(profundidad,-1,-1):                   
                if Contenedor == (j,k):                 
                    CeldaCheck = (j,k+1)
                    if CeldaCheck in ListaCeldasDepurada:
                        ListaAuxContenedores.append(CeldaCheck)
                        if ListaAuxContenedores[0] not in ListaContenedorez:
                            return False
                        
                               
    return True                     
                                                 

problem.addConstraint(Check,Contenedores_Todos)                    
                                            
   
def PrioridadPuertos(Contenedor1, Contenedor2):
    if(Contenedor1 < Contenedor2):
        
        return True
    else:
        return False    
     

for i in range(len(Contenedores_Todos)):
    for j in range(len(Contenedores_Todos)):
        if(Contenedores_Todos[i] in Contenedores_Puerto1):
            if Contenedores_Todos[j] in Contenedores_Puerto2:
                 problem.addConstraint(PrioridadPuertos,(Contenedores_Todos[i],Contenedores_Todos[j]))
 
            





solutions = problem.getSolutions()

salida = open(sys.argv[2].replace(".txt", '')+'-'+sys.argv[3].replace(".txt",'')+".txt", 'w')
salida.write("Cantidad soluciones: "+str(len(solutions))+'\n')
for i in range(len(solutions)):
   salida.write(str(solutions[i])+'\n')



