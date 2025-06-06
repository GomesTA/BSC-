import matplotlib.pyplot as plt
import random

x = [0, 1, 2, 3]
y = [0, 3, 4, 5]

# Extend the lists with additional random values
for _ in range(5):
    x.append(x[-1] + 1)
    y.append(random.randint(0, 10))

plt.plot(x, y, marker='o')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Plot of x vs y')
plt.grid(True)
plt.show()
