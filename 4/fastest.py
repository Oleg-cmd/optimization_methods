import sympy as sp

expression = "-x -4*(y^2) + 2*x*y + x"
f = sp.sympify(expression)
x_s, y_s, h_s = sp.symbols("x y h")
eps = 0.01


def module(grad_f_val):
    return sp.sqrt(sum(expr**2 for expr in grad_f_val))


grad_f = [sp.diff(f, var) for var in (x_s, y_s)]

val_x, val_y = 1, 1
f_start = f.subs({x_s: val_x, y_s: val_y})

while True:
    grad_f_val = [expr.subs({x_s: val_x, y_s: val_y}) for expr in grad_f]

    tmp_x = val_x - h_s * grad_f_val[0]
    tmp_y = val_y - h_s * grad_f_val[1]

    val = f.subs({x_s: tmp_x, y_s: tmp_y})

    df_val = sp.diff(val, h_s)

    solution = sp.solve(df_val, h_s)

    val_x = val_x - min(solution) * grad_f_val[0]
    val_y = val_y - min(solution) * grad_f_val[1]

    f_end = f.subs({x_s: val_x, y_s: val_y})

    if abs(f_end - f_start) < eps:
        print(
            f"Координаты x, y: {[val_x.evalf(), val_y.evalf()]} и значение функции в этой точке: {f_end.evalf()}"
        )
        break
    f_start = f_end
