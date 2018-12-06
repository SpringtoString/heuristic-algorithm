import numpy as np
import matplotlib.pyplot as plt
import math
import random
x=np.linspace(0,10,100)

y=x + 5*np.sin(5*x) + 2*np.cos(4*x)

plt.plot(x,y)
plt.show()
