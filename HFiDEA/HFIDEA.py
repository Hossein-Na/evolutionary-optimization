import numpy as np
import math


class refereneV:
    def __init__(self,ref):
        self.ref = ref
        self.associateS = []
        self.associateDV = []
        self.distances = []
        self.pS = []
        self.pDV = []
        self.qS = []
        self.qDV = []
                

def objFunction():
    pass

def generateInitialSolutions():
    pass
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




def checkDominatesd(a,b):
    return np.all(a <= b) and np.any(a < b)
    
def lhfDominate(a, b, weights, minimize=True):
    beta = np.array(a, dtype=float)
    alpha = np.array(b, dtype=float)
    w = np.array(weights, dtype=float)

    if minimize:
        better = beta < alpha   
        worse = beta > alpha    
    else:
        better = beta > alpha
        worse = beta < alpha

    n_b_beta = np.sum(better) 
    n_b_alpha = np.sum(worse) 

    condition_1 = n_b_beta > n_b_alpha
    if not condition_1:
        return False

    w_safe = np.where(w == 0, 1e-10, w)
    
    delta_F = np.sum((beta - alpha) / w_safe)

    condition_2 = delta_F < 0

    return condition_2


def selectEnvironment(pop,referenceVectors,F):
    S = []
    SD = []
    D = []
    min = math.inf
    pop = np.array(pop)
    F = np.array(F)
    i = 0 
    while i < len(F):
        x = F[i]
        disL = []
        min = math.inf
        for ref in referenceVectors:
            n = np.dot(ref.ref,x)
            m = np.dot(ref.ref,ref.ref)
            projX = (n / m) *  ref.ref
            distance = math.sqrt(np.dot(x -projX,x -projX))
            disL.append(distance)
            if min > distance:
                associatdV = ref
                min =distance
        associatdV.associateS.append(x)
        associatdV.distances.append(min)
        associatdV.associateDV.append(pop[i])
        D.append(disL)
        i += 1
    f = 0
    while f < len(referenceVectors):

        if (len(referenceVectors[f].associateS) > 0 ):
            solutions = referenceVectors[f].associateS.copy()
            DValues = referenceVectors[f].associateDV.copy()
            distanceS = referenceVectors[f].distances.copy()
            if len(solutions) > 0:
                i = 0 
                while i < len(solutions):
                    j = 0
                    flag = True
                    while j  < len(solutions):
                        if checkDominatesd (solutions[j],solutions[i]):
                            solutions.pop(i)
                            distanceS.pop(i)
                            DValues.pop(i)
                            flag = False
                            break
                        j += 1
                    if flag:
                        i += 1
            min = math.inf
            i = 0
            selectedsolution = np.array([])
            while i < len(solutions):
                if min > distanceS[i]:
                    selectedsolution = solutions[i]
                    min = distanceS[i]
                i += 1
            g = []
            min = math.inf
            i = 0
            solution = []
            decietionV = []
            while i < len(solutions):
                if lhfDominate(solutions[i],selectedsolution):
                    g.append(solutions[i])
                    if distanceS [i] < min:
                        min = distanceS[i]
                        solution = solutions[i]
                        decietionV = DValues[i]
                i += 1

            if len(g) > 0:
                selectedsolution = solution

            S.append(selectedsolution)
            SD.append(decietionV)
            referenceVectors.pop(f)      
            mask = np.all(F == selectedsolution , axis = 1)
            F = F[~mask]
            mask = np.all(pop == decietionV , axis = 1)
            pop = pop[~mask]
        else :
            f += 1

    for ref in referenceVectors:
        z = 0
        min = math.inf
        selectedsolution = []
        selectedDV = []
        while z < len(F):
            x = F[z]
            n = np.dot(ref.ref,x)
            m = np.dot(ref.ref,ref.ref)
            projX = (n / m) *  ref.ref
            distance = math.sqrt(np.dot(x -projX,x -projX))
            if min > distance:
                selectedsolution = x
                selectedDV = pop[z]
                min = distance
            
            z += 1

        S.append(selectedsolution)
        SD.append(selectedDV)

    return S,SD

    
            
def checkStabalization(p,q,pObjV,qObjV,refs,psi,history):
    c =False
    c = False
    Np = psi[0]
    Ns = psi[1]
    i = 0 
    while i < len(p):
        x = pObjV[i]
        min = math.inf
        for ref in refs:
            n = np.dot(ref.ref,x)
            m = np.dot(ref.ref,ref.ref)
            projX = (n / m) *  ref.ref
            distance = math.sqrt(np.dot(x -projX,x -projX))
            if min > distance:
                associatdV = ref
                min = distance
        associatdV.pS.append(x)
        associatdV.pDV.append(p[i])
        i += 1
    i = 0
    while i < len(q):
        x = qObjV[i]
        min = math.inf
        for ref in refs:
            n = np.dot(ref.ref,x)
            m = np.dot(ref.ref,ref.ref)
            projX = (n / m) *  ref.ref
            distance = math.sqrt(np.dot(x -projX,x -projX))
            if min > distance:
                associatdV = ref
                min =distance
        associatdV.pS.append(x)
        associatdV.pDV.append(q[i])
        i += 1

    muD = 0
    zA = 0

    for reference in refs:
        if len(reference.ps) > 0 and len(reference.qs) > 0:
            sumP = np.sum(ref.ps, axis=0) 
            sumQ = np.sum(ref.qs, axis=0)

            barP = sumP / len(ref.ps)
            barQ = sumQ / len(ref.qs)

            D_z = np.linalg.norm(barP - barQ)

            muDt += D_z
            zA += 1
        else:
            muD += 1.0
            zA += 1

        if zA > 0:
            muD_t = muD_t / zA
        else:
            muD_t = 1.0  


        if 'muD' not in history:
            history['muD'] = []
            history['D'] = []
            history['S'] = []

        history['muD'].append(muD_t)
        mu_t = np.mean(history['muD'])
        sigma_t = np.std(history['muD'])

        D_t = round(mu_t, Np)
        S_t = round(sigma_t, Np)

        history['D'].append(D_t)
        history['S'].append(S_t)

        c1 = False
        c2 = False

        if len(history['D']) >= Ns + 1:
            last_D = history['D'][-(Ns + 1):]  
            last_S = history['S'][-(Ns + 1):]  

            all_D_equal = True
            idx = 0
            while idx < len(last_D):
                if last_D[idx] != D_t:
                    all_D_equal = False
                    break
                idx += 1

            if all_D_equal:
                c1 = True

            all_S_equal = True
            idx = 0
            while idx < len(last_S):
                if last_S[idx] != S_t:
                    all_S_equal = False
                    break
                idx += 1

            if all_S_equal:
                c2 = True

        stabilized = (c1 and c2)

    return stabilized, history


#As the Investigating the Normalization Procedure of NSGA-III from DR.Deb mentioned the problems of finding hyperplane i implement the solution that they proposed at there  
def updateNadirP(pop):
    eps = 1e-4
    extremePoints = []
    extremePoint = [] 
    nadirP = [- math.inf] * len(pop[0])
    i = 0
    while i < len(pop[0]):
        min = math.inf
        for x in pop:
            j = 0
            while j < len(x):
                if j != i :
                    if min > x[j]:
                        min = x[j] 
                        extremePoint = x
                j += 1
        extremePoints.append(extremePoint)
        i = i + 1

    flag = True
    extremePoints = np.array(extremePoints)
    rankExtreme = np.linalg.matrix_rank(extremePoints)
    numOfRow = extremePoints.shape[0]
    i = 0
    while i < len(extremePoints):
        if extremePoints[i][i] < eps:
            flag = False
            
    if rankExtreme < numOfRow:
        flag = False

    if flag:
        ones = np.ones(extremePoints.shape[0])
        coefficients = np.linalg.solve(extremePoints, ones)
        if np.any(np.isclose(coefficients, 0)):
            print("One or more coefficients are zero. The hyperplane is parallel to an axis.")
            flag = False
        else :
            intercepts = 1.0 / coefficients
            if np.all(intercepts > 0):
                nadirP = intercepts
            else :
                flag = False    

    if flag == False:
        flag1 = 1 
        j = 0
        while j < len(pop) :
            k = 0
            while k < len(nadirP):
                if nadirP[k] < pop[i][j][k] or flag1 == 1:
                    nadirP[k] = pop[i][j][k]
            flag1 = 0
            j += 1

    return nadirP


def HFIDEA(N,pop,refs,uf,t,CR,MR,LB,UB,psiN,psiTM):
    ZNadir = []
    history = []
    historyTM = []
    i = 0
    while i < t:


        j = 0 
        Q = []
        while j < len(pop):
            n = np.random.randint(0 ,len(pop))
            m = np.random.randint(0 ,len(pop))
            prob = np.random.rand()
            if prob < CR :
                newSolutionDV = arithmeticCrossover(pop[n],pop[m])
            else:
                newSolutionDV = pop[n].copy()

            newSolutionDV = mutation(newSolutionDV,LB,UB,MR)
            Q.append(newSolutionDV)
            j += 1

        Rt = []
        Rt.extend(pop)
        Rt.extend(Q)
        F = []
        j = 0 
        while j < len(Rt):
            F.append(objFunction(Rt[j]))
            j += 1
        k = 0
        ZIdealP =[] 
        while k < len(F[0]):
            j =0 
            min = math.inf
            while j < len(F):
                if min > F[j][k]:
                    min = F[j][k]
                j += 1
            ZIdealP.apppend(min)
            k += 1

        ZNadir = updateNadirP(F)
        if len(ZNadir) > 0 :
            k = 0 
            while k < len(F):
                l = 0
                while l < len(F[0]):
                    F[k][l] =( F[k][l] - ZIdealP[l]) / (ZNadir[l] - ZIdealP[l])
                l += 1 
            k += 1

        else:
            k = 0
            while k < len(F):
                l = 0 
                while l < len(F[0]):
                    F[k][l] = F[k][l] - ZIdealP[k]
                    l += 1
                k += 1
        pF = F[:len(pop)]
        newPopF,newPop = selectEnvironment(Rt,refs,F)
        Cn , history = checkStabalization(pop,newPop,pF,newPopF,refs,psiN,history)
        Ctm = False

        if Cn :
            ZNadir = updateNadirP(newPopF)
        if uf :
            Ctm,histotryTM = checkStabalization(pop,newPop,pF,newPopF,refs,psiTM,historyTM) 

        pop = newPop
        i += 1
        if Ctm :
            break




