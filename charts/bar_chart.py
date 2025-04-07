import matplotlib.pyplot as plt
import mpld3

fig, ax = plt.subplots()
ax.bar(["A", "B", "C"], [4, 7, 3])
ax.set_title("Bar Chart")

html_str = mpld3.fig_to_html(fig)
with open("output/bar_chart.html", "w") as f:
    f.write(html_str)
