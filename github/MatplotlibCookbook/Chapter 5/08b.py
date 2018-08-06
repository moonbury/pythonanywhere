import numpy
import matplotlib.pyplot as plot

theta = numpy.linspace(0, 2 * numpy.pi, 8)
points = list(zip(numpy.cos(theta), numpy.sin(theta)))

plot.figure(figsize=(8., 8.))
plot.gca().add_patch(plot.Polygon(points, color = '.75'))

plot.grid(True)
plot.axis('scaled')

plot.savefig('polygon-b.png', dpi = 64)
