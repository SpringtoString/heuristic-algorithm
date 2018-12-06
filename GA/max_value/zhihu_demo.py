import math
import random
import operator

class GA():
    def __init__(self, length, count):
        # 染色体长度
        self.length = length
        # 种群中的染色体数量
        self.count = count
        # 随机生成初始种群
        self.population = self.gen_population(length, count)

    def evolve(self, retain_rate=0.2, random_select_rate=0.5, mutation_rate=0.01):
        """
        进化
        对当前一代种群依次进行选择、交叉并生成新一代种群，然后对新一代种群进行变异
        """
        parents = self.selection(retain_rate, random_select_rate)
        self.crossover(parents)
        self.mutation(mutation_rate)

    def gen_chromosome(self, length):
        """
        随机生成长度为length的染色体，每个基因的取值是0或1
        这里用一个bit表示一个基因
        """
        chromosome = 0
        for i in range(length):
            chromosome |= (1 << i) * random.randint(0, 1)
        return chromosome

    def gen_population(self, length, count):
        """
        获取初始种群（一个含有count个长度为length的染色体的列表）
        """
        return [self.gen_chromosome(length) for i in range(count)]

    def fitness(self, chromosome):
        """
        计算适应度，将染色体解码为0~9之间数字，代入函数计算
        因为是求最大值，所以数值越大，适应度越高
        """
        x = self.decode(chromosome)
        return x + 10*math.sin(5*x) + 7*math.cos(4*x)

    def selection(self, retain_rate, random_select_rate):
        """
        选择
        先对适应度从大到小排序，选出存活的染色体
        再进行随机选择，选出适应度虽然小，但是幸存下来的个体
        """
        # 对适应度从大到小进行排序
        graded = [(self.fitness(chromosome), chromosome) for chromosome in self.population]
        graded = [x[1] for x in sorted(graded, reverse=True)]
        # 选出适应性强的染色体
        retain_length = int(len(graded) * retain_rate)
        parents = graded[:retain_length]
        # 选出适应性不强，但是幸存的染色体
        for chromosome in graded[retain_length:]:
            if random.random() < random_select_rate:
                parents.append(chromosome)
        return parents

    def crossover(self, parents):
        """
        染色体的交叉、繁殖，生成新一代的种群
        """
        # 新出生的孩子，最终会被加入存活下来的父母之中，形成新一代的种群。
        children = []
        # 需要繁殖的孩子的量
        target_count = len(self.population) - len(parents)
        # 开始根据需要的量进行繁殖
        while len(children) < target_count:
            male = random.randint(0, len(parents)-1)
            female = random.randint(0, len(parents)-1)
            if male != female:
                # 随机选取交叉点
                cross_pos = random.randint(0, self.length)
                # 生成掩码，方便位操作
                mask = 0
                for i in range(cross_pos):
                    mask |= (1 << i)
                male = parents[male]
                female = parents[female]
                # 孩子将获得父亲在交叉点前的基因和母亲在交叉点后（包括交叉点）的基因
                child = ((male & mask) | (female & ~mask)) & ((1 << self.length) - 1)
                children.append(child)
        # 经过繁殖后，孩子和父母的数量与原始种群数量相等，在这里可以更新种群。
        self.population = parents + children

    def mutation(self, rate):
        """
        变异
        对种群中的所有个体，随机改变某个个体中的某个基因
        """
        for i in range(len(self.population)):
            if random.random() < rate:
                j = random.randint(0, self.length-1)
                self.population[i] ^= 1 << j


    def decode(self, chromosome):
        """
        解码染色体，将二进制转化为属于[0, 9]的实数
        """
        return chromosome * 9.0 / (2**self.length-1)

    def result(self):
        """
        获得当前代的最优值，这里取的是函数取最大值时x的值。
        """
        graded = [(self.fitness(chromosome), chromosome) for chromosome in self.population]
        graded = [x[1] for x in sorted(graded, reverse=True)]
        return ga.decode(graded[0])


if __name__ == '__main__':
    # 染色体长度为17， 种群数量为300
    ga = GA(17, 300)

    # 200次进化迭代
    for x in range(200):
         ga.evolve()

    print(ga.result())