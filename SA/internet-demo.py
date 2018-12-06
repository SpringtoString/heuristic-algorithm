import numpy as np
import matplotlib.pyplot as plt

def inputfun(x):
    return (x-2)*(x+3)*(x+8)*(x-9)

initT = 1000 #初始温度
minT = 1 #温度下限
iterL = 1000 #每个T值的迭代次数
delta = 0.95 #温度衰减系数
k = 1

initx = -10
nowt = initT
print ("初始解：",initx)

xx = np.linspace(-10,10,300)
yy = inputfun(xx)
plt.figure()
plt.plot(xx,yy)
plt.plot(initx,inputfun(initx),'o')

#模拟退火算法寻找最小值过程
while nowt>minT:
    for i in np.arange(1,iterL,1):
        funVal = inputfun(initx)
        xnew = initx+(2*np.random.rand()-1)
        if xnew>=-10 and xnew<=10:
            funnew = inputfun(xnew)
            res = funnew-funVal
            if res<0:
                initx = xnew
            else:
                p = np.exp(-(res)/(k*nowt))
                if np.random.rand()<p:
                    initx = xnew
#            print initx-xnew
#    print initx
#    print nowt
    nowt = nowt*delta

print ("最优解：",initx)
print ("最优值：",inputfun(initx))
plt.plot(initx,inputfun(initx),'*r')
plt.show()