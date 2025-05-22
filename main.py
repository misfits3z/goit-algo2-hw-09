import random
import math


# Визначення функції Сфери
def sphere_function(x):
    return sum(xi**2 for xi in x)


# Допоміжна функція для генерування сусідніх рішень
def get_neighbor(x, bounds, step_size=0.1):
    neighbor = []
    for xi, (lower, upper) in zip(x, bounds):
        # Зміщення в межах [-step_size, step_size]
        delta = random.uniform(-step_size, step_size)
        new_xi = xi + delta
        # Забезпечення, що нове значення лежить в межах
        new_xi = max(min(new_xi, upper), lower)
        neighbor.append(new_xi)
    return neighbor


# Hill Climbing
def hill_climbing(func, bounds, iterations=1000, epsilon=1e-6):
    # Ініціалізація випадкової початкової точки у межах bounds
    current = [random.uniform(lower, upper) for (lower, upper) in bounds]
    current_value = func(current)

    for i in range(iterations):
        # Генеруємо сусідню точку
        candidate = get_neighbor(current, bounds, step_size=0.1)
        candidate_value = func(candidate)

        # Якщо покращення більше epsilon, то оновлюємо поточне рішення
        if current_value - candidate_value > epsilon:
            # Різниця координат або функціональна зміна
            diff = abs(current_value - candidate_value)
            current, current_value = candidate, candidate_value
        else:
            # Якщо покращення незначне, припиняємо пошук
            break

    return current, current_value


# Random Local Search
def random_local_search(func, bounds, iterations=1000, epsilon=1e-6):
    # Початкове випадкове рішення
    best = [random.uniform(lower, upper) for (lower, upper) in bounds]
    best_value = func(best)

    for i in range(iterations):
        # Повністю нова випадкова точка в просторі розв'язків
        candidate = [random.uniform(lower, upper) for (lower, upper) in bounds]
        candidate_value = func(candidate)

        if best_value - candidate_value > epsilon:
            best, best_value = candidate, candidate_value
        # Альтернативно, можна перевіряти зміну від попередньої ітерації,
        # але тут кожна ітерація незалежна.

    return best, best_value


# Simulated Annealing
def simulated_annealing(
    func, bounds, iterations=1000, temp=1000, cooling_rate=0.95, epsilon=1e-6
):
    # Початкове рішення
    current = [random.uniform(lower, upper) for (lower, upper) in bounds]
    current_value = func(current)
    best = current[:]
    best_value = current_value

    for i in range(iterations):
        # Якщо температура знизилась до epsilon або нижче, припиняємо роботу
        if temp < epsilon:
            break

        # Генеруємо сусідню точку (можна використовувати більший step_size, зменшуючи його при охолодженні)
        candidate = get_neighbor(
            current, bounds, step_size=temp / 100
        )  # масштабування ступеня змін залежно від температури
        candidate_value = func(candidate)

        # Різниця функційних значень
        delta = candidate_value - current_value

        # Якщо кандидат краще, або із заданою імовірністю приймаємо погіршення
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temp):
            current, current_value = candidate, candidate_value

        # Оновлюємо найкраще знайдене рішення
        if current_value < best_value:
            best, best_value = current[:], current_value

        # Охолодження: зменшуємо температуру
        temp *= cooling_rate

        # Якщо зміна функції дуже мала, можна зупинитися
        if abs(delta) < epsilon:
            break

    return best, best_value


if __name__ == "__main__":
    # Межі для функції
    bounds = [(-5, 5), (-5, 5)]

    # Виконання алгоритмів
    print("Hill Climbing:")
    hc_solution, hc_value = hill_climbing(sphere_function, bounds)
    print("Розв'язок:", hc_solution, "Значення:", hc_value)

    print("\nRandom Local Search:")
    rls_solution, rls_value = random_local_search(sphere_function, bounds)
    print("Розв'язок:", rls_solution, "Значення:", rls_value)

    print("\nSimulated Annealing:")
    sa_solution, sa_value = simulated_annealing(sphere_function, bounds)
    print("Розв'язок:", sa_solution, "Значення:", sa_value)
