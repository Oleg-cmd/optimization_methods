from sympy import symbols, diff, lambdify

# for equation

a = 3
b = 1.7
c = -15.42
k = 6.89

fault = 0.01  #


def func(x):
    return a * (x**3) + b * (x**2) + c * x + k


# n - count of iterations
n = 0


# метод половинного деления
def halving(a, b, n):
    x = (a + b) / 2

    if func(a) * func(x) > 0:
        a = x
    else:
        b = x

    n = n + 1

    if abs(a - b) <= fault or abs(func(x)) < fault:
        x = (a + b) / 2
        return [x, func(x), n]
    else:
        return halving(a, b, n)


print(halving(-3, -2, n))


# метод ньютона
def newton_method(func, initial_guess, fault, max_iter=100):
    x = symbols("x")
    df = lambdify(x, diff(func(x), x))  # Производная функции

    n = 0
    while n < max_iter:
        x_new = initial_guess - func(initial_guess) / df(initial_guess)
        if abs(x_new - initial_guess) < fault:
            return x_new, n
        initial_guess = x_new
        n += 1
    return None


initial_guess = 10000  # Начальное приближение

root, newton_n = newton_method(func, initial_guess, fault)
if root is not None:
    print("Корень уравнения Ньютон:", root)
    print("Количество итераций:", newton_n)
else:
    print("Не удалось найти корень уравнения")


def falaise_iteration(f, x):
    x_sym = symbols("x")
    f_prime = diff(f, x_sym)  # Производная функции
    f_lambda = lambdify(x_sym, f, modules="numpy")  # Используем numpy
    f_prime_lambda = lambdify(x_sym, f_prime, modules="numpy")  # Используем numpy

    return lambda x: x - f_lambda(x) / f_prime_lambda(x)


def simple_iteration_method(g, initial_guess, tol=1e-6, max_iter=100):
    x = initial_guess
    n = 0
    while n < max_iter:
        x_new = g(x)
        if abs(x_new - x) < tol:
            return x_new, n
        x = x_new
        n += 1
    return None


def create_symbolic_function(a, b, c, k):
    x = symbols("x")
    return a * (x**3) + b * (x**2) + c * x + k


g = falaise_iteration(
    create_symbolic_function(a, b, c, k), symbols("x")
)  # определяем функцию g(x)

initial_guess = 2  # начальное приближение

root, simple_n = simple_iteration_method(g, initial_guess)
if root is not None:
    print("Корень уравнения:", root)
    print("Количество итераций:", simple_n)
else:
    print("Не удалось найти корень уравнения")
