import copy
import time
import globalManager as gm
from nodeManager import nodeManager as nm
from chromosome import Chromosome
import random
import math


class GA:
    
    @classmethod

    def start(cls, Pi):
        print("START!")
        start_time = time.time()
        best_chromo = []
        minfun1val_per_round = []
        minfun2val_per_round = []

        for i in range(gm.get_value("gene")):

            # Obtain current best chromosome
            f1val = [cls.fun1(chromo) for chromo in Pi]
            f2val = [cls.fun2(chromo) for chromo in Pi]
            non_dominated_sorted_solution = cls.fast_non_dominated_sort(f1val[:], f2val[:])
            best_chromo = [Pi[i] for i in non_dominated_sorted_solution[0]]

            # Record current minimal value of function1 and function2
            minfun1val_per_round.append(min(cls.fun1(chromo) for chromo in best_chromo))
            minfun2val_per_round.append(min(cls.fun2(chromo) for chromo in best_chromo))

            # Calculate crowding distance values
            crowding_distance_values = []
            for i in range(0, len(non_dominated_sorted_solution)):
                crowding_distance_values.append(cls.crowding_distance(f1val[:], f2val[:],non_dominated_sorted_solution[i][:]))

            # Add Qi to Ri (Ri = Pi U Qi)
            Ri = Pi[:]
            while len(Ri) != 2 * gm.get_value("popSize"):
                a1 = random.randint(0, gm.get_value("popSize") - 1)
                b1 = random.randint(0, gm.get_value("popSize") - 1)
                Ri.append(cls.generateChild(Pi[a1], Pi[b1]))

            # Fast non-dominated sort
            f1val2 = [cls.fun1(Ri[i]) for i in range(0, 2 * gm.get_value("popSize"))]
            f2val2 = [cls.fun2(Ri[i]) for i in range(0, 2 * gm.get_value("popSize"))]
            non_dominated_sorted_Ri = cls.fast_non_dominated_sort(f1val2[:], f2val2[:])

            # Calculate crowding distance values
            crowding_distance_values2 = []
            for i in range(0, len(non_dominated_sorted_Ri)):
                crowding_distance_values2.append( cls.crowding_distance(f1val2[:], f2val2[:], non_dominated_sorted_Ri[i][:]))

            # Generate new Pi
            indexOfPnext = []
            for i in range(0, len(non_dominated_sorted_Ri)):
                non_dominated_sorted_Ri_1 = [
                    cls.findindex(non_dominated_sorted_Ri[i][j], non_dominated_sorted_Ri[i])
                    for j in range(0, len(non_dominated_sorted_Ri[i]))
                ]
                front22 = cls.sort_by_val(
                    non_dominated_sorted_Ri_1[:], crowding_distance_values2[i][:]
                )
                front = [
                    non_dominated_sorted_Ri[i][front22[j]]
                    for j in range(0, len(non_dominated_sorted_Ri[i]))
                ]
                front.reverse()
                
                for value in front:
                    indexOfPnext.append(value)
                    if len(indexOfPnext) == gm.get_value("popSize"):
                        break
                if len(indexOfPnext) == gm.get_value("popSize"):
                    break

            Pi = [Ri[i] for i in indexOfPnext]

        end_time = time.time()
        runtime = end_time- start_time

        f1valbest = [cls.fun1(chromo) for chromo in best_chromo]
        f2valbest = [cls.fun2(chromo) for chromo in best_chromo]
        number = len(best_chromo)

        return runtime, best_chromo, f1valbest, f2valbest, number, minfun1val_per_round, minfun2val_per_round

    @classmethod
    def fun1(cls, chromo):
        totaldis = 0

        decode = cls.decode(chromo.getPart1(),chromo.getPart2())
        decode.append(0)
        preindex = 0
        for index in decode:
            totaldis += cls.calDistance(preindex, index)
            preindex = index

        return totaldis

    @classmethod
    def fun2(cls, chromo):
        totaldis = 0
        preindex = 0
        salesmendis = []

        decode = cls.decode(chromo.getPart1(), chromo.getPart2())
        decode.append(0)

        for index in decode:
            totaldis += cls.calDistance(preindex, index)
            preindex = index
            if index == 0:
                salesmendis.append(totaldis)
                totaldis = 0

        return max(salesmendis) - min(salesmendis)

    @classmethod
    def decode(cls, p1, p2):
        offset = 0
        for x in p2:
            p1.insert(x + offset, 0)
            offset += 1
        return p1

    @classmethod
    def calDistance(cls, fromindex, toindex):
        nodefrom = nm.getNode(fromindex)
        nodeto = nm.getNode(toindex)
        return nodefrom.distance_to(nodeto)
    
    @classmethod
    def fast_non_dominated_sort(cls, f1val, f2val):
        S = [[] for i in range(0, len(f1val))]
        front = [[]]
        n = [0 for i in range(0, len(f1val))]
        rank = [0 for i in range(0, len(f1val))]

        for p in range(0, len(f1val)):
            S[p] = []
            n[p] = 0
            for q in range(0, len(f1val)):
                if (
                        (f1val[p] > f1val[q] and f2val[p] > f2val[q])
                        or (f1val[p] >= f1val[q] and f2val[p] > f2val[q])
                        or (f1val[p] > f1val[q] and f2val[p] >= f2val[q])
                ):
                    if q not in S[p]:
                        S[p].append(q)
                elif (
                        (f1val[q] > f1val[p] and f2val[q] > f2val[p])
                        or (f1val[q] >= f1val[p] and f2val[q] > f2val[p])
                        or (f1val[q] > f1val[p] and f2val[q] >= f2val[p])
                ):
                    n[p] = n[p] + 1
            if n[p] == 0:
                rank[p] = 0
                if p not in front[0]:
                    front[0].append(p)

        i = 0
        while front[i] != []:
            Q = []
            for p in front[i]:
                for q in S[p]:
                    n[q] = n[q] - 1
                    if n[q] == 0:
                        rank[q] = i + 1
                        if q not in Q:
                            Q.append(q)
            i = i + 1
            front.append(Q)

        del front[len(front) - 1]

        front.reverse()
        return front
    
    @classmethod
    def crowding_distance(cls, f1val, f2val, front):
        distance = [0 for i in range(0, len(front))]
        sorted1 = cls.sort_by_val(front, f1val[:])
        sorted2 = cls.sort_by_val(front, f2val[:])
        distance[0] = math.inf
        distance[len(front) - 1] = math.inf
        # print(f1val)
        # print(f2val)
        flag = (not math.isclose(max(f1val), min(f1val), rel_tol=1e-5)) and \
               (not math.isclose(max(f2val), min(f2val), rel_tol=1e-5))

        for k in range(1, len(front) - 1):
            if flag:
                distance[k] = distance[k] + (
                        f1val[sorted1[k + 1]] - f2val[sorted1[k - 1]]
                ) / (max(f1val) - min(f1val))
            else:
                distance[k] = math.inf
        for k in range(1, len(front) - 1):
            if flag:
                distance[k] = distance[k] + (
                        f1val[sorted2[k + 1]] - f2val[sorted2[k - 1]]
                ) / (max(f2val) - min(f2val))
            else:
                distance[k] = math.inf
        return distance

    # ！
    @classmethod
    def sort_by_val(cls, front, val):
        sorted_list = copy.deepcopy(front)
        front_val =[val[index] for index in front]
        dic = dict(zip(sorted_list, front_val))
        sorted_dic = {k: v for k, v in sorted(dic.items(), key=lambda item: item[1], reverse=False)}
        return list(sorted_dic.keys())
    
    @classmethod
    def findindex(cls, num, val):
        for i in range(0, len(val)):
            if val[i] == num:
                return i
        return -1

    @classmethod
    def generateChild(cls, parent1, parent2):
        mr = random.random()
        childseq = cls.getCrossChildSeq(parent1, parent2)
        if mr < gm.get_value("mr"):
            r = random.random()

            if r > 0.5:
                return Chromosome(cls.mutation1(childseq))
            else:
                return Chromosome(cls.mutation2(childseq))
        return Chromosome(childseq)


    @classmethod
    def getCrossChildSeq(cls, PA, PB):
        m = gm.get_value("m")
        
        PApart1 = copy.deepcopy(PA.getPart1())
        PApart2 = copy.deepcopy(PA.getPart2())
        PBpart1 = copy.deepcopy(PB.getPart1())
        PBpart2 = copy.deepcopy(PB.getPart2())

        PAd = cls.decode(PApart1, PApart2)
        PBd = cls.decode(PBpart1, PBpart2)
        PAd.insert(0, 0)
        PBd.insert(0, 0)

        cross = cls.crossover(PAd, PBd, "forward")
        rational_cross = cls.rationalize(cross)
        childseq = cls.encode(rational_cross)

        return childseq

    @classmethod
    def crossover(cls, PA, PB, MARK):
        length = len(PA)
        l = random.randrange(1, length)
        k = PA[l]
        output = [k]
        # x = -1
        # y = -1
        while length > 1:
            if MARK == "forward":
                x = cls.latterCity(PA, k)
                y = cls.latterCity(PB, k)
            elif MARK == "backward":
                x = cls.formerCity(PA, k)
                y = cls.formerCity(PB, k)

            PA.remove(k)
            PB.remove(k)
            dx = cls.calDistance(k, x)
            dy = cls.calDistance(k, y)

            if dx < dy:
                k = x
            else:
                k = y

            output.append(k)
            length = len(PA)

        return output
    
    @classmethod
    def latterCity(cls, gene, k):
        i = (gene.index(k) + 1) % len(gene)
        return gene[i]

    @classmethod
    def formerCity(cls,gene, k):
        i = gene.index(k) - 1
        return gene[i]

    @classmethod
    def rationalize(cls, raw):
        i = 0
        while i < len(raw):
            x = raw[i]
            if x == 0 and not cls.isValid(raw, i):
                j = (i + 1) % len(raw)
                while j != i:
                    if cls.wouldBeValid(raw, j):
                        if j > i:
                            raw.pop(i)
                            i -= 1
                            raw.insert(j - 1, 0)
                        else:
                            raw.pop(i)
                            raw.insert(j, 0)
                        break
                    else:
                        j = (j + 1) % len(raw)
            i += 1

        return raw

    @classmethod
    def isValid(cls, raw, i):
        if i + 2 >= len(raw):
            return False

        if raw[i + 1] == 0 or raw[i + 2] == 0:
            return False

        if i == 0:
            return True

        if raw[max(i - 1, 0)] == 0 or raw[max(i - 2, 0)] == 0:
            return False

        return True

    @classmethod
    def wouldBeValid(cls, raw, i):
        if i + 1 >= len(raw):
            return False

        if raw[i] == 0 or raw[i + 1] == 0:
            return False

        if i == 0:
            return True

        if raw[max(i - 1, 0)] == 0 or raw[max(i - 2, 0)] == 0:
            return False

        return True
    
    @classmethod
    def encode(cls, raw):
        x = raw.index(0)
        raw = raw[x + 1:] + raw[:x]
        part2 = []

        for i, e in enumerate(raw):
            if e == 0:
                raw.pop(i)
                part2.append(i)

        raw.extend(part2)
        return raw

    @classmethod
    def mutation1(cls, parent):
        m = gm.get_value("m")
        n = len(parent)
        j = random.randint(1, n - (m - 1) - 1)
        i = random.randint(0, j - 1)
        part1 = parent[0:i] + parent[i:j][::-1] + parent[j : n - (m - 1)]

        part2 = [ i + x for i, x in enumerate(sorted(random.sample(range(2, n - 3), m - 1)))]
        return part1 + part2

    @classmethod
    def mutation2(cls, parent):
        m = gm.get_value("m")
        n = len(parent)
        j = random.randint(1, n - (m - 1) - 1)
        i = random.randint(0, j - 1)
        part1 = parent[i:j] + parent[0:i] + parent[j : n - (m - 1)]
        part2 = random.sample(range(1, n - m), m - 1)

        return part1 + part2




