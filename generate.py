import matplotlib.pyplot as plt
import mpld3
import mpld3.plugins as plugins
import numpy as np
from pathlib import Path
import matplotlib.patches as mpatches
from math import pi, sin, cos, exp, sqrt, log

# Create output directory
output_dir = Path("html_charts")
output_dir.mkdir(exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

# Generate common data
x = np.linspace(0, 10, 20)
y = np.sin(x) * np.exp(-x/10)

# 1. Area Chart

def create_area_chart():
    formulas = [
        ("y = x * np.sin(x)", lambda x: x * np.sin(x)),
        ("y = np.minimum(x, 5)", lambda x: np.minimum(x, 5)),
        ("y = np.sqrt(x)", lambda x: np.sqrt(x)),
        ("y = np.log(x + 1)", lambda x: np.log(x + 1)),
        ("y = 1 - np.exp(-x)", lambda x: 1 - np.exp(-x)),
        ("y = x - (x**3)/6", lambda x: x - (x**3)/6),
        ("y = np.floor(x)", lambda x: np.floor(x)),
        ("y = x % 3", lambda x: x % 3),
        ("y = np.abs(np.sin(x))", lambda x: np.abs(np.sin(x))),
        ("y = x / (1 + x)", lambda x: x / (1 + x)),
    ]

    for i, (label, func) in enumerate(formulas, 1):
        x = np.linspace(0, 10, 100)
        y = func(x)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.fill_between(x, y, alpha=0.5)
        ax.plot(x, y, 'r')
        ax.set_title(f"Area {i}: {label}")

        filename = f"area_{i:02d}.html"
        mpld3.save_html(fig, (output_dir / filename).as_posix())
        plt.close(fig)


# 2. Bar Chart
def create_bar_chart():
    categories = [f'Cat{i}' for i in 'ABCDEFGHIJ']
    formulas = [
        "y = [3,7,2,5,8,1,4,9,6,2]",
        "y = [i² for i in range(10)]",
        "y = [5sin(i) for i in range(10)]",
        "y = Fibonacci mod 7",
        "y = Primes <30",
        "y = Random 1-10",
        "y = Triangular nums",
        "y = [10-abs(i-5) for i in range(10)]",
        "y = Digitsofπ",
        "y = Binary weights"
    ]
    values = [
        [3,7,2,5,8,1,4,9,6,2],
        [i**2 for i in range(10)],
        [int(5*sin(i)) for i in range(10)],
        [1,1,2,3,5,1,6,0,6,6],
        [2,3,5,7,11,13,17,19,23,29],
        np.random.randint(1,11,10),
        [1,3,6,10,15,21,28,36,45,55],
        [10-abs(i-5) for i in range(10)],
        [3,1,4,1,5,9,2,6,5,3],
        [1,2,4,8,16,32,64,128,256,512]
    ]
    
    for i, (formula, y) in enumerate(zip(formulas, values), 1):
        fig, ax = plt.subplots(figsize=(10,6))
        bars = ax.bar(categories, y)
        ax.set_title(f"Bar {i}: {formula}")
        
        # Tooltips
        tt = [f'{cat}\nval={val}' for cat,val in zip(categories,y)]
        plugins.connect(fig, plugins.PointLabelTooltip(bars, labels=tt))
        
        filename = f"bar_{i:02d}.html"
        mpld3.save_html(fig, (output_dir / filename).as_posix())
        plt.close(fig)

# 3. Box Plot


def create_box_plot():
    data = [np.random.normal(0, std, 100) for std in range(1, 4)]
    fig, ax = plt.subplots(figsize=(10, 6))
    box = ax.boxplot(data, patch_artist=True)
    ax.set_title("Box Plot\nData: Normal distributions (μ=0, σ=1-3)")
    ax.set_xticklabels(['σ=1', 'σ=2', 'σ=3'])

    # Customize colors
    colors = ['lightblue', 'lightgreen', 'pink']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)

    # Create legend
    patches = [mpatches.Patch(color=color, label=label)
               for color, label in zip(colors, ['σ=1', 'σ=2', 'σ=3'])]
    ax.legend(handles=patches)

    mpld3.save_html(fig, str(output_dir / "box_plot.html"))
    plt.close(fig)

# 4. Error Bar Chart


def create_error_bar_chart():
    x_err = np.random.uniform(0.1, 0.3, len(x))
    y_err = np.random.uniform(0.1, 0.3, len(y))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(x, y, xerr=x_err, yerr=y_err, fmt='-o',
                label='y = sin(x) * e^(-x/10) ± error')
    ax.set_title("Error Bar Chart\nFunction with random errors")
    ax.legend()
    mpld3.save_html(fig, str(output_dir / "error_bar_chart.html"))
    plt.close(fig)

# 5. Heat Map


def create_heatmap():
    formulas = [
        "z = np.sin(X) + np.cos(Y)",
        "z = X**2 - Y**2",
        "z = np.exp(-(X**2 + Y**2)/10)",
        "z = np.sin(X**2 + Y**2)",
        "z = np.abs(X) + np.abs(Y)",
        "z = np.sin(X) * np.cos(Y)",
        "z = np.log(X**2 + Y**2 + 1)",
        "z = np.tanh(X + Y)",
        "z = np.maximum(0, 1 - np.sqrt(X**2 + Y**2))",
        "z = (X % 3) * (Y % 2)"
    ]

    for i, formula in enumerate(formulas, 1):
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)

        try:
            Z = eval(formula.split('=')[1].strip(), {"np": np, "X": X, "Y": Y})
        except Exception as e:
            print(f"Failed to evaluate formula {formula}: {e}")
            continue

        fig, ax = plt.subplots(figsize=(10, 6))
        im = ax.imshow(Z, cmap='viridis', extent=(-5, 5, -5, 5), origin='lower')
        ax.set_title(f"Heatmap {i}: {formula}")
        fig.colorbar(im, ax=ax)

        filename = f"heatmap_{i:02d}.html"
        mpld3.save_html(fig, (output_dir / filename).as_posix())
        plt.close(fig)


# 6. Histogram


def create_histogram():
    formulas = [
        "N(0,1)",
        "N(2,0.5)",
        "Exp(λ=1)",
        "Poisson(λ=3)",
        "U(0,1)",
        "χ²(k=3)",
        "Beta(α=2,β=5)",
        "Gamma(k=2,θ=2)",
        "LogNormal(μ=0,σ=1)",
        "Weibull(λ=1,k=1.5)"
    ]
    generators = [
        lambda: np.random.normal(0,1,1000),
        lambda: np.random.normal(2,0.5,1000),
        lambda: np.random.exponential(1,1000),
        lambda: np.random.poisson(3,1000),
        lambda: np.random.uniform(0,1,1000),
        lambda: np.random.chisquare(3,1000),
        lambda: np.random.beta(2,5,1000),
        lambda: np.random.gamma(2,2,1000),
        lambda: np.random.lognormal(0,1,1000),
        lambda: np.random.weibull(1.5,1000)
    ]
    
    for i, (formula, gen) in enumerate(zip(formulas, generators), 1):
        data = gen()
        fig, ax = plt.subplots(figsize=(10,6))
        ax.hist(data, bins=30, density=True)
        ax.set_title(f"Histogram {i}: {formula}")
        
        filename = f"histogram_{i:02d}.html"
        mpld3.save_html(fig, (output_dir / filename).as_posix())
        plt.close(fig)

# 7. Line Chart


def create_line_chart():
    formulas = [
        ("y = x * np.sin(x)", lambda x: x * np.sin(x)),
        ("y = np.minimum(x, 5)", lambda x: np.minimum(x, 5)),
        ("y = np.sqrt(x)", lambda x: np.sqrt(x)),
        ("y = np.log(x + 1)", lambda x: np.log(x + 1)),
        ("y = 1 - np.exp(-x)", lambda x: 1 - np.exp(-x)),
        ("y = x - (x**3)/6", lambda x: x - (x**3)/6),
        ("y = np.floor(x)", lambda x: np.floor(x)),
        ("y = x % 3", lambda x: x % 3),
        ("y = np.abs(np.sin(x))", lambda x: np.abs(np.sin(x))),
        ("y = x / (1 + x)", lambda x: x / (1 + x)),
    ]
    
    for i, (label, func) in enumerate(formulas, 1):
        x = np.linspace(0, 10, 100)
        y = func(x)
        
        fig, ax = plt.subplots(figsize=(10,6))
        line, = ax.plot(x, y)
        ax.set_title(f"Line {i}: {label}")
        
        # Tooltips
        idx = np.linspace(0, len(x)-1, 15, dtype=int)
        tt = [f'x={x[j]:.2f}\ny={y[j]:.2f}' for j in idx]
        plugins.connect(fig, plugins.PointLabelTooltip(line, labels=tt))
        
        filename = f"line_{i:02d}.html"
        mpld3.save_html(fig, (output_dir / filename).as_posix())
        plt.close(fig)

# 8. Pie Chart

def create_pie_chart():

    formulas = [
        "π digits distribution",
        "Prime number classes",
        "Fibonacci sequence mod 5",
        "Planetary mass distribution",
        "Electron orbital probabilities",
        "Element abundance in crust",
        "Blood type distribution",
        "RGB color composition",
        "Music genre preferences",
        "Planetary atmospheric composition"
    ]
    datasets = [
        [3,1,4,1,5,9,2,6,5,3],
        [1,2,3,1],
        [1,1,2,3,0],
        [330,4.87,5.97,0.642],
        [2,6,10,14],
        [46.6,27.7,8.1,5.0],
        [37,35,8,20],
        [0.3,0.59,0.11],
        [30,25,20,15,10],
        [78,21,0.9,0.1]
    ]
    labels = [
        ['3','1','4','1','5','9','2','6','5','3'],
        ['Primes ≡1','≡3','≡7','≡9'],
        ['F(n)≡0','≡1','≡2','≡3','≡4'],
        ['Earth','Venus','Mars','Mercury'],
        ['s','p','d','f'],
        ['O','Si','Al','Fe'],
        ['O+','A+','B+','AB+'],
        ['Red','Green','Blue'],
        ['Pop','Rock','Classical','Jazz','HipHop'],
        ['N₂','O₂','Ar','CO₂']
    ]

    for i, (formula, data, lbls) in enumerate(zip(formulas, datasets, labels), 1):
        fig, ax = plt.subplots(figsize=(10, 6))
        wedges, texts, autotexts = ax.pie(data, labels=lbls, autopct='%1.1f%%', startangle=90)
        ax.set_title(f"Pie {i}: {formula}")
        ax.axis('equal')

        tt = [f'{l}: {d}' for l, d in zip(lbls, data)]
        tooltip = plugins.PointLabelTooltip(wedges, labels=tt)
        plugins.connect(fig, tooltip)

        filename = f"pie_{i:02d}.html"
        mpld3.save_html(fig, (output_dir / filename).as_posix())
        plt.close(fig)


# 9. Polar Plot


def create_polar_plot():
    r = np.arange(0, 3, 0.01)
    theta = 2 * np.pi * r
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, polar=True)
    line = ax.plot(theta, r, label='Archimedean spiral: r = θ/2π')
    ax.set_title("Polar Plot\nArchimedean Spiral", pad=20)
    ax.legend(loc='upper right')
    mpld3.save_html(fig, str(output_dir / "polar_plot.html"))
    plt.close(fig)

# 10. Stacked Bar Chart


def create_stacked_bar_chart():
    formulas = [
        "N(μ=0,σ=1) vs N(0,2) vs N(1,1)",
        "Exp(λ=1) vs Exp(λ=2)",
        "U(0,1) vs U(-1,1)",
        "Poisson(λ=3) vs Poisson(λ=6)",
        "χ²(k=2) vs χ²(k=5)",
        "Beta(α=2,β=2) vs Beta(α=0.5,β=0.5)",
        "Gamma(k=1,θ=2) vs Gamma(k=2,θ=2)",
        "LogNormal(μ=0,σ=1) vs LogNormal(μ=1,σ=0.5)",
        "Weibull(λ=1,k=1.5) vs Weibull(λ=1,k=3)",
        "Pareto(α=1) vs Pareto(α=3)"
    ]
    datasets = [
        [np.random.normal(0,1,100), np.random.normal(0,2,100), np.random.normal(1,1,100)],
        [np.random.exponential(1,100), np.random.exponential(0.5,100)],
        [np.random.uniform(0,1,100), np.random.uniform(-1,1,100)],
        [np.random.poisson(3,100), np.random.poisson(6,100)],
        [np.random.chisquare(2,100), np.random.chisquare(5,100)],
        [np.random.beta(2,2,100), np.random.beta(0.5,0.5,100)],
        [np.random.gamma(1,2,100), np.random.gamma(2,2,100)],
        [np.random.lognormal(0,1,100), np.random.lognormal(1,0.5,100)],
        [np.random.weibull(1.5,100), np.random.weibull(3,100)],
        [np.random.pareto(1,100), np.random.pareto(3,100)]
    ]
    
    for i, (formula, data) in enumerate(zip(formulas, datasets), 1):
        fig, ax = plt.subplots(figsize=(10,6))
        box = ax.boxplot(data, patch_artist=True, labels=[f'Dataset {j+1}' for j in range(len(data))])
        
        # Color boxes
        colors = plt.cm.tab10(np.linspace(0,1,len(data)))
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)
        
        ax.set_title(f"Boxplot {i}: {formula}")
        
        filename = f"boxplot_{i:02d}.html"
        mpld3.save_html(fig, (output_dir / filename).as_posix())
        plt.close(fig)

# 11. Scatter Plot (NEW)


def create_scatter_plot():
    formulas = [
        ("y = x * np.sin(x)", lambda x: x * np.sin(x)),
        ("y = np.minimum(x, 5)", lambda x: np.minimum(x, 5)),
        ("y = np.sqrt(x)", lambda x: np.sqrt(x)),
        ("y = np.log(x + 1)", lambda x: np.log(x + 1)),
        ("y = 1 - np.exp(-x)", lambda x: 1 - np.exp(-x)),
        ("y = x - (x**3)/6", lambda x: x - (x**3)/6),
        ("y = np.floor(x)", lambda x: np.floor(x)),
        ("y = x % 3", lambda x: x % 3),
        ("y = np.abs(np.sin(x))", lambda x: np.abs(np.sin(x))),
        ("y = x / (1 + x)", lambda x: x / (1 + x)),
    ]
    
    for i, (label, func) in enumerate(formulas, 1):
        x = np.linspace(0, 10, 100)
        y = func(x) 
        
        fig, ax = plt.subplots(figsize=(10,6))
        sc = ax.scatter(x, y, c=np.abs(x), cmap='viridis')
        ax.set_title(f"Scatter {i}: {label}")
        
        # Tooltips
        tt = [f'x={xi:.2f}\ny={yi:.2f}' for xi,yi in zip(x,y)]
        plugins.connect(fig, plugins.PointLabelTooltip(sc, labels=tt))
        
        filename = f"scatter_{i:02d}.html"
        mpld3.save_html(fig, (output_dir / filename).as_posix())
        plt.close(fig)


# Generate all charts
chart_functions = [
    create_area_chart,
    create_bar_chart,
    create_box_plot,
    create_error_bar_chart,
    create_heatmap,
    create_histogram,
    create_line_chart,
    create_pie_chart,
    create_polar_plot,
    create_stacked_bar_chart,
    create_scatter_plot
]

for i, func in enumerate(chart_functions, 1):
    func()
    print(f"Generated chart {i} of {len(chart_functions)}")

print(
    f"\nAll {len(chart_functions)} charts generated in '{output_dir}' directory!")
print("Includes 11 chart types with mathematical formulas and interactivity")
