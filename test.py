import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("/data/cardio_train.csv")

'''
y = [1, 2, 4, 12]
plt.plot(y, "bo")
plt.plot(y, "go")
plt.show()
'''
x = np.linspace(0, 10, 100)

plt.plot(x, np.sin(x))
plt.plot(x, np.cos(x), 'bo-')

fig, axs = plt.subplots(2, 1)  # 2 rows, 1 column

axs[0].plot(x, np.sin(x))
axs[0].set_title("Sine")

axs[1].plot(x, np.cos(x))
axs[1].set_title("Cosine")

fig.suptitle("Trigonometric Functions")
plt.tight_layout()
plt.show()
'''
#######################
x = np.linspace(0, 10, 100)
ax = plt.axes()
ax.plot(x, np.sin(x))
ax.set(xlim=(0, 10), ylim=(-2, 2),
       xlabel='x', ylabel='sin(x)',
       title='A Simple Plot')
plt.show()
'''