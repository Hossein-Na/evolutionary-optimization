import random
import math
import normalization
# pop = population 

def creatPopulation():
    pass
    #this part depend on your self if you want you can use def create_chromosome() from initial_implementation

def objectiveFunction(population):
    #this part depend on your problem 
    pass

def sortFront(popObejectiveValue,pop):
    frontSets = []
    s = []
    i = 0
    penalty = [0] * len(popObejectiveValue)
    dominatedByMe = [[] for _ in range(len(popObejectiveValue))]

    while i < len(popObejectiveValue):
        j = 0
        dom = 0
        while j < len(popObejectiveValue):
            flag1 = True
            flag2 = True
            k = 0
            while k < len(popObejectiveValue[0]):
                if popObejectiveValue[i][k] > popObejectiveValue[j][k] :
                    flag2 = False
                elif popObejectiveValue[i][k] < popObejectiveValue[j][k] :
                    flag1 = False
                k += 1

           

            if flag1 and flag2 != True:
                penalty[i] = penalty[i] + 1
                dom = dom + 1
            elif flag2 and flag1 != True:
                dominatedByMe[i].append(j)
            j = j + 1
                
            

        if dom == 0:
            s.append(i)
            
        i = i + 1
    frontSets.append(s)
    i = 0
    while i < len(frontSets) and len(frontSets[i]) > 0:
        q = []
        j = 0
        while j < len(frontSets[i]):
            idx = frontSets[i][j]
            k = 0
            while k < len(dominatedByMe[idx]):
                dominated_idx = dominatedByMe[idx][k]
                penalty[dominated_idx] = penalty[dominated_idx] - 1
                if penalty[dominated_idx] == 0:
                    q.append(dominated_idx)
                k = k + 1
            j = j + 1

        i = i + 1
        if q:
            frontSets.append(q)
        else:
            break

    result1 = []
    result2 = []
    result = []
    for front in frontSets:
        result1.append([pop[idx] for idx in front])
        result2.append([popObejectiveValue[idx] for idx in front])
    result.append(result1)
    result.append(result2)
    return result

# you can implement any mutation you want to   
# I implement polynomial mutation  
def mutation(x,MR,lb,ub):


    a = random.random()  
    n = x.copy()
    MR = MR / 100
    delta = 0
    nm = 15
    child = []
    if a < MR :
        u = random.random()
        if u <= 0.5:
            delta = (2*u) ** (1 / (nm + 1))
        else :
            delta = 1 - ((2*(1-u)) ** (1 / (1 + nm) ))
        i = 0
        while(i<len(n)):
            n[i] += delta * (ub - lb)

        child = n

    return child
    
# you can implement any Crossover you want to 
# I implemented SBX

def crossOver(x1,x2,CR):
    Nc = 15
    CR = CR / 100

    u = random.random()     
    a = random.random() 
    arr = []
    if a < CR:    
        if u <= 0.5:
            beta = (2 * u) ** (1 / (Nc + 1))
        else:
            beta = (1 / (2 * (1 - u))) ** (1 / (Nc + 1))
        i = 0
        arr = []
        child1 = []
        child2 = []
        while i <len(x1):
            y1 = 0.5 * (((1 + beta) * x1[i]) + ((1 - beta) * x2[i]))
            y2 = 0.5 * (((1 - beta) * x1[i]) + ((1 + beta) * x2[i]))
            child1.append(y1)
            child2.append(y2)
            i = i + 1
        arr.append(child1)
        arr.append(child2)
        
    
    return arr



def associate(S, referencePo):
    
    p = [0] * len(referencePo)
    i = 0
    while i < len(S):
        t = []
        s = S[i] 
        for ref in referencePo: 
            dot = sum(s[j] * ref[j] for j in range(len(s)))
            ref_norm_sq = sum(ref[j] * ref[j] for j in range(len(ref)))
            if ref_norm_sq == 0:
                t.append(10000000000)
                continue
            factor = dot / ref_norm_sq
            proj = [factor * ref[j] for j in range(len(ref))]
            dist = math.sqrt(sum((s[j] - proj[j]) ** 2 for j in range(len(s))))
            t.append(dist)

        min_val = t[0]
        m = 0
        for j in range(1, len(t)) :
            if t[j] < min_val :
                min_val = t[j]
                m = j
        p[m] += 1
        i += 1
    
    return p  


def Niching(p,k,lastFrontS,ref,Fl):
    i = 0
    selectedS = []
    while i < k:
        q = 1000000
        j = 0
        while j < len(p) :
            if q > p[j] and sum(ref[j][l] * ref[j][l] for l in range(len(ref[0]))) != 0:
                q = p[j]
                o = j
            j = j + 1
        j = 0
        flag = 1
        min = 0
        while j < len(lastFrontS):
            dot = sum(lastFrontS[j][l] * ref[o][l] for l in range(len(lastFrontS[0])))
            ref_norm_sq = sum(ref[o][l] * ref[o][l] for l in range(len(ref[0])))
            factor = dot / ref_norm_sq
            proj = [factor * ref[o][l] for l in range(len(ref[0]))]
            
            dist = math.sqrt(sum((lastFrontS[j][l] - proj[l]) ** 2 for l in range(len(lastFrontS[0]))))
            if dist < min or flag ==1:
                flag = 0
                min = dist
                f = j        
            j = j + 1
        
        selectedS.append(Fl[f])
        lastFrontS.pop(f)
        Fl.pop(f)
        p[o] = p[o] + 1
        i = i + 1 
    

    return selectedS 


def NSGAIII(pop,numOfIteration,referencePo,CR,MR):
    n = 0
    while n < numOfIteration:

        i = 0
        Q = []
        while len(Q) < len(pop):
            ran1 = random.randint(0,len(pop) - 1)
            ran2 = random.randint(0,len(pop) - 1)
            ran3 = random.randint(0,len(pop) - 1)
            children = crossOver(pop[ran1],pop[ran2],CR).copy()
            
            if len(children) != 0 :
                child1 = children[0]
                child2 = children[1]
                Q.append(child1)
                Q.append(child2)
                i = i + 2

            child = mutation(pop[ran3],MR)
            if len(child) != 0:
                Q.append(child)
                i = i + 1


        Rt = []
        Rt.extend(pop)
        Rt.extend(Q)
        x = objectiveFunction(Rt)
        out = sortFront(x,Rt)
        front = out[0]
        frontObjValue = out[1]
        i = 0 
        j = 0
        St = [] 
        StObj = []
        while len(St) < len(pop):
            j = 0
            while j < len(front[i]):
                St.append(front[i][j])
                StObj.append(frontObjValue[i][j])
                j = j + 1 
            i = i + 1
        lastF = i - 1
        newPop = []
        newPopObj = []
        if len(St) == len(pop):
            newPop = St.copy()
            newPopObj = StObj.copy()
        else:
            i = 0
            while i < len(St) - len(front[lastF]):
                newPop.append(St[i])
                newPopObj.append(StObj[i])

                i = i + 1
            
            K = len(pop) - len(newPop)
            Fl =front[lastF].copy()
            St1 , FlO = normalization.normalize(frontObjValue,newPopObj).copy() 

            P = associate(St1,referencePo) 
            P1 = Niching(P,K,FlO,referencePo,Fl)
            newPop.extend(P1)
            pop = newPop.copy()

        n =  n + 1


    return pop

