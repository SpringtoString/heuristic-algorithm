import numpy as np
import matplotlib.pyplot as plt
import math
import random

#群体规模
m=30

#惯性权重
w=1

# 加速常数
c1=2
c2=5

# 最大速度
Vmax=3

# 最大代数
Gmax=10

#目标函数，也就是适应度
def aimFunction(x):
    y=x+5*math.sin(5*x)+2*math.cos(4*x)
    return y

#左右边界
left=0
right=10
#随机初始化粒子群位置和速度
x=np.random.uniform(left,right,m)
y=x+5*np.sin(5*x)+2*np.cos(4*x)
v=np.random.uniform(0,Vmax,m)

pbset=x.copy()
y_best=y.copy()
gbset=x[y.argmax()]

i=0

while i<Gmax:
    for k in range(m):
        v[k] = w * v[k] + c1 * random.random() * (pbset[k] - x[k]) + c2 * random.random() * (gbset - x[k])
        # 速度限制
        if v[k]>Vmax:
            v[k]=Vmax
        if v[k]<0:
            v[k] = 0.01
        x[k]=x[k]+v[k]
        if x[k]<left:
            x[k]=left
        if x[k]>right:
            x[k]=right
    y=x+5*np.sin(5*x)+2*np.cos(4*x)
    for k in range(m):
        if y_best[k]<y[k]:
            y_best[k]=y[k]
            pbset[k]=x[k]
    gbset=pbset[y_best.argmax()]
    i+=1

print(gbset,aimFunction(gbset))
