import math
import numpy as np
import random


class wVectorn:
    def __init__(self,wVector1,solution,PBIS,decietionV):
        self.wVector1 = wVector1
        self.solution = solution
        self.neighbors = []
        self.PBIS = PBIS
        self.decietionValue = decietionV

    def setSolution(self,solution):
        self.solution = solution

    def setNeighbor(self,wVector1):
        self.neighbors.append(wVector1)

# This function depends on your problem
def objFunction(solution):
    pass

# This function depends on your problem 
def generatePop():
    pass 

#polynomial mutation  
def mutation(x, lb, ub, MR=0.1, nm=15):

    child = x.copy()
    for i in range(len(child)):
        if np.random.rand() < MR:          
            u = np.random.rand()
            if u <= 0.5:
                delta = (2 * u) ** (1 / (nm + 1)) - 1   
            else:
                delta = 1 - (2 * (1 - u)) ** (1 / (nm + 1))
            child[i] += delta * (ub[i] - lb[i])
            child[i] = np.clip(child[i], lb[i], ub[i]) 
    return child

def arithmeticCrossover(parent1, parent2, alpha=None):
    if alpha is None:
        alpha = np.random.uniform(0, 1)   
    child = alpha * parent1 + (1 - alpha) * parent2
    return child

# I implement penalty-based boundary for evaluate the solutions but you can implement the others like Tchebycheff or others
def PBI(wVector,idealP,solution, theta):
    i = 0
    wVector = np.array(wVector)
    idealP = np.array(idealP)
    solution = np.array(solution)
    lenwvector = math.sqrt(np.dot(wVector,wVector)) 
    lengthIdealPP = np.dot(wVector,idealP) / lenwvector

    lengthSP = np.dot(wVector,solution) / lenwvector

    d1 = abs(lengthSP - lengthIdealPP )

    vectorI = (np.array(wVector) / lenwvector) * lengthIdealPP
    vec1 = vectorI - idealP 
    vectorII = (np.array(wVector) / lenwvector) * lengthSP
    vec2 = vectorII - solution
    perp = vec1 - vec2
    d2 = math.sqrt(np.dot(perp, perp))

    d = d1 + theta * d2

    return d
    
def dominanceCheck(a,b):
    return np.all(a >= b) and np.any(a > b) 

def nonDomnanceSet(popValue,pop):
    EP = []
    for i in  range(len(popValue)):
        li = []
        
        for j in range(len(popValue)):
            if i != j  and dominanceCheck(popValue[j],popValue[i]):
                break
            elif j == (len(popValue) -1 ) :
                li.append(pop[i])
                li.append(popValue[i])
                EP.append(li)

    return EP


def findneighbors(wVectors, numNeighbors):
    for i in range(len(wVectors)):
        dists = [np.linalg.norm(wVectors[i].wVector1 - wVectors[j].wVector1)
                  for j in range(len(wVectors))]
        nearest = np.argsort(dists)[:numNeighbors]
        for idx in nearest:
            wVectors[i].setNeighbor(wVectors[idx])



def findIdealPoint(pop):
    i = 0
    z = pop[0].copy()
    while i < len(pop):
        j = 0
        while j < len(pop[0]):
            if pop[i][j] > z[j] :
                z[j] = pop[i][j]
            j += 1
        i += 1
    return z



def MOEA_D(pop,wVectors , numIteration, numNeighbors,CR,MR,DVLowerBounds,DVUBounds):

    wVectors = np.array(wVectors)
    pop = np.array(pop)
    EP = []
    arrWVectors = []
    popValue = []
    
    i = 0    
    while i < len(pop):
        popValue.append(objFunction(pop[i]))
        i += 1
    popValue = np.array(popValue)
    idealpoint = findIdealPoint(popValue)
    i = 0
    while i < len(wVectors):
        arrWVectors.append(wVectorn(wVectors[i],popValue[i],PBI(wVectors[i],idealpoint,popValue[i],0.7),pop[i]))
        i += 1


    EP = nonDomnanceSet(popValue,pop)
    findneighbors(arrWVectors,numNeighbors)

    i = 0  
    while i < numIteration:
        j = 0 
        while j < len(pop):
            n = np.random.randint(0 ,numNeighbors)
            m = np.random.randint(0 ,numNeighbors)
            prob = np.random.rand()
            if prob < CR :
                newSolutionDV = arithmeticCrossover(arrWVectors[j].neighbors[n].decietionValue,arrWVectors[j].neighbors[m].decietionValue)
            else:
                newSolutionDV = arrWVectors[j].neighbors[n].decietionValue.copy()

            newSolutionDV = mutation(newSolutionDV,DVLowerBounds,DVUBounds,MR)

            newSolution = objFunction(newSolutionDV)
            k = 0 
            while k < len(idealpoint):
                if idealpoint [k] < newSolution[k]:
                    idealpoint[k] = newSolution[k]
                k += 1
            k = 0 
            while k < numNeighbors:
                PBVs = PBI(arrWVectors[j].neighbors[k].wVector1,idealpoint,newSolution,0.7)
                if PBVs < arrWVectors[j].neighbors[k].PBIS:
                    arrWVectors[j].neighbors[k].PBIS = PBVs
                    arrWVectors[j].neighbors[k].solution = newSolution
                    arrWVectors[j].neighbors[k].decietionValue = newSolutionDV
                    break
                k += 1

            k = 0 
            dominated = False
            while k < len(EP) : 
                if dominanceCheck(newSolution,EP[k][1]):
                    EP.pop(k)
                    continue
                if dominanceCheck(EP[k][1] , newSolution):
                    dominated = True
                k += 1
                
            if dominated != True:
                li = [newSolutionDV,newSolution]         
                EP.append(li)

        
            j += 1

        i += 1
    return EP
                    


        
