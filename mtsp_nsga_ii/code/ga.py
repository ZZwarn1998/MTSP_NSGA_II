from nodemanager import NodeManager
from chromosome import Chromosome
from node import Node
from nsga_ii import fast_non_dominated_sort, crowding_distance
import random
import copy
import time


class GA:
    """genetic algorithm class
    The class to solve the mtsp problem, the core method of this class is the crossover and mutation methods,the solve()
    methods use the process of NSGA-II to solve the problem.

    Reference:The population select algorithm in this class was mainly based on the NSGA-II:
    https://github.com/haris989/NSGA-II ;Most of the code was based on the arifield's work:
    https://github.com/ariefield/MTSP-Genetic

    Atrributes:
        problem: A str that the specific problem to solve
        num_travellers: A int that the num of travellers, in this project is 5
        population_size: Int, num of population size, in this project is 100
        generations: Int, num of generations when solve, in this project is 200
        mutation_rate: Int, probability of mutation, in this prject is 0.2
        node_manager: An instance of NodeManager class which manage the city nodes
        num_citys: Int, the number of citys
    """

    def __init__(self, problem, num_travellers, population_size, generations, mutation_rate):
        self.problem = problem
        self.num_travellers = num_travellers
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.node_manager = NodeManager()
        # Load problem data
        path = "..//data//" + self.problem + ".txt"
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
        """Solve function to get the solution of the question,use the process of NSGA-II

        Returns:
            runtime: float, the runtime of the GA algorithm
            optimal_length: int, the minimize of the sum distance
            optimal_path: list, the solution of the path
            minfun1val_per_round: list,The optimal solution for each generation

        """

        def _find_index(num, val):
            for i in range(0, len(val)):
                if val[i] == num:
                    return i
            return -1

        Pi = [Chromosome(1, self.num_citys, self.num_travellers) for i in range(0, self.population_size)]
        print("START!")
        start_time = time.time()
        best_chromo = []
        minfun1val_per_round = []
        minfun2val_per_round = []

        for i in range(self.generations):

            # Obtain current best chromosome
            f1val = [self.fitness_function_1(chromo) for chromo in Pi]
            f2val = [self.fitness_function_2(chromo) for chromo in Pi]
            non_dominated_sorted_solution = fast_non_dominated_sort(f1val[:], f2val[:])
            best_chromo = [Pi[i] for i in non_dominated_sorted_solution[0]]

            # Record current minimal value of function1 and function2
            minfun1val_per_round.append(min(self.fitness_function_1(chromo) for chromo in best_chromo))
            minfun2val_per_round.append(min(self.fitness_function_2(chromo) for chromo in best_chromo))

            # Calculate crowding distance values
            crowding_distance_values = []
            for i in range(0, len(non_dominated_sorted_solution)):
                crowding_distance_values.append(
                    crowding_distance(f1val[:], f2val[:], non_dominated_sorted_solution[i][:]))

            # Add Pi to Ri (Ri = Pi U Qi)
            Ri = Pi[:]
            while len(Ri) != 2 * self.population_size:
                a1 = random.randint(0, self.population_size - 1)
                b1 = random.randint(0, self.population_size - 1)
                Ri.append(self.generateChild(Pi[a1], Pi[b1]))

            # Fast non-dominated sort
            f1val2 = [self.fitness_function_1(Ri[i]) for i in range(0, 2 * self.population_size)]
            f2val2 = [self.fitness_function_2(Ri[i]) for i in range(0, 2 * self.population_size)]
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

            Pi = [Ri[i] for i in indexOfPnext]

        end_time = time.time()
        runtime = end_time - start_time

        f1valbest = [self.fitness_function_1(chromo) for chromo in best_chromo]
        f2valbest = [self.fitness_function_2(chromo) for chromo in best_chromo]

        # as for this project we just need to konw the shortest path,that is the min f1 value
        optimal_length = min(f1valbest)
        optimal_path = best_chromo[f1valbest.index(optimal_length)].getAll()

        return runtime, optimal_length, optimal_path, minfun1val_per_round

    def fitness_function_1(self, chromosome: Chromosome):
        """function to calulate the value of fitness type 1

        Args:
            chromosome:Chromosome instance that to be calulate

        Returns:
            The value of fitness function 1, note that this function expect to reduce the total sum diatance

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
        """function to calulate the value of fitness type 2

        Args:
            chromosome:Chromosome instance that to be calulate

        Returns:
            The value of fitness function 2, note that this function expect to reduce the distance of each traveller

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

    def generateChild(self, parent1: Chromosome, parent2: Chromosome):
        """Generate a child by two parents
        This function is to generate a new child by the crossover and mutation operate

        Args:
            parent1: Chromosome, parents A to generate the child
            parent2: Chromosome, parents B to generate the child

        Returns:
            Chromosome, the child

        """
        mr = random.random()
        childseq = self.getCrossChildSeq(parent1, parent2)
        if mr < self.mutation_rate:
            r = random.random()

            if r > 0.5:
                return Chromosome(0, self.mutation1(childseq), self.num_travellers)
            else:
                return Chromosome(0, self.mutation2(childseq), self.num_travellers)
        return Chromosome(0, childseq, self.num_travellers)

    def getCrossChildSeq(self, pa: Chromosome, pb: Chromosome) -> list:
        """The function to do the crossover operate between two Chromosome
        Note that after generate a child by crossover() we need to do rationalize
        Args:
            pa:Chromosome, parents A to do the crossover operate
            pb:Chromosome, parents B to do the crossover operate

        Returns:
            Note that the return of this function is a list of child not Chomosome instance

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
        """The function to do the crossovere operate between two parents represented by list

        Args:
            pa: list, parent A to do the crossover
            pb: list, parent B to do the crossover
            mark: str, the search directions

        Returns:
            The result after crossover, list.

        """

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
        """Rationalize the crossover result
        As the result by the crossover() may unreasonable, that is, for example: 0123004560, there are two
        zeros linked together, this function is to fix this problem.

        Args:
            raw: List, the result after the crossver

        Returns:
            the list result after processing

        """

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

    def mutation1(self, parent):
        """Mutation operate type 1

        Args:
            parent: list

        Returns:
            The list of the result

        """
        m = self.num_travellers
        n = len(parent)
        j = random.randint(1, n - (m - 1) - 1)
        i = random.randint(0, j - 1)
        part1 = parent[0:i] + parent[i:j][::-1] + parent[j: n - (m - 1)]

        part2 = [i + x for i, x in enumerate(sorted(random.sample(range(2, n - 3), m - 1)))]
        return part1 + part2

    def mutation2(self, parent):
        """Mutation operate type 2"""
        m = self.num_travellers
        n = len(parent)
        j = random.randint(1, n - (m - 1) - 1)
        i = random.randint(0, j - 1)
        part1 = parent[i:j] + parent[0:i] + parent[j: n - (m - 1)]
        part2 = random.sample(range(1, n - m), m - 1)

        return part1 + part2



