from sympy import symbols, diff, lambdify
import math

a = 1
b = 2
fault = 0.05


def func(x):
    return (x**7) / 7 - x**3 + (x**2) / 2 - x


def halving_with_steps(a, b, fault, max_iter=100):
    n = 0
    while n < max_iter:
        x = (a + b) / 2
        print(f"x =  (a + b) / 2 = {a:.3f}+{b:.3f} / 2 = {x:.3f}")
        fx = func(x)
        if abs(a - b) <= fault or abs(fx) < fault:
            print(f"a - b = {a:.3f} - {b:.3f} = {a - b:.3f} <= fault = {fault:.3f}")
            return x, fx, n + 1

        prod = func(a) * fx
        if prod > 0:
            a = x
            print(f"func(a) * fx = {func(a):.3f} * {fx:.3f} = {prod:.3f} > 0")
            print(f"a = x = {a:.3f}")
        else:
            b = x
            print(f"func(a) * fx = {func(a):.3f} * {fx:.3f} = {prod:.3f} < 0")
            print(f"b = x = {b:.3f}")

        n += 1
        print("\n")

    return None


root, halving_result, halving_n = halving_with_steps(a, b, fault)
print("-" * 60)
print("Корень уравнения (метод половинного деления):", root)
print("Значение функции в корне:", halving_result)
print("Количество итераций:", halving_n, "\n")


def golden_section_with_steps(a, b, fault, max_iter=10000):
    n = 0
    golden_ratio = (3 - math.sqrt(5)) / 2

    while n < max_iter:
        x1 = a + golden_ratio * (b - a)
        print(
            f" x1 = a + golden_ratio * (b - a) = {a:.3f} + {golden_ratio:.3f} * ({b:.3f} - {a:.3f}) = {x1:.3f}"
        )
        x2 = a + (1 - golden_ratio) * (b - a)
        print(
            f" x2 = a + (1 - golden_ratio) * (b - a) = {a:.3f} + ({1 - golden_ratio:.3f}) * ({b:.3f} - {a:.3f}) = {x2:.3f}"
        )

        fx1 = func(x1)
        fx2 = func(x2)
        print(f"f(x1) = {fx1:.3f}\nf(x2) = {fx2:.3f}")

        if abs(b - a) <= fault:
            print(f"a - b = {a:.3f} - {b:.3f} = {a - b:.3f} <= fault = {fault:.3f}")
            if fx1 < fx2:
                print(f"f(x1) = {fx1:.3f} < f(x2) = {fx2:.3f}")
                return x1, fx1, n + 1
            else:
                print(f"f(x2) = {fx2:.3f} < f(x1) = {fx1:.3f}")
                return x2, fx2, n + 1

        if fx1 < fx2:
            b = x2
            print(f"fx1 < fx2: b = x2 = {b:.3f}")
        else:
            a = x1
            print(f"fx1 >= fx2: a = x1 = {a:.3f}")

        n += 1
        print("\n")

    print("Метод золотого сечения не смог найти корень за", max_iter, "итераций.")
    return None, None, n + 1


root, golden_result, golden_n = golden_section_with_steps(a, b, fault)
print("-" * 80)
print("Корень уравнения (метод золотого сечения):", root)
print("Значение функции в корне:", golden_result)
print("Количество итераций:", golden_n, "\n")


def chord_with_steps(a, b, fault, max_iter=100):
    n = 0

    while n < max_iter:
        x = a - func(a) * (b - a) / (func(b) - func(a))
        print(
            f"x = a - func(a) * (b - a) / (func(b) - func(a)) = {a:.3f} - {func(a):.3f} * ({b:.3f} - {a:.3f}) / ({func(b):.3f} - {func(a):.3f}) = {x:.3f}"
        )
        fx = func(x)
        print(f"f(x) = {fx:.3f}")
        if abs(func(x)) <= fault:
            print(f"|f(x)| = {abs(func(x)):.3f} <= fault = {fault:.3f}")
            return x, fx, n + 1

        prod = func(a) * fx
        if prod > 0:
            a = x
            print(f"func(a) * f(x) = {func(a):.3f} * {fx:.3f} = {prod:.3f} > 0")
            print(f"a = x = {a:.3f}")
        else:
            b = x
            print(f"func(a) * f(x) = {func(a):.3f} * {fx:.3f} = {prod:.3f} < 0")
            print(f"b = x = {b:.3f}")

        n += 1
        print("\n")


root, chord_result, chord_n = chord_with_steps(a, b, fault)
print("-" * 60)
print("Корень уравнения (метод хорд):", root)
print("Значение функции в корне:", chord_result)
print("Количество итераций:", chord_n, "\n")


def newton_with_steps(func, initial_guess, fault, max_iter=100):
    x = symbols("x")
    df = lambdify(x, diff(func(x), x))  # Производная функции
    n = 0

    while n < max_iter:
        x_new = initial_guess - func(initial_guess) / df(initial_guess)
        print(
            f"x_new = {initial_guess:.3f} - func({initial_guess:.3f}) / df({initial_guess:.3f}) = {x_new:.3f}"
        )
        if abs(x_new - initial_guess) < fault:
            print(
                f"|x_new - initial_guess| = {x_new:.3f} - {initial_guess:.3f} = |{x_new - initial_guess:.3f}| <= fault = {fault:.3f}"
            )
            return x_new, func(x_new), n

        print(f"initial_guess = x_new = {x_new:.3f}")
        initial_guess = x_new
        n += 1
        print("\n")

    return None


initial_guess = (a + b) / 2  # Начальное приближение

root, newton_result, newton_n = newton_with_steps(func, initial_guess, fault)
print("-" * 50)
print("Корень уравнения (метод Ньютона):", root)
print("Значение функции в корне:", newton_result)
print("Количество итераций:", newton_n, "\n")
