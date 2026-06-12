import numpy as np
import pub_style
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.datasets import load_iris

iris_data = load_iris()
X_data = iris_data.data
y_target = iris_data.target

feature_names = iris_data.feature_names
target_names = iris_data.target_names

x_col = 0
y_col = 1

polynomial_degree = 2

datasets_to_plot = ["setosa", "virginica"]

pub_style.use()
fig, ax = pub_style.new_figure(minor_ticks=True, despine=False, ratio=1)

ax.set_xlabel(f"{feature_names[x_col].capitalize()}")
ax.set_ylabel(f"{feature_names[y_col].capitalize()}")

# ax.grid(True, which="major", linestyle="-", linewidth=0.5, alpha=0.6)
# ax.grid(True, which="minor", linestyle="-", linewidth=0.4, alpha=0.3)
# ax.set_axisbelow(True)
pub_style.griddify() # griddify does all of the above!

markers = ['o', 's', 'D']

# # And the colour for the lines (regressions):
# regression_color = "#8a8a8a"  # <-- neutral grey
regression_color = 'k'
# regression_color = '#7f9fa1' # <-- greyish seafoam

# # Plotting in a loop for each dataset:
all_data_x_to_plot = []
all_data_y_to_plot = []
regression_flag = 0  # control plotting of regression labels
for class_name in datasets_to_plot:
    class_index = list(target_names).index(class_name)  # Get correct label
    class_mask = y_target == class_index
    data_x = X_data[class_mask, x_col].reshape(-1, 1)
    data_y = X_data[class_mask, y_col]

    # Scatter plot:
    ax.scatter(
        data_x,
        data_y,
        label=class_name.capitalize(),
        s=20,
        # color = dataset_colors[class_index],
        # edgecolors=dataset_line_colors[class_index],
        edgecolors='k',
        marker=markers[class_index],
        # linewidths = 1.5,
        zorder=3,
        alpha=0.7,
    )

    # Linear regression:
    lin_model = LinearRegression().fit(data_x, data_y)
    x_range = np.linspace(data_x.min() - 2.0, data_x.max() + 2.0, 100).reshape(-1, 1)
    y_pred_linear = lin_model.predict(x_range)
    ax.plot(
        x_range,
        y_pred_linear,
        label="LR" if regression_flag == 0 else "_nolegend_",
        # linewidth = 2.6,
        color=regression_color,
        zorder=2,  # use the z-order to force scatter to be displayed over lines
    )

    # Polynomial regression:
    poly = PolynomialFeatures(polynomial_degree)
    data_x_poly = poly.fit_transform(data_x)
    poly_model = LinearRegression().fit(data_x_poly, data_y)
    x_range_poly = poly.transform(x_range)
    y_pred_poly = poly_model.predict(x_range_poly)
    ax.plot(
        x_range,
        y_pred_poly,
        label="PR" if regression_flag == 0 else "_nolegend_",
        # linewidth = 2.6,
        color=regression_color,
        linestyle="--",
        zorder=2,
    )

    # Tracking which data we plot to adjust plotting limits later:
    all_data_x_to_plot.extend(data_x)
    all_data_y_to_plot.extend(data_y)

    regression_flag += 1

# After the loop, replace ax.margins(0) with:
x_min, x_max = np.min(all_data_x_to_plot), np.max(all_data_x_to_plot)
y_min, y_max = np.min(all_data_y_to_plot), np.max(all_data_y_to_plot)

ax.set_xlim(x_min - 0.5, x_max + 0.5)
ax.set_ylim(y_min - 0.5, y_max + 0.5)
ax.legend()

fig.savefig("regresfigure")
