import numpy as np
import matplotlib.pyplot as plt
x=np.linspace(-10,10,100)

y=x + 10*np.sin(5*x) + 7*np.cos(4*x)

plt.plot(x,y)
plt.show()