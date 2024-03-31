from sympy import symbols, diff, lambdify
import math

a = 1
b = 1.5
fault = 0.05


def func(x):
    return (x**7) / 7 - x**3 + (x**2) / 2 - x


def halving_with_steps(func, a, b, fault, direction="min", max_iter=100):
    n = 0
    x = (a + b) / 2

    print("Шаг\t a\t\t\t b\t\t\t x\t\t\t f'(x)")
    print("-" * 60)
    while n < max_iter:
        # print(f"{n+1}\t {a:.10f}\t {b:.10f}\t {x:.10f}\t {fx:.10f}")
        x1, x2 = (a + b - fault) / 2, (a + b + fault) / 2
        y1, y2 = (func(x1), func(x2))
        if y1 > y2:
            a = x1
        else:
            b = x2

        if abs(b - a) < fault * 2:
            return x, func(x), n
        n += 1


root, halving_result, halving_n = halving_with_steps(func, a, b, fault, "min")
print("-" * 60)
print("Экстремум функции (метод половинного деления):", root)
print("Значение функции в точке:", halving_result)
print("Количество итераций:", halving_n, "\n")


def golden_section_with_steps(func, a, b, fault, direction="min", max_iter=10000):
    n = 0
    x_symbol = symbols("x")
    golden_ratio = (3 - math.sqrt(5)) / 2

    print("Шаг\t a\t\t\t b\t\t\t x1\t\t\t x2\t\t\t f(x1)\t\t\t f(x2)")
    print("-" * 80)
    while n < max_iter:
        x1, x2 = a + 0.382 * (b - a), a + 0.618 * (b - a)
        y1, y2 = func(x1), func(x2)
        # print(
        #     f"{n+1}\t {a:.10f}\t {b:.10f}\t {x1:.10f}\t {x2:.10f}\t {fx1:.10f}\t {fx2:.10f}"
        # )
        if y1 >= y2:
            a = x1
            x1 = x2
            y1 = func(x1)
            x2 = a + 0.618 * (b - a)
        else:
            b = x2
            x2 = x1
            y2 = func(x2)
            x1 = a + 0.382 * (b - a)

        x = (a + b) / 2
        if abs(b - a) < fault:
            return x, func(x), n

        n += 1
    print("Метод золотого сечения не смог найти экстремум за", max_iter, "итераций.")
    return None, None, n + 1


root, golden_result, golden_n = golden_section_with_steps(
    func, a, b, fault, direction="min"
)
print("-" * 80)
print("Экстремум функции (метод золотого сечения):", root)
print("Значение функции в точке:", golden_result)
print("Количество итераций:", golden_n, "\n")


def chord_with_steps(func, a, b, fault, max_iter=100):
    n = 0
    x_symbol = symbols("x")
    f_prime = lambdify(x_symbol, diff(func(x_symbol), x_symbol))  # Производная функции

    print("Шаг\t a\t\t\t b\t\t\t x\t\t\t f(x)")
    print("-" * 60)
    while n < max_iter:
        x = a - (f_prime(a) / (f_prime(a) - f_prime(b)) * (a - b))
        fx = func(x)
        print(f"{n+1}\t {a:.10f}\t {b:.10f}\t {x:.10f}\t {fx:.10f}")

        if abs(f_prime(x)) <= fault:
            print(f"Значение производной в точке x: {f_prime(x)}")
            return x, fx, n + 1

        if f_prime(a) * f_prime(x) < 0:
            b = x
        else:
            a = x

        n += 1

    print("Достигнуто максимальное количество итераций.")
    return None, None, n + 1


root, chord_result, chord_n = chord_with_steps(func, a, b, fault)
print("-" * 60)
print("Экстремум функции (метод хорд):", root)
print("Значение функции в точке:", chord_result)
print("Количество итераций:", chord_n, "\n")

initial_guess = (a + b) / 2  # Начальное приближение


def newton_with_steps(func, a, b, fault, direction="min", max_iter=100):
    x = symbols("x")
    df = lambdify(x, diff(func(x), x))  # Производная функции
    ddf = lambdify(x, diff(df(x), x))  # Производная второй степени

    n = 0
    print("Шаг\t a\t\t\t b\t\t\t x1\t\t\t x2\t\t\t f(x1)\t\t\t f(x2)")
    print("-" * 80)

    if func(a) * ddf(a) > 0:
        x = a
    else:
        x = b

    while n < max_iter:
        x = x - df(x) / ddf(x)
        if abs(df(x)) <= fault:
            return x, func(x), n
        n += 1

    print("Достигнуто максимальное количество итераций.")
    return None, None


root, newton_result, newton_n = newton_with_steps(func, a, b, fault, direction="min")
print("-" * 50)
print("Экстремум функции (метод Ньютона):", root)
print("Значение функции в точке:", newton_result)
print("Количество итераций:", newton_n, "\n")
