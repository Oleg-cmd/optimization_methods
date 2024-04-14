import numpy as np
import matplotlib.pyplot as plt


# Define the inequalities as functions
def inequality1(x1):
    return (12 + 2 * x1) / 3


def inequality2(x1):
    return 2 - x1


def inequality3(x1):
    return 4 - 0.5 * x1


# Create a range of values for x1
x1 = np.linspace(0, 10, 400)

# Plot the inequalities
plt.figure(figsize=(10, 10))
plt.axvline(0, color="0", lw=1)
plt.axhline(0, color="0", lw=1)

# Fill the feasible region
plt.fill_between(
    x1,
    np.maximum(inequality1(x1), inequality2(x1)),
    inequality3(x1),
    where=(inequality1(x1) >= inequality2(x1)) & (x1 + 2 * inequality3(x1) <= 24),
    color="gray",
    alpha=0.5,
)

# Plot the lines for each inequality
plt.plot(x1, inequality1(x1), label=r"$2x_1 - 3x_2 \geq 12$")
plt.plot(x1, inequality2(x1), label=r"$x_1 + x_2 \geq 2$")
plt.plot(x1, inequality3(x1), label=r"$3x_1 + 6x_2 \leq 24$")

# Add labels and legends
plt.xlim(0, 10)
plt.ylim(0, 10)
plt.xlabel(r"$x_1$")
plt.ylabel(r"$x_2$")
plt.legend()
plt.title("Feasible Region for the Linear Programming Problem")

# Find corner points
corners = [(0, inequality2(0)), (0, inequality3(0)), (2, 0), (4, 0), (6 / 5, 8 / 5)]

# Evaluate objective function at corner points
objective_values = [(-2 * x[0] - 3 * x[1]) for x in corners]

# Plot the corner points
for point in corners:
    plt.plot(*point, "ro")

plt.show()

# Return the corner points and their corresponding objective function values
print(corners, objective_values)
