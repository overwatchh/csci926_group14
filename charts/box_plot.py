import matplotlib.pyplot as plt
import mpld3

data = [[7, 8, 9, 5, 6], [3, 4, 5, 2, 1]]
fig, ax = plt.subplots()
ax.boxplot(data)
ax.set_title("Box Plot")

html_str = mpld3.fig_to_html(fig)
with open("output/box_plot.html", "w") as f:
    f.write(html_str)
