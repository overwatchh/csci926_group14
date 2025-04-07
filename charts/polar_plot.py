import matplotlib.pyplot as plt
import mpld3
import numpy as np

theta = np.linspace(0, 2 * np.pi, 100)
r = np.abs(np.sin(theta))

fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
ax.plot(theta, r)
ax.set_title("Polar Plot")

html_str = mpld3.fig_to_html(fig)
with open("output/polar_plot.html", "w") as f:
    f.write(html_str)
