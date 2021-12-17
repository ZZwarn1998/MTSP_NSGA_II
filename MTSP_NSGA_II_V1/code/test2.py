'''
just for testing
'''

import copy
import random
from Node import Node
import globalManager as gm
import test as t
from nodeManager import nodeManager
from Population import Population
import random
from chromosome import chromosome

def crossover_COMBINED_HGA( PA, PB, method, MARK):

    childp1 = []
    childp2 = []

    if method == 1:
        pa1 = PA.getpart1()
        pa2 = PA.getpart2()
        pb1 = PB.getpart1()
        pb2 = PB.getpart2()
        childp1, childp2 = crossover_1(pa1, pa2, pb1, pb2, MARK)
        print("1childp1",childp1)
        print("1childp2",childp2)
        child = chromosome(childp1, childp2)
    else:
        decodePA = PA.getdecode()
        decodePB = PB.getdecode()
        childbefore = crossover_2(decodePA, decodePB, MARK)
        print("#",childbefore)
        child = rationalization(childbefore)
        print("2childp1",childp1)
        print("2childp2",childp2)


    return child

def crossover_1(pa1, pa2, pb1, pb2, MARK):
    x = -1
    y = -1
    childp1 = []
    childp2 = []
    length = len(pa1)
    k = random.randint(1, length)
    childp1.append(k)
    while (length > 1):
        if MARK == "latter":
            x = pa1[pa1.index(k) + 1]
            y = pb1[pb1.index(k) + 1]
        elif MARK == "former":
            if pa1.index(k) == 0:
                x = pa1[-1]
            else:
                x = pa1[pa1.index(k) - 1]
            if pb1.index(k) == 0:
                y = pb1[-1]
            else:
                y = pb1[pb1.index(k) - 1]
        pa1.remove(k)
        pb1.remove(k)

        nodek = nodeManager.getNode(k)
        nodex = nodeManager.getNode(x)
        nodey = nodeManager.getNode(y)
        dx = nodek.distance_to(nodex)
        dy = nodek.distance_to(nodey)
        if dx < dy:
            k = x
        else:
            k = y
        childp1.append(k)
        length = len(pa1)
    if random.random() > 0.5:
        childp2 = copy.deepcopy(pa2)
    else:
        childp2 = copy.deepcopy(pb2)
    return childp1, childp2

def crossover_2(pa1, pb1, MARK):
    x = -1
    y = -1
    child = []

    length = gm.get_value("n")
    k = random.randint(1, length)
    child.append(k)
    while (length > 1):
        if MARK == "latter":
            x = pa1[pa1.index(k) + 1]
            y = pb1[pb1.index(k) + 1]
        elif MARK == "former":
            if pa1.index(k) == 0:
                x = pa1[-1]
            else:
                x = pa1[pa1.index(k) - 1]
            if pb1.index(k) == 0:
                y = pb1[-1]
            else:
                y = pb1[pb1.index(k) - 1]
        pa1.remove(k)
        pb1.remove(k)

        nodek = nodeManager.getNode(k)
        nodex = nodeManager.getNode(x)
        nodey = nodeManager.getNode(y)
        dx = nodek.distance_to(nodex)
        dy = nodek.distance_to(nodey)
        if dx < dy:
            k = x
        else:
            k = y
        child.append(k)
        length = len(pa1)

    return child

def rationalization(child):
    indexOfFirstZero = child.index(0)
    step = indexOfFirstZero
    copychild = copy.deepcopy(child)
    p1 = []
    p2 = []
    for i in range(step):
        copychild.insert(len(copychild),copychild[0])
        copychild.remove(copychild[0])
    # print(copychild)
    if judgeIfRationalized(copychild):

        numBehindZero = []
        # print(copychild)
        for index in range(1,len(copychild) -  1):
            if copychild[index] == 0 :
                numBehindZero.append(copychild[index + 1])
        while 0 in copychild:
            copychild.remove(0)
        p1 = copy.deepcopy(copychild)
        for num in numBehindZero:
            p2.append(copychild.index(num))
        print("p1",p1)
        print("p2",p2)
        child = chromosome(p1, p2)
        return child

    else:
        while(0 in copychild):
            copychild.remove(0)
        p1 = copy.deepcopy(copychild)
        p2 = sorted(random.sample(range(1, gm.get_value('n')), gm.get_value('m')-1))
        print("#p1", p1)
        print("#p2",p2)
        child = chromosome(p1, p2)
        return child



def judgeIfRationalized(child):
    indexOfZeroLis = [0]
    start = 0
    end = len(child)
    while(0 in child[start + 1:end]):
        try:
            indexOfZeroLis.append(child.index(0, start + 1, end))
            start = child.index(0, start + 1, end)
        except ValueError:
            print("break!")
    indexOfZeroLis.append(len(child))
    lSubf = []
    for i in range(0, len(indexOfZeroLis) - 1):
        lSubf.append(indexOfZeroLis[i+1] - indexOfZeroLis[i])
    print(lSubf)

    if 1 in lSubf:
        return False
    else:
        return True



# def recode(child):
#
#     return childp1,childp2

if __name__ =="__main__":
    # total = 10
    # n = 2
    # dividers = sorted(random.sample(range(1, total), n))
    # print(dividers)
    # lis = [ i for i in range(0,100,2)]
    # print(lis)
    # print( [a - b for a, b in zip(dividers + [total], [0] + dividers)])
    # child = [1,2,0,3,4,0,5,6]
    chromosome1 =chromosome()
    chromosome2 = chromosome()
    # rationalization(child)


