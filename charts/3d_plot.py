import matplotlib.pyplot as plt
import mpld3
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
X = np.linspace(-5, 5, 50)
Y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(X, Y)
Z = np.sin(np.sqrt(X**2 + Y**2))
ax.plot_surface(X, Y, Z, cmap="viridis")

ax.set_title("3D Surface Plot")
html_str = mpld3.fig_to_html(fig)
with open("output/3d_plot.html", "w") as f:
    f.write(html_str)
