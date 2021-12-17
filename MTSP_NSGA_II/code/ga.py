from nodemanager import NodeManager
from chromosome import Chromosome
from node import Node
from nsga_ii import fast_non_dominated_sort, crowding_distance
import random
import copy
import time


class GA:
    """genetic algorithm class

    Reference:The population select algorithm in this class was mainly based on the NSGA-II:
    https://github.com/haris989/NSGA-II ;Most of the code was based on the arifield's work:
    https://github.com/ariefield/MTSP-Genetic

    Atrributes:

    """

    def __init__(self, problem, num_travellers, population_size, generations, mutation_rate):
        self.num_travellers = num_travellers
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.node_manager = NodeManager()
        # Load problem data
        path = "..//data//" + problem + ".txt"
        file = open(path, 'r')
        n = -1
        for index, row in enumerate(file):
            if index == 0:
                row = row.strip()
                n = int(row)
            else:
                row = row.strip()
                elems = row.split(' ')
                node = Node(int(elems[1]), int(elems[2]))
                self.node_manager.add_node(node)
        self.num_citys = n

    def solve(self):
        '''

        Returns:

        '''

        def _find_index(num, val):
            for i in range(0, len(val)):
                if val[i] == num:
                    return i
            return -1

        p_t = [Chromosome(1, self.num_citys, self.num_travellers) for i in range(0, self.population_size)]
        print("START!")
        start_time = time.time()
        best_chromo = []
        minfun1val_per_round = []
        minfun2val_per_round = []

        for i in range(self.generations):

            # Obtain current best chromosome
            f1val = [self.fitness_function_1(chromo) for chromo in p_t]
            f2val = [self.fitness_function_2(chromo) for chromo in p_t]
            non_dominated_sorted_solution = fast_non_dominated_sort(f1val[:], f2val[:])
            best_chromo = [p_t[i] for i in non_dominated_sorted_solution[0]]

            # Record current minimal value of function1 and function2
            minfun1val_per_round.append(min(self.fitness_function_1(chromo) for chromo in best_chromo))
            minfun2val_per_round.append(min(self.fitness_function_2(chromo) for chromo in best_chromo))

            # Calculate crowding distance values
            crowding_distance_values = []
            for i in range(0, len(non_dominated_sorted_solution)):
                crowding_distance_values.append(
                    crowding_distance(f1val[:], f2val[:], non_dominated_sorted_solution[i][:]))

            # Add Qi to Ri (Ri = Pi U Qi)
            r_t = p_t[:]
            while len(r_t) != 2 * self.population_size:
                a1 = random.randint(0, self.population_size - 1)
                b1 = random.randint(0, self.population_size - 1)
                r_t.append(self.generateChild(p_t[a1], p_t[b1]))

            # Fast non-dominated sort
            f1val2 = [self.fitness_function_1(r_t[i]) for i in range(0, 2 * self.population_size)]
            f2val2 = [self.fitness_function_2(r_t[i]) for i in range(0, 2 * self.population_size)]
            non_dominated_sorted_Ri = fast_non_dominated_sort(f1val2[:], f2val2[:])

            # Calculate crowding distance values
            crowding_distance_values2 = []
            for i in range(0, len(non_dominated_sorted_Ri)):
                crowding_distance_values2.append(
                    crowding_distance(f1val2[:], f2val2[:], non_dominated_sorted_Ri[i][:]))

            # Generate new Pi
            indexOfPnext = []
            for i in range(0, len(non_dominated_sorted_Ri)):
                non_dominated_sorted_Ri_1 = [
                    _find_index(non_dominated_sorted_Ri[i][j], non_dominated_sorted_Ri[i])
                    for j in range(0, len(non_dominated_sorted_Ri[i]))
                ]
                front22 = sorted(non_dominated_sorted_Ri_1[:], key=lambda x: crowding_distance_values2[i][:][x])
                front = [
                    non_dominated_sorted_Ri[i][front22[j]]
                    for j in range(0, len(non_dominated_sorted_Ri[i]))
                ]
                front.reverse()

                for value in front:
                    indexOfPnext.append(value)
                    if len(indexOfPnext) == self.population_size:
                        break
                if len(indexOfPnext) == self.population_size:
                    break

            p_t = [r_t[i] for i in indexOfPnext]

        end_time = time.time()
        runtime = end_time - start_time

        f1valbest = [self.fitness_function_1(chromo) for chromo in best_chromo]
        f2valbest = [self.fitness_function_2(chromo) for chromo in best_chromo]

        # as for this project we just need to konw the shortest path,that is the min f1 value
        optimal_length = min(f1valbest)
        optimal_path = best_chromo[f1valbest.index(optimal_length)].getAll()

        return runtime, optimal_length, optimal_path, minfun1val_per_round

    def fitness_function_1(self, chromosome: Chromosome) -> int:
        """

        Args:
            chromosome:

        Returns:

        """
        totaldis = 0

        decode = Chromosome.decode(chromosome.getPart1(), chromosome.getPart2())
        decode.append(0)
        preindex = 0
        for index in decode:
            totaldis += self.node_manager.cal_node_distance(preindex, index)
            preindex = index

        return totaldis

    def fitness_function_2(self, chromosome: Chromosome) -> int:
        """

        Args:
            chromosome:

        Returns:

        """
        totaldis = 0
        preindex = 0
        salesmendis = []

        decode = Chromosome.decode(chromosome.getPart1(), chromosome.getPart2())
        decode.append(0)

        for index in decode:
            totaldis += self.node_manager.cal_node_distance(preindex, index)
            preindex = index
            if index == 0:
                salesmendis.append(totaldis)
                totaldis = 0

        return max(salesmendis) - min(salesmendis)

    def getCrossChildSeq(self, pa: Chromosome, pb: Chromosome) -> list:
        """
        
        Args:
            pa:
            pb:

        Returns:

        """
        PApart1 = copy.deepcopy(pa.getPart1())
        PApart2 = copy.deepcopy(pa.getPart2())
        PBpart1 = copy.deepcopy(pb.getPart1())
        PBpart2 = copy.deepcopy(pb.getPart2())

        PAd = Chromosome.decode(PApart1, PApart2)
        PBd = Chromosome.decode(PBpart1, PBpart2)
        PAd.insert(0, 0)
        PBd.insert(0, 0)

        cross = self.crossover(PAd, PBd, "forward")
        rational_cross = self.rationalize(cross)
        childseq = Chromosome.encode(rational_cross)

        return childseq

    def crossover(self, pa, pb, mark):
        def _latterCity(gene, k):
            i = (gene.index(k) + 1) % len(gene)
            return gene[i]

        def _formerCity(gene, k):
            i = gene.index(k) - 1
            return gene[i]

        length = len(pa)
        l = random.randrange(1, length)
        k = pa[l]
        output = [k]
        # x = -1
        # y = -1
        while length > 1:
            if mark == "forward":
                x = _latterCity(pa, k)
                y = _latterCity(pb, k)
            elif mark == "backward":
                x = _formerCity(pa, k)
                y = _formerCity(pb, k)

            pa.remove(k)
            pb.remove(k)
            dx = self.node_manager.cal_node_distance(k, x)
            dy = self.node_manager.cal_node_distance(k, y)

            if dx < dy:
                k = x
            else:
                k = y

            output.append(k)
            length = len(pa)

        return output

    @classmethod
    def rationalize(cls, raw):
        def _isValid(raw, i):
            if i + 2 >= len(raw):
                return False

            if raw[i + 1] == 0 or raw[i + 2] == 0:
                return False

            if i == 0:
                return True

            if raw[max(i - 1, 0)] == 0 or raw[max(i - 2, 0)] == 0:
                return False

            return True

        def _wouldBeValid(raw, i):
            if i + 1 >= len(raw):
                return False

            if raw[i] == 0 or raw[i + 1] == 0:
                return False

            if i == 0:
                return True

            if raw[max(i - 1, 0)] == 0 or raw[max(i - 2, 0)] == 0:
                return False

            return True

        i = 0
        while i < len(raw):
            x = raw[i]
            if x == 0 and not _isValid(raw, i):
                j = (i + 1) % len(raw)
                while j != i:
                    if _wouldBeValid(raw, j):
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

    def generateChild(self, parent1, parent2):
        mr = random.random()
        childseq = self.getCrossChildSeq(parent1, parent2)
        if mr < self.mutation_rate:
            r = random.random()

            if r > 0.5:
                return Chromosome(0, self.mutation1(childseq), self.num_travellers)
            else:
                return Chromosome(0, self.mutation2(childseq), self.num_travellers)
        return Chromosome(0, childseq, self.num_travellers)

    def mutation1(self, parent):
        m = self.num_travellers
        n = len(parent)
        j = random.randint(1, n - (m - 1) - 1)
        i = random.randint(0, j - 1)
        part1 = parent[0:i] + parent[i:j][::-1] + parent[j: n - (m - 1)]

        part2 = [i + x for i, x in enumerate(sorted(random.sample(range(2, n - 3), m - 1)))]
        return part1 + part2

    def mutation2(self, parent):
        m = self.num_travellers
        n = len(parent)
        j = random.randint(1, n - (m - 1) - 1)
        i = random.randint(0, j - 1)
        part1 = parent[i:j] + parent[0:i] + parent[j: n - (m - 1)]
        part2 = random.sample(range(1, n - m), m - 1)

        return part1 + part2


if __name__ == "__main__":
    ga = GA("mtsp51", 5, 100, 200, 0.2)
    print(ga.sort_by_val([1, 2], [1, 8, 4, 8]))
    a = [1, 2]
    b = [1, 8, 4, 8]
    a = sorted(a, key=lambda x: b[x])
    print(a)
