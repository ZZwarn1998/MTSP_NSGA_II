from Node import Node
import globalManager as gm
import test as t
from nodeManager import nodeManager
from Population import Population
import random
from chromosome import chromosome
import copy
import math

class GA:

    @classmethod
    # Evolve pop
    def evolvePopulation(cls, Pi):
        Qi = Population(gm.get_value('size'))

        # Crossover
        for i in range(0, gm.get_value('size')):
            PA = cls.binaryTournamentSelection(Pi)
            PB = cls.binaryTournamentSelection(Pi)
            child1 = cls.crossover_COMBINED_HGA(PA, PB, 1)
            child2 = cls.crossover_COMBINED_HGA(PA, PB, 2)
            # child2 = cls.crossover_COMBINED_HGA(PA, PB, 2)

            Qi.saveChromosome(i, child1)
            Qi.saveChromosome(i + 1, child2)

        # Mutation
        for qi in range(Qi.sizeOfPop):
            if random.random() <= gm.get_value("MR"):
                # if random.random() <= 0.5:
                # mutachromo = cls.mutation_1(Qi.getChromosome(qi))
                mutachromo = cls.mutation_1(Qi.getChromosome(qi))
                Qi.saveChromosome(qi, mutachromo)
                # else:
                    #     mutachromo = mutation_2(Qi.getChromosome(qi))
                    #     Qi.saveChromosome(qi, mutachromo)

        # Ri = Pi U Qi
        Ri = Population(gm.get_value('size')*2)
        for i in range(gm.get_value('size')*2):
            if i < gm.get_value('size'):
                Ri.saveChromosome(i, copy.deepcopy(Pi.getChromosome(i)))
            else:
                Ri.saveChromosome(i, copy.deepcopy(Qi.getChromosome(i - 100)))

        # Fast Non Dominated Sort
        F = cls.fastNonDominatedSort(Ri)

        # the boundary set is sequentially merged into Pt+1 until |Pt+1 ∪ ri+1| is greater than |Pt|;
        Pinext = Population(gm.get_value("size"))
        sizeOfPinext = 0
        jmark = -1
        for j,Fj in enumerate(F):
            if sizeOfPinext + len(Fj) <= gm.get_value("size"):
                for index in Fj:
                    Pinext.saveChromosome(sizeOfPinext, Ri.getChromosome(index))
                    sizeOfPinext = sizeOfPinext + 1
            else:
                jmark = j
                break

        # Crowding Distance Assignment
        if jmark != -1:
            Fj = cls.crowdingDistanceAssignment(Ri,F[jmark])
            for index in Fj:
                if sizeOfPinext + 1 <= gm.get_value("size"):
                    Pinext.saveChromosome(sizeOfPinext, Ri.getChromosome(index))
                    sizeOfPinext = sizeOfPinext + 1
                else:
                    break

        return Pinext

    @classmethod
    def crowdingDistanceAssignment(cls, Ri, Fj):
        distance = [0 for i in range(0, len(Fj))]
        fitness = [Ri.getChromosome(i).getFitness() for i in Fj]
        dic = dict(zip(Fj,fitness))
        sortF = []
        for k in sorted(dic,key=dic.__getitem__):
            sortF.append(k)

        distance[0] = 4444444444444444
        distance[len(Fj) - 1] = 4444444444444444
        
        for k in range(1, len(Fj) - 1):
            distance[k] = distance[k] + (dic[sortF[k + 1]] - dic[sortF[k - 1]]) / (max(fitness) - min(fitness))
        newFj = []
        dicdis = dict(zip(sortF,distance))
        for k in sorted(dicdis,key=dicdis.__getitem__,reverse = True ):
            newFj.append(k)

        return newFj


    @classmethod
    def fastNonDominatedSort(cls, Ri):
        S = [[] for i in range(0, Ri.sizeOfPop)]
        front = [[]]
        n = [0 for i in range(0, Ri.sizeOfPop)]
        rank = [0 for i in range(0, Ri.sizeOfPop)]

        for i in range(Ri.sizeOfPop):
            S[i] = []
            n[i] = 0
            for j in range(Ri.sizeOfPop):
               if Ri.getChromosome(i).getFitness() >= Ri.getChromosome(j).getFitness():
                    if j not in S[i]:
                        S[i].append(j)
               elif Ri.getChromosome(i).getFitness() < Ri.getChromosome(j).getFitness():
                   n[i] = n[i] + 1

            if n[i] == 0:
                rank[i] = 0
                if i not in front[0]:
                    front[0].append(i)
        i = 0
        while (front[i] != []):
            Q = []
            for p in front[i]:
                for q in S[p]:
                    n[q] = n[q] - 1
                    if (n[q] == 0):
                        rank[q] = i + 1
                        if q not in Q:
                            Q.append(q)
            i = i + 1
            front.append(Q)

        del front[len(front) - 1]
        return front

    @classmethod
    def mutation_1(cls,chromo):
        newchromo = copy.deepcopy(chromo)
        p1 = newchromo.getpart1()
        p2 = sorted(random.sample(range(1, gm.get_value('n')), gm.get_value('m') - 1))
        p2.insert(0, 0)
        p2.append(len(p1))
        pairs = []
        for i in range(len(p2) - 1 ):
            start = p2[i]
            end = p2[i + 1]
            pairs.append([start, end])

        random.shuffle(pairs)

        mutap1 = []
        mutap2 = sorted(random.sample(range(1, gm.get_value('n')), gm.get_value('m') - 1))
        for pair in pairs:
            start = pair[0]
            end = pair[1]
            mutap1.extend(p1[start:end ])

        mutachromo = chromosome(mutap1, mutap2)

        return mutachromo

    @classmethod
    def binaryTournamentSelection(cls, pop):
        tSize = gm.get_value("tournamentsize")
        tournament = Population(tSize)

        for index in range(tSize):
            randomInt = random.randint(0, pop.sizeOfPop)
            tournament.saveChromosome(index, pop.getChromosome(randomInt))

        best = tournament.getBestChromosome()
        return best

    @classmethod
    def crossover_COMBINED_HGA(cls ,PA,PB, method):
        if method == 1:
            pa1 = PA.getpart1()
            pa2 = PA.getpart2()
            pb1 = PB.getpart1()
            pb2 = PB.getpart2()
            MARK = "latter"
            child = cls.crossover_1(pa1, pa2, pb1, pb2, MARK)
        else:
            decodePA = PA.getdecode()
            decodePB = PB.getdecode()
            MARK = "latter"
            childbefore = cls.crossover_2(decodePA, decodePB, MARK)
            child = cls.rationalization(childbefore)
        return child

    @classmethod
    def crossover_1(cls, pa1, pa2, pb1, pb2, MARK):
        x = -1
        y = -1
        childp1 = []
        childp2 = []
        length = len(pa1)
        k = random.randint(1, gm.get_value("n") - 1)
        childp1.append(k)
        while (length > 1):
            if MARK == "latter":
                # print(pa1,k)
                if pa1.index(k) == len(pa1) - 1:
                    x = pa1[0]
                else:
                    x = pa1[pa1.index(k) + 1]
                if pb1.index(k) == len(pa1) - 1:
                    y = pb1[0]
                else:
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

        child = chromosome(childp1,childp2)
        return child

    @classmethod
    def crossover_2(cls, pa1, pb1, MARK):
        x = -1
        y = -1
        childseq = []

        length = len(pa1)
        k = random.randint(1, gm.get_value("n") - 1)
        childseq.append(k)
        while (length > 1):
            if MARK == "latter":
                if pa1.index(k) == len(pa1) - 1:
                    x = pa1[0]
                else:
                    x = pa1[pa1.index(k) + 1]
                if pb1.index(k) == len(pa1) - 1:
                    y = pb1[0]
                else:
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
            childseq.append(k)
            length = len(pa1)

        return childseq

    @classmethod
    def rationalization(cls, child):
        # Locate the first zero
        indexOfFirstZero = child.index(0)

        # Rationalization
        step = indexOfFirstZero
        copychild = copy.deepcopy(child)
        p1 = []
        p2 = []

        # [ ... 0(First) ... ] ---> [0(First) ... ]
        for i in range(step):
            copychild.insert(len(copychild), copychild[0])
            copychild.remove(copychild[0])

        # [0 ... 0 ... 0 ... 0 ... 0 ... ]
        # [0 ... 00 ... 00 ... ]
        # [000 ... 0 ... 0 ... ]

        seq = copy.deepcopy(copychild)
        loc = []
        subseq = []
        subseqlen = []
        start = 0
        end = len(seq)
        cnt = 0

        # while (0 in seq[start + 1:end]):
        #     try:
        #         loc.append(seq.index(0, start + 1, end))
        #         start = child.index(0, start + 1, end)
        #     except ValueError:
        #         print("break!")

        while 0 in seq[start :end]:
            try:
                # print(start, end)
                loc.append(seq.index(0, start, end))
                start = seq.index(0, start, end) + 1

            except ValueError:
                # start = len(seq)
                print("there is no zero.")
                break

        # loc.insert(0,0)
        loc.insert(len(seq),len(seq))

        for i in range(0, len(loc) - 1):
            s = copy.deepcopy(seq[loc[i]+1:loc[i+1]])
            subseqlen.append(len(s))
            subseq.append(s)

        while 0 in seq:
            seq.remove(0)

        if 0 in subseqlen:
            for l in subseqlen:
                if l == 0:
                   cnt = cnt + 1
            for index,l in enumerate(subseqlen):
                if l > cnt:
                   subseqlen[index] = l - cnt
                elif l == 0 :
                   subseqlen[index] = 1
            sum = subseqlen[0]
            for i in subseqlen[1:len(subseqlen)]:
                p2.append(sum)
                sum = sum + i
            p1 = seq
        else:
            p1 = seq
            p2 = loc[1:len(loc)-1]
        '''
                if cls.judgeIfRationalized(copychild):
                    # Sequence has been rationalized
                    numBehindZero = []
                    for index in range(1, len(copychild) - 1):
                        if copychild[index] == 0:
                            numBehindZero.append(copychild[index + 1])

                    while 0 in copychild:
                        copychild.remove(0)
                    p1 = copy.deepcopy(copychild)
                    for num in numBehindZero:
                        p2.append(copychild.index(num))
                    # print("p1", p1)
                    # print("p2", p2)
                    child = chromosome(p1, p2)
                    return child

                else:

                        # 这里与论文内容不符合

                    # while (0 in copychild):
                    #     copychild.remove(0)
                    # p1 = copy.deepcopy(copychild)
                    # p2 = sorted(random.sample(range(1, gm.get_value('n')), gm.get_value('m') - 1))


                    child = chromosome(p1, p2)
                '''


        child = chromosome(p1, p2)
        return child



    @classmethod
    def judgeIfRationalized(cls, child):
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
        # print(lSubf)

        if 1 in lSubf:
            return False
        else:
            return True