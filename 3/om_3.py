def f(x):
    return (x**7) / 7 - x**3 + (x**2) / 2 - x


def main():
    # Шаг 1

    a, b = 1, 1.5
    epsilon = 0.00001
    epsilon0 = 0.05
    x1 = a
    delta_x = 0.0001  # Шаг изменения x
    print("Step 1: x1 =", a, "delta =", delta_x)

    x2 = 0
    x3 = 0
    x_ = 0

    iterations = 0
    max_iter = 100
    skip = False

    while iterations <= max_iter:
        print("\n\nIteration:", iterations)
        if not skip:
            # Шаг 2
            x2 = x1 + delta_x
            print("\nStep 2: x1 =", x1, "x2 =", x2)

            # Шаг 3
            f1, f2 = f(x1), f(x2)
            print("\nStep 3: f(x1) =", f1, "f(x2) =", f2)

            # Шаг 4
            if f1 > f2:
                x3 = x1 + 2 * delta_x
            else:
                x3 = x1 - delta_x

            # Шаг 5
            f3 = f(x3)
            print("\nStep 5: x3 =", x3, "f(x3) =", f3)

        # Шаг 6
        f1, f2, f3 = f(x1), f(x2), f(x3)
        f_min = min(f1, f2, f3)
        x_min = x1 if f_min == f1 else x2 if f_min == f2 else x3
        print("\nStep 6: f_min =", f_min, "x_min =", x_min)

        # Шаг 7
        numerator = (x2**2 - x3**2) * f1 + (x3**2 - x1**2) * f2 + (x1**2 - x2**2) * f3
        denumerator = 2 * ((x2 - x3) * f1 + (x3 - x1) * f2 + (x1 - x2) * f3)
        print("\nStep 7: numerator =", numerator, "denumerator =", denumerator)

        # Проверка знаменателя
        if denumerator == 0:
            # Результатом итерации является прямая
            x1 = x_min
            iterations += 1
            print("denumerator == 0, Jump to step 2")
            skip = False
            continue

        x_ = numerator / denumerator
        f_ = f(x_)
        print("\nStep 7: x_ =", x_, "f(x_) =", f_)

        # Шаг 8
        condition_1 = abs((f_min - f_) / f_) < epsilon0
        condition_2 = abs((x_min - x_) / x_) < epsilon
        print("\nStep 8: condition_1 =", condition_1, "condition_2 =", condition_2)

        if condition_1 and condition_2:
            print(
                "\n\nFinal minimum x:",
                x_min,
                "f(x):",
                f_min,
                "Iterations:",
                iterations + 1,
            )
            break

        elif condition_1 or condition_2:
            if x_ >= x1 and x_ <= x3:
                x2 = min(x_min, x_)
                skip = True
                iterations += 1
                print("x_ >= x1 and x_ <= x3, Jump to step 6")
                continue
            else:
                skip = False
                iterations += 1
                x1 = x_
                continue
        else:
            x1 = x_
            x2 = x3
            x3 = x_min

        iterations += 1
        skip = False

    if iterations > max_iter:
        print("\n\nMaximum number of iterations reached.")
        print("\nFinal minimum x:", x_, "f(x):", f(x_), "Iterations:", iterations)


if __name__ == "__main__":
    main()
