import numpy
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plot


x = numpy.linspace(-3, 3, 256)
y = numpy.linspace(-3, 3, 256)
X, Y = numpy.meshgrid(x, y)
Z = numpy.sinc(numpy.sqrt(X ** 2 + Y ** 2))

fig = plot.figure()
ax = fig.gca(projection = '3d')
ax.plot_wireframe(X, Y, Z, rstride=16, cstride=16)
ax.contour(X, Y, Z, zdir='z', offset=-.2, cmap = cm.BrBG)

plot.show()
