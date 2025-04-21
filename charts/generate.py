import os
import json
import numpy as np
import matplotlib.pyplot as plt
import mpld3

# Create output directories
output_dir = "output"
data_dir = "test_data"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(data_dir, exist_ok=True)

# Helper function to save chart and data
def save_chart_and_data(fig, chart_name, version, data_dict):
    # Save HTML chart
    html_path = os.path.join(output_dir, f"{chart_name}_{version}.html")
    mpld3.save_html(fig, html_path)
    plt.close(fig)
    
    # Save test data
    data_path = os.path.join(data_dir, f"{chart_name}_{version}.json")
    with open(data_path, 'w') as f:
        json.dump(data_dict, f, indent=2)

# 1. Line Chart
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 10 if i == 1 else 100)
    y = np.sin(x)
    ax.plot(x, y, label="sin(x)")
    ax.set_title("Line Chart")
    save_chart_and_data(fig, "line_chart", i, {
        "chart_type": "line_chart",
        "version": i,
        "x": x.tolist(),
        "y": y.tolist()
    })

# 2. Bar Chart
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.arange(5 if i == 1 else 20)
    y = np.random.randint(1, 10, len(x))
    ax.bar(x, y)
    ax.set_title("Bar Chart")
    save_chart_and_data(fig, "bar_chart", i, {
        "chart_type": "bar_chart",
        "version": i,
        "x": x.tolist(),
        "y": y.tolist()
    })

# 3. Horizontal Bar Chart
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.arange(5 if i == 1 else 20)
    y = np.random.randint(1, 10, len(x))
    ax.barh(x, y)
    ax.set_title("Horizontal Bar Chart")
    save_chart_and_data(fig, "horizontal_bar_chart", i, {
        "chart_type": "horizontal_bar_chart",
        "version": i,
        "x": x.tolist(),
        "y": y.tolist()
    })

# 4. Pie Chart
for i in [1, 2]:
    fig, ax = plt.subplots()
    data = np.random.randint(1, 10, 4 if i == 1 else 8)
    labels = [f"Slice {j}" for j in range(len(data))]
    ax.pie(data, labels=labels)
    ax.set_title("Pie Chart")
    save_chart_and_data(fig, "pie_chart", i, {
        "chart_type": "pie_chart",
        "version": i,
        "data": data.tolist(),
        "labels": labels
    })

# 5. Scatter Plot
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.random.rand(10 if i == 1 else 100)
    y = np.random.rand(10 if i == 1 else 100)
    ax.scatter(x, y)
    ax.set_title("Scatter Plot")
    save_chart_and_data(fig, "scatter_plot", i, {
        "chart_type": "scatter_plot",
        "version": i,
        "x": x.tolist(),
        "y": y.tolist()
    })

# 6. Histogram
for i in [1, 2]:
    fig, ax = plt.subplots()
    data = np.random.randn(100 if i == 1 else 1000)
    counts, bins = np.histogram(data, bins=10)
    ax.hist(data, bins=10)
    ax.set_title("Histogram")
    save_chart_and_data(fig, "histogram", i, {
        "chart_type": "histogram",
        "version": i,
        "data": data.tolist(),
        "counts": counts.tolist(),
        "bins": bins.tolist()
    })

# 7. Box Plot
for i in [1, 2]:
    fig, ax = plt.subplots()
    data = [np.random.randn(10 if i == 1 else 100) for _ in range(4)]
    ax.boxplot(data)
    ax.set_title("Box Plot")
    save_chart_and_data(fig, "box_plot", i, {
        "chart_type": "box_plot",
        "version": i,
        "data": [d.tolist() for d in data]
    })

# 8. Area Chart
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.linspace(0, 10, 10 if i == 1 else 100)
    y = np.abs(np.sin(x))
    ax.fill_between(x, y, alpha=0.5)
    ax.set_title("Area Chart")
    save_chart_and_data(fig, "area_chart", i, {
        "chart_type": "area_chart",
        "version": i,
        "x": x.tolist(),
        "y": y.tolist()
    })

# 9. Stem Plot
for i in [1, 2]:
    fig, ax = plt.subplots()
    x = np.arange(10 if i == 1 else 50)
    y = np.random.rand(len(x))
    ax.stem(x, y)
    ax.set_title("Stem Plot")
    save_chart_and_data(fig, "stem_plot", i, {
        "chart_type": "stem_plot",
        "version": i,
        "x": x.tolist(),
        "y": y.tolist()
    })

# 10. Heatmap
for i in [1, 2]:
    fig, ax = plt.subplots()
    data = np.random.rand(5 if i == 1 else 20, 5 if i == 1 else 20)
    cax = ax.imshow(data, cmap="viridis")
    fig.colorbar(cax)
    ax.set_title("Heatmap")
    save_chart_and_data(fig, "heatmap", i, {
        "chart_type": "heatmap",
        "version": i,
        "data": data.tolist()
    })

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
    save_chart_and_data(fig, "stacked_bar_chart", i, {
        "chart_type": "stacked_bar_chart",
        "version": i,
        "x": x.tolist(),
        "y1": y1.tolist(),
        "y2": y2.tolist()
    })

# 12. Polar Plot
for i in [1, 2]:
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    theta = np.linspace(0, 2 * np.pi, 10 if i == 1 else 100)
    r = np.abs(np.sin(theta) * (1 + 0.1 * np.random.randn(len(theta))))
    ax.plot(theta, r)
    ax.set_title("Polar Plot")
    save_chart_and_data(fig, "polar_plot", i, {
        "chart_type": "polar_plot",
        "version": i,
        "theta": theta.tolist(),
        "r": r.tolist()
    })

print(f"All charts have been saved in the '{output_dir}' folder.")
print(f"All test data has been saved in the '{data_dir}' folder.")