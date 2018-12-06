import numpy as np
import matplotlib.pyplot as plt
import math
import random

def aimFunction(x):
    y=x+5*math.sin(5*x)+2*math.cos(4*x)
    return y

start=0
end=10

X=random.uniform(start,end)
Y=aimFunction(X)

T=100
rate=0.99
while T>1:
    x=random.uniform(start,end)
    y=aimFunction(x)
    if y>Y:
        X=x
        Y=y
    else:
        if math.exp(-(Y-y)/T)>random.random():
            X = x
            Y = y
    T*=rate

print(X,Y)

