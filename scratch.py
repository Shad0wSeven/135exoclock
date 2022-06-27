import numpy as np

z = np.loadtxt('data.txt', delimiter=' ')

print(z[:, 0].shape)

time = np.linspace(0.7, 0.8, 1000)  # [day]
print(time.shape)
# time = np.linspace(0.7, 0.8, 1000)  # [day]

# print(time[0])