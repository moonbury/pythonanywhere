import numpy
from matplotlib import pyplot as plot
import matplotlib.cm as cm

def iter_count(C, max_iter):
	X = C
	for n in range(max_iter):
		if abs(X) > 2.:
			return n
		X = X ** 2 + C
	return max_iter

N = 512
max_iter = 64
xmin, xmax, ymin, ymax = -0.32, -0.22, 0.8, 0.9
X = numpy.linspace(xmin, xmax, N)
Y = numpy.linspace(ymin, ymax, N)
Z = numpy.empty((N, N))

for i, y in enumerate(Y):
	for j, x in enumerate(X):
		Z[i, j] = iter_count(complex(x, y), max_iter)

levels = [0, 8, 12, 16, 20, 24, 32]
plot.contourf(X, Y, Z, levels, cmap = cm.gray, antialiased = True)
plot.show()
