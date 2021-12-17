import copy
import random


class Chromosome:
    def __init__(self, option, *args):
        if option == 0:  # param1:num_travellers parm2:num of travellers
            self.gen = args[0]
            self.num_travellers = args[1]
        if option == 1:  # random, param1:num_citys, param2:num_travellers
            self.gen, self.num_travellers = self.randomly_generate(args[1], args[0])

    def getAll(self):
        return self.getPart1()+self.getPart2()

    def getPart1(self):
        part1 = copy.deepcopy(self.gen[: -(self.num_travellers - 1)])
        return part1

    def getPart2(self):
        part2 = copy.deepcopy(self.gen[len(self.gen) - (self.num_travellers - 1):])
        return part2

    @classmethod
    def randomly_generate(cls, num_traverlers, num_citys):
        part1 = random.sample(range(1, num_citys), num_citys - 1)
        part2 = [i + num for i, num in
                 enumerate(sorted(random.sample(range(2, num_citys - 3), num_traverlers - 1)))]
        return part1 + part2, num_traverlers

    @classmethod
    def encode(cls, gene):
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
        offset = 0
        for x in p2:
            p1.insert(x + offset, 0)
            offset += 1
        return p1

if __name__ == "__main__":
    ch = Chromosome(0, [1, 2, 3, 4, 5, 6, 7], 3)
    print(ch.getPart1())
    ch2 = Chromosome(1, 20, 3)
    print(ch2.getPart1())
    print(ch2.getPart2())
