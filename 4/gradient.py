import numpy as np
from scipy.optimize import minimize_scalar


# Функция и её градиент
def f(x):
    return -x[0] - 4 * x[1] ** 2 + 2 * x[0] * x[1] + x[0]


def grad_f(x):
    return np.array([-1 + 2 * x[1] + 1, -8 * x[1] + 2 * x[0]])


# Метод градиентного спуска
def gradient_descent(x0, alpha, n_iters):
    x = x0
    history = [[x0, f(x0)]]
    for i in range(n_iters):
        x = x - alpha * grad_f(x)
        history.append([x, f(x)])
    return history


# Начальная точка
x0 = np.array([1.0, 1.0])

alpha = 0.1
max_iter = 10

# Проведем три итерации для каждого метода
history_gradient_descent = gradient_descent(x0, alpha, max_iter)
history_steepest_descent = steepest_descent(x0, max_iter)

print("\nМетод градиентного спуска: \n")
for result in history_gradient_descent:
    print("x1:", result[0][0], "x2:", result[0][1], "function:", result[1])
