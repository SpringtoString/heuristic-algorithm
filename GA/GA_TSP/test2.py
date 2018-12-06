import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import math
import random
matplotlib.rcParams['font.family']= 'STSong'

#载入数据
city_name=[]
city_condition=[]
with open('data.txt','r') as f:
    lines=f.readlines()
    for line in lines:
        line=line.split('\n')[0]
        line=line.split(',')
        city_name.append(line[0])
        city_condition.append([float(line[1]),float(line[2])])
city_condition=np.array(city_condition)

#展示地图
# plt.scatter(city_condition[:,0],city_condition[:,1])
# plt.show()

#距离矩阵
city_count=len(city_name)
Distance=np.zeros([city_count,city_count])
for i in range(city_count):
    for j in range(city_count):
        Distance[i][j]=math.sqrt((city_condition[i][0]-city_condition[j][0])**2+(city_condition[i][1]-city_condition[j][1])**2)


#种群数
count=300
#改良次数
improve_count=30000
#进化次数
itter_time=30000

#设置强者的定义概率，即种群前30%为强者
retain_rate=0.3

#设置弱者的存活概率
random_select_rate=0.5

#变异率
mutation_rate=0.1

#设置起点
origin=15
index=[i for i in range(city_count)]
index.remove(15)


# def get_path(x):
#     graded = [[x[i], index[i]] for i in range(len(x))]
#     graded_index = [t[1] for t in sorted(graded)]
#     return graded_index
#总距离
def get_total_distance(x):
    distance=0
    distance+=Distance[origin][x[0]]
    for i in range(len(x)):
        if i==len(x)-1:
            distance += Distance[origin][x[i]]
        else:
            distance += Distance[x[i]][x[i+1]]
    return distance

#改良
def improve(x):
    i=0
    distance=get_total_distance(x)
    while i<improve_count:
        # randint [a,b]
        u=random.randint(0,len(x)-1)
        v = random.randint(0, len(x)-1)
        if u!=v:
            new_x=x.copy()
            t=new_x[u]
            new_x[u]=new_x[v]
            new_x[v]=t
            new_distance=get_total_distance(new_x)
            if new_distance<distance:
                distance=new_distance
                x=new_x.copy()
        else:
            continue
        i+=1

#自然选择
def selection(population):
    """
    选择
    先对适应度从大到小排序，选出存活的染色体
    再进行随机选择，选出适应度虽然小，但是幸存下来的个体
    """
    # 对总距离从小到大进行排序
    graded = [[get_total_distance(x), x] for x in population]
    graded = [x[1] for x in sorted(graded)]
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

            left=random.randint(0,len(male)-2)
            right=random.randint(left+1,len(male)-1)

            #交叉片段
            gene1=male[left:right]
            gene2=female[left:right]

            child1_c=male[right:]+male[:right]
            child2_c=female[right:]+female[:right]
            child1=child1_c.copy()
            child2= child2_c.copy()

            for o in gene2:
                child1_c.remove(o)

            for o in gene1:
                child2_c.remove(o)

            child1[left:right]=gene2
            child2[left:right]=gene1

            child1[right:]=child1_c[0:len(child1)-right]
            child1[:left] = child1_c[len(child1) - right:]

            child2[right:] = child2_c[0:len(child1) - right]
            child2[:left] = child2_c[len(child1) - right:]

            children.append(child1)
            children.append(child2)

    return children

#变异
def mutation(children):
    for i in range(len(children)):
        if random.random() < mutation_rate:
            child=children[i]
            u=random.randint(1,len(child)-4)
            v = random.randint(u+1, len(child)-3)
            w= random.randint(v+1, len(child)-2)
            child=children[i]
            child=child[0:u]+child[v:w]+child[u:v]+child[w:]

#得到最佳纯输出结果
def get_result(population):
    graded = [[get_total_distance(x), x] for x in population]
    graded = sorted(graded)
    return graded[0][0],graded[0][1]

#使用改良圈算法初始化种群
population=[]
for i in range(count):
    #随机生成个体
    x=index.copy()
    random.shuffle(x)
    improve(x)
    population.append(x)

register=[]
i=0
distance, result_path = get_result(population)
while i<itter_time:
    #选择繁殖个体群
    parents=selection(population)
    #交叉繁殖
    children=crossover(parents)
    #变异操作
    mutation(children)
    #更新种群
    population=parents+children

    distance,result_path=get_result(population)
    register.append(distance)
    i=i+1

print(distance)
print(result_path)

result_path=[origin]+result_path+[origin]
X=[]
Y=[]
for index in result_path:
    X.append(city_condition[index,0])
    Y.append(city_condition[index, 1])

plt.plot(X,Y,'-o')
plt.show()

plt.plot(list(range(len(register))),register)
plt.show()