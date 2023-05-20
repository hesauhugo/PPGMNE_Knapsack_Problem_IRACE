#!/usr/bin/env python
# coding: utf-8

# Primeiramente vamos carregar as libs "numpy" e "sys".

# In[1]:


import numpy as np
import sys


# Função para ler as instancias a partir de um endereço dado.
# 
# Parâmetro:
# 
# * fname = Nome do arquivo da instância.
# 
# Retornos:
# * Utility = Vetor c do problema ou vetor de utilidades
# * A = Matriz A do problema
# * RHS = Vetor b do problema ou RHS
# * row = número de restrições do problema ou número de linhas
# * col = número de colunas do problema ou número de objetos 

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


# Função para Calcular a Função objetivo:
# 
# Parâmetros :
# 
# * x = Vetor da solução, binário; = 1 se o objeto está na mochila; = 0 caso contrário;
# * c = Vetor c do problema, ou vetor de utilidades;
# 
# Retorno:
# 
# * Valor da Função objetivo

# In[3]:


def CalculateOF(x, c):
    return sum(c*x)


# Função para atualizar a Função objetivo para vizinhança ChangeOne:
# 
# Parâmetros:
# 
# * x = Vetor da solução, binário; = 1 se o objeto está na mochila; = 0 caso contrário;
# * c = Vetor c do problema, ou vetor de utilidades;
# * prevOF = Valor da função objetivo anterior (valor que será atualizado);
# * j = Índice do objeto que será colocado/retirado da mochila;
# 
# Retorno:
# 
# * Valor da função objetivo atualizada;
# 

# In[4]:


#Se alterar o calculo da linha 3, esta função pode ser aplicada a qualquer vizinhança.
def UpdateOF(x, c, prevOF, j):
    return prevOF + (1-x[j]) * c[j] - x[j] * c[j] 
  #Retorna: Fo anterior + valor atualizado do objeto * custo - o valor atual do objeto * o custo


# Função para verificar a factibilidade da vizinhança ChangeOne:
# 
# Parâmetros:
#     
# * a = Matriz A do problema
# * b = Vetor b do problema ou RHS
# * x = Vetor da solução, binário; = 1 se o objeto está na mochila;
# * LHS = Vetor com o valor calculado do LHS. Cada posição representa uma linha;
# * j = Índice do objeto que será colocado/retirado da mochila;
# * row = número de restrições do problema ou número de linhas;
# 
# Retorno:
# * Factibilidade do problema: true ou false

# In[5]:


#Se alterar o calculo da linha 5, esta função pode ser aplicada a qualquer vizinhança.
def IsFeasible(a, b, x, LHS, j, row):
    Feasible = True
    for i in range(row):
        aux = LHS[i] + (1 - x[j]) * a[i,j] - x[j] * a[i,j]
        # aux = Valor atual do LHS para restrição i 
        #     + valor atualizado do objeto j * custo da restrição i para objeto j
        #     - o valor atual do objeto j * o custo custo da restrição i para objeto j;
        if (aux >  b[i]):
            Feasible = False
            break
    return Feasible


# 

# Função para calcular o LHS:
# 
# Parâmetros:
#     
# * x = Vetor da solução, binário; = 1 se o objeto está na mochila;
# * a = Matriz A do problema
# * row = número de linhas ou restrições do problema;
# 
# Retorno:
# * LHS = Vetor com o valor calculado do LHS. Cada posição representa uma linha;
# 

# In[6]:


def CalculateLHS(x, a, row):
    LHS = np.zeros(row)
    for i in range(row):
        LHS[i] = sum(a[i]*x)
    return LHS 


# Função para atualizar o LHS para a vizinhança ChangeOne:
# 
# Parâmetros:
#     
# * a = Matriz A do problema
# * x = Vetor da solução, binário; = 1 se o objeto está na mochila;
# * LHS = Vetor com o valor calculado do LHS. Cada posição representa uma linha;
# * j = Índice do objeto que será colocado/retirado da mochila;
# * row = número de restrições do problema ou número de linhas;
# 
# Retorno:
# * LHS = Vetor com o valor calculado do LHS atualizado. Cada posição representa uma linha;

# In[7]:


#Se alterar o calculo da linha 4, esta função pode ser aplicada a qualquer vizinhança.
def UpdateLHS(a, x, LHS, j, row):
    for i in range(row):
        LHS[i] = LHS[i] + (1 - x[j]) * a[i,j] - x[j] * a[i,j]
    # LHS[i] = Valor atual do LHS para restrição i 
    #        + valor atualizado do objeto j * custo da restrição i para objeto j
    #        - o valor atual do objeto j * o custo custo da restrição i para objeto j;
    return LHS 


# Função para Heuristíca Construtiva: 
#   
# 
# Parâmetros:
#     
# 
# * a = Matriz A do problema
# * b = Vetor b do problema ou RHS
# * c = Vetor c do problema ou vetor de utilidades
# * row = número de restrições do problema ou número de linhas
# * col = número de colunas do problema ou número de objetos 
# 
# Retorno:
# 
# * x = Vetor da solução, binário; = 1 se o objeto está na mochila, =0 c.c.;

# In[8]:


def Greedy(a, b, c, row, col):
    x = np.zeros(col)
    cc = c.copy()
    Feasible = True
    maxIndex = 0
    LHS = CalculateLHS(x, a, row) 
    while Feasible:
        maxIndex = np.argmax(cc)
        Feasible = IsFeasible(a, b, x, LHS, maxIndex, row)
        LHS = UpdateLHS(a, x, LHS, maxIndex, row)
        x[maxIndex] = 1
        cc[maxIndex] = 0
    x[maxIndex] = 0
    return x


# Funções para atualizar a Lista Tabu para vizinhança ChangeOne:
# 
# Parâmetros:
# * tabuList = Vetor para representar a Lista Tabu;
# * j = Índice do objeto que será colocado/retirado da mochila;
# * SizeMax = Tamanho máximo da lista Tabu;
# 
# Retorno:
# 
# * tabuList = Vetor para representar a Lista Tabu atualizado;

# In[9]:


def UpdateTabuList(tabuList, j, SizeMax):
    if (len(tabuList) == SizeMax):
        del tabuList[0]
    tabuList.append(j)
    return tabuList


# Função para calcular a vizinhança ChangeOne com lista Tabu:
# 
# Parâmetros:
#     
# * x = Vetor da solução, binário; = 1 se o objeto está na mochila;
# * tabuList = Vetor para representar a Lista Tabu;
# * A = Matriz A do problema;
# * Utility = Vetor c do problema ou vetor de utilidades;
# * RHS = Vetor b do problema ou RHS;
# * row = número de restrições do problema ou número de linhas;
# * col = número de colunas do problema ou número de objeto;
# * SizeMax = Tamanho máximo da lista Tabu;
# 
# Retorno: 
# 
# * Vetor com a melhor solução, binário; = 1 se o objeto está na mochila;
# * Valor da Função Ojbetivo;
# * Vetor para representar a Lista Tabu;
# 

# In[10]:


def ChangeOneTS(x, tabuList, A, Utility, RHS, row, col, SizeMax):
    actualX = x.copy() #copy the solution to preserve the original
    bestX = x.copy()
    LHS = CalculateLHS(x, A, row)
    prevOF = CalculateOF(x, Utility)
    bestOF = 0
    bestIndex = -1
    for j in range(col):
        actualOF = UpdateOF(actualX, Utility, prevOF, j)
        if (tabuList.count(j) == 0): #Verificaça6o Lista Tabu
            if (actualOF > bestOF):
                if (IsFeasible(A, RHS, actualX, LHS, j, row)):
                    bestIndex = j
                    bestOF = actualOF
          
    if (bestIndex > -1):
        bestX = actualX.copy()
        bestX[bestIndex] = (1-actualX[bestIndex])
        tabuList = UpdateTabuList(tabuList, bestIndex, SizeMax)
        return bestX, bestOF, tabuList
    else:
        return actualX, prevOF, tabuList


# Função da busca Tabu:
# 
# Parâmetros:
# * X0 = Vetor da solução, binário; = 1 se o objeto está na mochila;
# * A = Matriz A do problema;
# * RHS = Vetor b do problema ou RHS;
# * Utility = Vetor c do problema ou vetor de utilidades;
# * row = número de restrições do problema ou número de linhas;
# * col = número de colunas do problema ou número de objeto;
# * maxItNoImprove = Número máximo de iterações sem melhoria;
# * SizeMax = Tamanho máximo da lista Tabu;
# 
# 
# Retorno:
# * Valor da Função objetivo

# In[11]:


# COLOCAR AQUI O SEU TABU SEARCH
def TabuSearch(X0, A, RHS, Utility, row, col, maxItNoImprove, SizeMax):
    actualX = X0.copy()
    bestX = X0.copy()
    actualOF = CalculateOF(bestX, Utility)
    bestOF = actualOF
    tabuList = []

    iteration = 0

    while (iteration < maxItNoImprove):
        actualX, actualOF, tabuList = ChangeOneTS(actualX, tabuList, A, Utility, RHS, row, col, SizeMax)
        if actualOF > bestOF:
            bestOF = actualOF
            bestX = actualX.copy()
            iteration = 0
        #   print("*OF: ", bestOF)  
        iteration += 1
    return bestOF


# Função para salvar os argumentos passados pelo IRACE:
# 
# Parâmetro:
# 
# * argv = Argumentos passados pelo IRACE acessados atraves do comando sys.argv 
# 
# Retorno:
# * Nome do arquivo da instância;
# * Número máximo de iterações sem melhoria;
# * Tamanho máximo da lista tabu;

# In[12]:


def GetArguments(argv):
    parameters = []

    for i, arg in enumerate(argv):
        parameters.append(arg)
      
    if(len(argv) == 5):  
        fName = parameters[2] 
        maxItNoImprove = float(parameters[4])
        SizeMax = float(parameters[6])
    else:
        fName = parameters[1] 
        maxItNoImprove = float(parameters[3])
        SizeMax = float(parameters[5])
    return fName, maxItNoImprove, SizeMax


# Função Principal:
# 

# In[13]:


def main(): 
    fName, maxItNoImprove, SizeMax = GetArguments(sys.argv)
    Utility, A, RHS, row, col  = ReadInstance(fName)  
    maxItNoImprove *= col # % do numero de variaveis
    SizeMax *= col # % do numero de variaveis
    X0 = Greedy(A, RHS, Utility, row, col)
    bestOF = - TabuSearch(X0, A, RHS, Utility, row, col, maxItNoImprove, SizeMax)
    return bestOF

if __name__ == "__main__":
    print(main())


# Vale lembrar que este código é feito especialmente para utilizar o IRACE, portanto é preciso exportá-lo para um arquivo .py em:
# 
# 
# 
# * Arquivo > Fazer download > Fazer o download de .py
# 
# Para a utilização do IRACE é recomendado a utilização de uma IDE como o VS Code:
# 
# [Download](https://code.visualstudio.com/download)
# 
# [Tutorial de como instalar o VS Code no Windows e como rodar codigo Python](https://www.youtube.com/watch?v=Z12w7PZWc2E)
# 

# In[ ]:




