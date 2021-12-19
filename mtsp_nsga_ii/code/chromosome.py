import copy
import random


class Chromosome:
    """chromosome class """
    def __init__(self, option, *args):
        """Init a chromosome

        Args:
            option: int, 0:init a chromosome by a specific parameter;1:random init a chromosome
            *args: if option==0, param1 is the gene(list) of the chromosome, param2 is the number of travelles
                   if option==1, param1 is the number of citys and param2 is number of travellers
        """
        if option == 0:  # param1:gene parm2:num of travellers
            self.gen = args[0]
            self.num_travellers = args[1]
        if option == 1:  # random, param1:num_citys, param2:num_travellers
            self.gen, self.num_travellers = self.randomly_generate(args[1], args[0])

    def getAll(self):
        """Get the all part of the Chomosome"""
        return self.getPart1()+self.getPart2()

    def getPart1(self):
        """Get the part1 of the chomosome which is the path of all travellers"""
        part1 = copy.deepcopy(self.gen[: -(self.num_travellers - 1)])
        return part1

    def getPart2(self):
        """Get part2 of the chmomosome which is the control index for different paths"""
        part2 = copy.deepcopy(self.gen[len(self.gen) - (self.num_travellers - 1):])
        return part2

    @classmethod
    def randomly_generate(cls, num_traverlers, num_citys):
        """randomly generate a chomosome by given number of travellers and citys"""
        part1 = random.sample(range(1, num_citys), num_citys - 1)
        part2 = [i + num for i, num in
                 enumerate(sorted(random.sample(range(2, num_citys - 3), num_traverlers - 1)))]
        return part1 + part2, num_traverlers

    @classmethod
    def encode(cls, gene):
        """Do encode.E.g: 0123045067 -> 1234567|35

        """
        x = gene.index(0)
        gene = gene[x + 1:] + gene[:x]
        part2 = []

        for i, e in enumerate(gene):
            if e == 0:
                gene.pop(i)
                part2.append(i)
        gene.extend(part2)
        return gene

    @classmethod
    def decode(cls, p1, p2):
        """Do decode.E.g: 1234567|35->123045067

        Args:
            p1: part1 of the gene represent by list
            p2: part2 of the gene represent by list

        Returns:
            The decode gene

        """
        offset = 0
        for x in p2:
            p1.insert(x + offset, 0)
            offset += 1
        return p1

