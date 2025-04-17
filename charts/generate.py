import os
import numpy as np
import matplotlib.pyplot as plt
import mpld3

# Create output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)


# Helper function to save chart
def save_chart(fig, chart_name, version):
    file_path = os.path.join(output_dir, f"{chart_name}_{version}.html")
    mpld3.save_html(fig, file_path)
    plt.close(fig)


# 1. Line Chart
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 10 if i == 1 else 100)
    ax.plot(x, np.sin(x), label="sin(x)")
    ax.set_title("Line Chart")
    save_chart(fig, "line_chart", i)

# 2. Bar Chart
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.arange(5 if i == 1 else 20)
    y = np.random.randint(1, 10, len(x))
    ax.bar(x, y)
    ax.set_title("Bar Chart")
    save_chart(fig, "bar_chart", i)

# 3. Horizontal Bar Chart
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.arange(5 if i == 1 else 20)
    y = np.random.randint(1, 10, len(x))
    ax.barh(x, y)
    ax.set_title("Horizontal Bar Chart")
    save_chart(fig, "horizontal_bar_chart", i)

# 4. Pie Chart
for i in [1, 2]:
    fig, ax = plt.subplots()
    data = np.random.randint(1, 10, 4 if i == 1 else 8)
    ax.pie(data, labels=[f"Slice {j}" for j in range(len(data))])
    ax.set_title("Pie Chart")
    save_chart(fig, "pie_chart", i)

# 5. Scatter Plot
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.random.rand(10 if i == 1 else 100)
    y = np.random.rand(10 if i == 1 else 100)
    ax.scatter(x, y)
    ax.set_title("Scatter Plot")
    save_chart(fig, "scatter_plot", i)

# 6. Histogram
for i in [1, 2]:
    fig, ax = plt.subplots()
    data = np.random.randn(100 if i == 1 else 1000)
    ax.hist(data, bins=10)
    ax.set_title("Histogram")
    save_chart(fig, "histogram", i)

# 7. Box Plot
for i in [1, 2]:
    fig, ax = plt.subplots()
    data = [np.random.randn(10 if i == 1 else 100) for _ in range(4)]
    ax.boxplot(data)
    ax.set_title("Box Plot")
    save_chart(fig, "box_plot", i)

# 8. Area Chart
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 10 if i == 1 else 100)
    y = np.abs(np.sin(x))
    ax.fill_between(x, y, alpha=0.5)
    ax.set_title("Area Chart")
    save_chart(fig, "area_chart", i)

# 9. Stem Plot
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.arange(10 if i == 1 else 50)
    y = np.random.rand(len(x))
    ax.stem(x, y)
    ax.set_title("Stem Plot")
    save_chart(fig, "stem_plot", i)

# 10. Heatmap (using imshow)
for i in [1, 2]:
    fig, ax = plt.subplots()
    data = np.random.rand(5 if i == 1 else 20, 5 if i == 1 else 20)
    cax = ax.imshow(data, cmap="viridis")
    fig.colorbar(cax)
    ax.set_title("Heatmap")
    save_chart(fig, "heatmap", i)

# 11. Stacked Bar Chart
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.arange(5 if i == 1 else 20)
    y1 = np.random.randint(1, 5, size=len(x))
    y2 = np.random.randint(1, 5, size=len(x))
    ax.bar(x, y1, label="A")
    ax.bar(x, y2, bottom=y1, label="B")
    ax.legend()
    ax.set_title("Stacked Bar Chart")
    save_chart(fig, "stacked_bar_chart", i)

# 12. Polar Plot
for i in [1, 2]:
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    theta = np.linspace(0, 2 * np.pi, 10 if i == 1 else 100)
    r = np.abs(np.sin(theta) * (1 + 0.1 * np.random.randn(len(theta))))
    ax.plot(theta, r)
    ax.set_title("Polar Plot")
    save_chart(fig, "polar_plot", i)

print(f"All charts have been saved in the '{output_dir}' folder.")
