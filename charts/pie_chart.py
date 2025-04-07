import matplotlib.pyplot as plt
import mpld3

fig, ax = plt.subplots()
ax.pie([30, 40, 30], labels=["A", "B", "C"], autopct="%1.1f%%")
ax.set_title("Pie Chart")

html_str = mpld3.fig_to_html(fig)
with open("output/pie_chart.html", "w") as f:
    f.write(html_str)
