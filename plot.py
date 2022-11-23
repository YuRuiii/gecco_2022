import numpy as np
import matplotlib.pyplot as plt

idx = []
fitness = []
with open('fitness.txt', 'r') as f:
    lines = f.readlines()
    
for line in lines:
    line.split(' ')
    idx.append(int(line[0]))
    fitness.append(float(line[1]))
    
x = np.array(idx)
y = np.array(fitness)
plt.plot(x, y)
plt.show()
    

    