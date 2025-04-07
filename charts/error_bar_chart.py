import matplotlib.pyplot as plt
import mpld3

x = [1, 2, 3]
y = [2, 4, 6]
errors = [0.5, 0.2, 0.3]

fig, ax = plt.subplots()
ax.errorbar(x, y, yerr=errors, fmt="o")
ax.set_title("Error Bar Chart")

html_str = mpld3.fig_to_html(fig)
with open("output/error_bar_chart.html", "w") as f:
    f.write(html_str)
