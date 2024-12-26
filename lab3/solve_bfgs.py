import numpy as np

# def analyzed_func(x):
#     #Функция Розенброк.
#     return (1 - x[0])**2 + 100 * (x[1] - x[0]**2)**2
# def analyzed_func_grad(x):
#     #Градиент функции Розенброк
#     dfdx0 = -2 * (1 - x[0]) - 400 * x[0] * (x[1] - x[0]**2)
#     dfdx1 = 200 * (x[1] - x[0]**2)
#     return np.array([dfdx0, dfdx1])

# def analyzed_func(x):
#     #Функция чашки.
#     return (x[0]-1)**2+x[1]**2
# def analyzed_func_grad(x):
#     #Градиент функции чашки
#     dfdx0 = 2*(x[0]-1)
#     dfdx1 = 2*x[1]
#     return np.array([dfdx0, dfdx1])

def analyzed_func(x):
    #Функция Химмельблау.
    return (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 - 7)**2
def analyzed_func_grad(x):
    #Градиент функции Химмельблау
    dfdx0 = 4*x[0]*(x[0]**2 + x[1] - 11) + 2*(x[0] + x[1]**2 - 7)
    dfdx1 = 2*(x[0]**2 + x[1] - 11) + 4*x[1]*(x[0] + x[1]**2 - 7)
    return np.array([dfdx0, dfdx1])

def line_search(f, grad, x, p):
    alpha = 1.0
    c = 1e-4
    while f(x + alpha * p) > f(x) + c * alpha * grad(x) @ p:
        alpha *= 0.5  # Уменьшаем шаг
    return alpha

def bfgs(initial_x, max_iter=1000, tol=1e-6):
    n = len(initial_x)
    x_k = initial_x
    g_k = analyzed_func_grad(x_k)
    H_k = np.eye(n)  # Начальный гауссиан

    for i in range(max_iter):
        if np.linalg.norm(g_k) < tol:
            print(f"BFGS cошлось за {i} итераций.")
            return x_k

        p_k = -H_k @ g_k  # Направление поиска

        # Линейный поиск для нахождения alpha
        alpha_k = line_search(analyzed_func, analyzed_func_grad, x_k, p_k)
        x_k_new = x_k + alpha_k * p_k

        g_k_new = analyzed_func_grad(x_k_new)
        s_k = x_k_new - x_k
        y_k = g_k_new - g_k

        # Обновление Гауссиана
        rho_k = 1.0 / (y_k @ s_k)
        H_k = (np.eye(n) - rho_k * np.outer(s_k, y_k)) @ H_k @ (np.eye(n) - rho_k * np.outer(y_k, s_k)) + rho_k * np.outer(s_k, s_k)

        x_k = x_k_new
        g_k = g_k_new

    print("BFGS достигнуто максимальное количество итераций.")
    return x_k

def gradient_descent(initial_x, max_iter=10000, tol=1e-6, alpha=0.001):
    x_k = initial_x
    for i in range(max_iter):
        g_k = analyzed_func_grad(x_k)
        if np.linalg.norm(g_k) < tol:
            print(f"Градиентом сошлось за {i} итераций.")
            return x_k
        x_k = x_k - alpha * g_k  # Обновление точки
    print("Градиентом достигнуто максимальное количество итераций.")
    return x_k

# Начальная точка
initial_x = np.array([-3.21, 5.0])

# Запуск BFGS
result_bfgs = bfgs(initial_x)
print("Оптимальное значение BFGS:", result_bfgs)
print("Значение функции BFGS:", analyzed_func(result_bfgs))

# Запуск градиентного спуска
result_gd = gradient_descent(initial_x)
print("Оптимальное значение GD:", result_gd)
print("Значение функции GD:", analyzed_func(result_gd))

