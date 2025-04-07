import matplotlib.pyplot as plt
import mpld3

fig, ax = plt.subplots()
ax.scatter([1, 2, 3], [4, 5, 6])
ax.set_title("Scatter Plot")

html_str = mpld3.fig_to_html(fig)
with open("output/scatter_plot.html", "w") as f:
    f.write(html_str)
