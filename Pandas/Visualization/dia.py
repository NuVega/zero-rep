import matplotlib.pyplot as plt
import numpy as np

array1 = np.random.rand(5)
array2 = np.random.rand(5)

plt.scatter(array1, array2)

plt.xlabel("X")
plt.ylabel("Y")
plt.title("Диаграмма рассеяния")

plt.show()