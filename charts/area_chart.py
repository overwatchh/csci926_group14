import matplotlib.pyplot as plt
import mpld3

x = [1, 2, 3, 4]
y = [1, 4, 2, 3]
fig, ax = plt.subplots()
ax.fill_between(x, y, alpha=0.5)
ax.plot(x, y, marker="o")
ax.set_title("Area Chart")

html_str = mpld3.fig_to_html(fig)
with open("output/area_chart.html", "w") as f:
    f.write(html_str)
