import os.path

import numpy as np

matrix = np.load("../41/second_task.npy")

x = []
y = []
z = []

threshold = 500 + 41

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        el = matrix[i][j]
        if el > threshold:
            x.append(i)
            y.append(j)
            z.append(el)


np.savez("Task 2.npz", x=x, y=y, z=z)
np.savez_compressed("Task 2 (compressed).npz", x=x, y=y, z=z)

npz_size = os.path.getsize("Task 2.npz")
npz_compressed_size = os.path.getsize("Task 2 (compressed).npz")

print(f'savez = {npz_size}')
print(f'savez_compressed = {npz_compressed_size}')
print(f'diff = {npz_size - npz_compressed_size}')