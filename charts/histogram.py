import matplotlib.pyplot as plt
import mpld3

data = [1, 2, 2, 3, 3, 3, 4, 4, 5]
fig, ax = plt.subplots()
ax.hist(data, bins=5)
ax.set_title("Histogram")

html_str = mpld3.fig_to_html(fig)
with open("output/histogram.html", "w") as f:
    f.write(html_str)
