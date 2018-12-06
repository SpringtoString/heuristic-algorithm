import numpy as np
import matplotlib.pyplot as plt
import math
import random
# x=np.linspace(-10,10,100)
#
# y=x + 10*np.sin(5*x) + 7*np.cos(4*x)

#GA参数
#查找范围
start=0
end=10

#染色体长度
length=18

#种群数
count=20

#进化次数
itter_time=10

#设置强者的定义概率，即种群前30%为强者
retain_rate=0.3

#设置弱者的存活概率
random_select_rate=0.5

#变异率
mutation_rate=0.2


#目标函数
def aimFunction(x):
    y=x+5*math.sin(5*x)+2*math.cos(4*x)
    return y

#解码
def decode(x):
    y=start+x*(end-start) / (2**length-1)
    return y

#获取随机个体，用于生成种群
def gen_chromosome():
    """
    随机生成长度为length的染色体，每个基因的取值是0或1
    这里用一个bit表示一个基因
    """
    chromosome = 0
    for i in range(length):
        chromosome |= (1 << i) * random.randint(0, 1)
    return chromosome

#自然选择
def selection(population):
    """
    选择
    先对适应度从大到小排序，选出存活的染色体
    再进行随机选择，选出适应度虽然小，但是幸存下来的个体
    """
    # 对适应度从大到小进行排序
    graded = [(aimFunction(decode(chromosome)), chromosome) for chromosome in population]
    graded = [x[1] for x in sorted(graded, reverse=True)]
    # 选出适应性强的染色体
    retain_length = int(len(graded) * retain_rate)
    parents = graded[:retain_length]
    # 选出适应性不强，但是幸存的染色体
    for chromosome in graded[retain_length:]:
        if random.random() < random_select_rate:
            parents.append(chromosome)
    return parents

#交叉繁殖
def crossover(parents):
    #生成子代的个数,以此保证种群稳定
    target_count=count-len(parents)
    #孩子列表
    children=[]
    while len(children)<target_count:
        male_index = random.randint(0, len(parents) - 1)
        female_index = random.randint(0, len(parents) - 1)
        if male_index!=female_index:
            male=parents[male_index]
            female=parents[female_index]
            cross_pos = random.randint(0, length)
            mask = 0
            for i in range(cross_pos):
                mask |= (1 << i)
            # 孩子将获得父亲在交叉点前的基因和母亲在交叉点后（包括交叉点）的基因
            child = ((male & mask) | (female & ~mask)) & ((1 << length) - 1)
            children.append(child)
    return children

#变异
def mutation(children):
    for i in range(len(children)):
        if random.random() < mutation_rate:
            j = random.randint(0, length-1)
            population[i] ^= 1 << j

#得到最佳纯输出结果
def get_result(population):
    graded = [(aimFunction(decode(chromosome)), decode(chromosome)) for chromosome in population]
    graded = [x for x in sorted(graded, reverse=True)]
    print(graded[0][0],graded[0][1])

#开始遗传算法
#初始化种群，随机性得到种群
population=[gen_chromosome() for i in range(count)]
i=0
while i<itter_time:
    #选择繁殖个体群
    parents=selection(population)
    #交叉繁殖
    children=crossover(parents)
    #变异操作
    mutation(children)
    #更新种群
    population=parents+children
    get_result(population)
    i=i+1











