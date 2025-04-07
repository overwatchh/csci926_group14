import matplotlib.pyplot as plt
import mpld3

labels = ["A", "B", "C"]
val1 = [3, 2, 5]
val2 = [4, 1, 2]

fig, ax = plt.subplots()
ax.bar(labels, val1, label="Group 1")
ax.bar(labels, val2, bottom=val1, label="Group 2")
ax.set_title("Stacked Bar Chart")
ax.legend()

html_str = mpld3.fig_to_html(fig)
with open("output/stacked_bar_chart.html", "w") as f:
    f.write(html_str)
