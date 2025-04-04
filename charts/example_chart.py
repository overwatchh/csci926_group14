import matplotlib.pyplot as plt
import mpld3

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 6], marker='o')
ax.set_title('Test Chart')

html_str = mpld3.fig_to_html(fig)

with open('output/example_chart.html', 'w') as f:
    f.write(html_str)
