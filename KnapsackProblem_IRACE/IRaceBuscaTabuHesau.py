#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from numpy.random import seed
from numpy.random import randint
import time
import sys


# In[2]:


def ReadInstance(Fname):
    with open(Fname) as f:
    
        row = [int(x) for x in next(f).split()] # read first line
        empty = [int(x) for x in next(f).split()] # read next line
        col = [int(x) for x in next(f).split()] # read next line
        empty = [int(x) for x in next(f).split()] # read next line
        empty = [int(x) for x in next(f).split()] # read next line

        Utility = []
        Utility.append([float(x) for x in next(f).split()])

        Utility =Utility[0]

        empty = [int(x) for x in next(f).split()] # read next line

        A = []
        count = 0
        while count < row[0]: # read rest of lines
            A.append([float(x) for x in next(f).split()])
            count = count + 1
    
        empty = [int(x) for x in next(f).split()] # read next line

        RHS = []
        RHS.append([float(x) for x in next(f).split()])
        RHS =RHS[0]

    RHS = np.array(RHS)
    A = np.array(A)
    Utility = np.array(Utility)
    row, col = A.shape
    
    return Utility, A, RHS, row, col


# In[3]:


def RetornarValorDaFuncaoObj(x, u,col):
    total=0
    for j in range(col):
        total= total + (x[j]*u[j])
    return total 


# In[4]:


def EViavel(a, x, b,row,col):
    eviavel= True 
    for i in range(row):
        total=0
        for j in range(col):
            total= total + (a[i,j]*x[j])
        if total> b[i]:
            eviavel= False 
            break 
    return eviavel


# In[5]:


def HeuristicaGulosa(a,b,c,x,row,col):
    cc = c.copy()
    xx = x.copy() 
    Viavel = True
    maxIndex  = 0
    while Viavel:
        maxIndex = np.argmax(cc)
        xx[maxIndex] = 1
        cc[maxIndex] = 0 
        Viavel = EViavel(a,xx,b,row,col)
    xx[maxIndex] = 0
    return xx


# In[6]:


def BuscaTabu(tempo,T,x, A, RHS, cols, rows, c):
    ini = time.time()
    achouT = time.time()
    
    melhorFO = RetornarValorDaFuncaoObj(c,x)
    melhorx= x.copy()
    vetorITabu = []
    vetorJTabu = []
    vetorJMaisTabu = []

    while True:
        jLinha=-1
        iLinha=-1
        JMaislinha = -1
        melhorFOtabu=-1
        melhorxtabu=[]
        
        jLinhaSemMelhoria = -1
        iLinhaSemMelhoria = -1
        JMaislinhaSemMelhoria = -1
        melhorFOtabuSemMelhoria = -1
        melhorxtabuSemMelhoria=[]
        
        for i in range(cols):
            j = i+1

            while j < cols-1:
                xx = melhorx.copy()
                indiceTabu= -1
                usouCriterioAspiracao= False
            
                for k in range(len(vetorITabu)):
                    if vetorITabu[k]==i and vetorJTabu[k]==j and  vetorJMaisTabu[k]==j+1:
                        indiceTabu=k
            
                if indiceTabu==-1:
                    xx[i],xx[j],xx[j+1]= 1-xx[i], 1-xx[j],1-xx[j+1]
                    #FOLinha= RetornarValorDaFuncaoObj(c, xx)
                    FOLinha = melhorFO
                    if melhorx[i] == xx[i] and melhorx[j] == xx[j] and melhorx[j+1] == xx[j+1]:
                        j=j+1
                        continue
                    else:
                        if xx[i]==1 :
                            FOLinha = FOLinha + c[i]
                        else:
                            FOLinha = FOLinha - c[i]      
                        if xx[j]==1 :
                            FOLinha = FOLinha + c[j]
                        else:
                            FOLinha = FOLinha - c[j]      
                        if xx[j+1]==1 :
                            FOLinha = FOLinha + c[j+1]
                        else:
                            FOLinha = FOLinha - c[j+1]      
                    
                    if FOLinha > melhorFOtabu: 
                        if EViavel(A,xx,RHS):
                            melhorxtabu= xx.copy()
                            melhorFOtabu= FOLinha
                            jLinha=j
                            iLinha=i
                            JMaislinha = j+1
                    elif EViavel(A,xx,RHS):
                        if FOLinha > melhorFOtabuSemMelhoria:
                            melhorxtabuSemMelhoria= xx.copy()
                            melhorFOtabuSemMelhoria= FOLinha
                            jLinhaSemMelhoria=j
                            iLinhaSemMelhoria=i
                            JMaislinhaSemMelhoria = j+1

                else:

                    xx[i],xx[j],xx[j+1]= 1-xx[i], 1-xx[j],1-xx[j+1]
                    #FOLinha= RetornarValorDaFuncaoObj(c, xx)
                    FOLinha = melhorFO
                    if melhorx[i] == xx[i] and melhorx[j] == xx[j] and melhorx[j+1] == xx[j+1]:
                        j=j+1
                        continue
                    else:
                        if xx[i]==1 :
                            FOLinha = FOLinha + c[i]
                        else:
                            FOLinha = FOLinha - c[i]      
                        if xx[j]==1 :
                            FOLinha = FOLinha + c[j]
                        else:
                            FOLinha = FOLinha - c[j]      
                        if xx[j+1]==1 :
                            FOLinha = FOLinha + c[j+1]
                        else:
                            FOLinha = FOLinha - c[j+1]      
                    if FOLinha > melhorFO: 
                        if EViavel(A,xx,RHS):
                            melhorxtabu= xx.copy()
                            melhorFOtabu= FOLinha
                            jLinha=j
                            iLinha=i
                            JMaislinha = j+1
                            usouCriterioAspiracao= True
                j=j+1                            

        if iLinha != -1:
            if(usouCriterioAspiracao == False): 
                vetorITabu.append(iLinha) 
                vetorJTabu.append(jLinha) 
                vetorJMaisTabu.append(JMaislinha) 
                achouT = time.time()

                if len(vetorITabu) > T:
                    vetorITabu=vetorITabu[(1):]
                    vetorJTabu=vetorJTabu[(1):]
                    vetorJMaisTabu=vetorJMaisTabu[(1):]
        else:
            vetorITabu.append(iLinhaSemMelhoria) 
            vetorJTabu.append(jLinhaSemMelhoria) 
            vetorJMaisTabu.append(JMaislinhaSemMelhoria) 
            achouT = time.time()
                
            if len(vetorITabu) > T:
                vetorITabu=vetorITabu[(1):]
                vetorJTabu=vetorJTabu[(1):]
                vetorJMaisTabu=vetorJMaisTabu[(1):]

        if melhorFOtabu> melhorFO:
            melhorFO = melhorFOtabu
            melhorx = melhorxtabu
            achouT = time.time()

        fim = time.time()
        if fim <= (ini+tempo):
            continue
        else: 
            break
        #(achouT-ini)    
    return melhorFO,melhorx


# In[7]:


def GetArguments(argv):
    parameters = []

    for i, arg in enumerate(argv):
        parameters.append(arg)
      
    if(len(argv) == 5):  
        fName = parameters[2] 
        tempo = float(parameters[4])
        SizeMax = float(parameters[6])
    else:
        fName = parameters[1] 
        tempo = float(parameters[3])
        SizeMax = float(parameters[5])
    return fName, tempo, SizeMax


# In[8]:


def main(): 
    fName, tempo, T = GetArguments(sys.argv)
    Utility, A, RHS, row, col  = ReadInstance(fName)  
    tempo *= 100 # % do numero de variaveis
    T *= col # % do numero de variaveis
    x = np.zeros(col) 
    x= HeuristicaGulosa(A,RHS,Utility,x,row,col)
    bestOF = - BuscaTabu(tempo,T,x, A, RHS, col, row, Utility)
    return bestOF

if __name__ == "__main__":
    print(main())

