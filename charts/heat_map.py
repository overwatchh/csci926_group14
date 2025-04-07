import matplotlib.pyplot as plt
import mpld3
import numpy as np

data = np.array([[1, 2, 3], [4, 5, 6]])
fig, ax = plt.subplots()
cax = ax.imshow(data, cmap="viridis")
fig.colorbar(cax)
ax.set_title("Heatmap")

html_str = mpld3.fig_to_html(fig)
with open("output/heatmap.html", "w") as f:
    f.write(html_str)
