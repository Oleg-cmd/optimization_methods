import random
from tabulate import tabulate

def calculate_target_value(sample, matrix):
    target_value = sum(matrix[sample[j] - 1][sample[j + 1] - 1] for j in range(len(sample) - 1))
    target_value += matrix[sample[-1] - 1][sample[0] - 1]
    return target_value

def get_remaining_indices(length, indices):
    return [i for i in range(length) if i not in indices]

def mutate(child, child_number):
    mutation = 0.01
    if random.random() < mutation:
        print(f"Произошла мутация в ребенке {child_number}!")
        print("Был:", child)
        idx1, idx2 = random.sample(range(len(child)), 2)
        child[idx1], child[idx2] = child[idx2], child[idx1]
    return child

def func(couple, fragment_1, fragment_2, cut, n):
    child = [[], fragment_1, []]
    for gene in couple[cut[0] + 1:] + couple[:cut[0] + 1]:
        if gene not in (child[0] + child[1] + child[2]):
            if len(child[2]) < len(fragment_2):
                child[2].append(gene)
            else:
                child[0].append(gene)
    child = mutate(child[0] + child[1] + child[2], n)
    return child

def get_fragments(individual, cut_points):
    return [
        individual[:cut_points[0]],
        individual[cut_points[0]:cut_points[1]],
        individual[cut_points[1]:]
    ]

def create_child(parent, fragment, other_fragment, cut_points, identifier):
    return func(parent, fragment, other_fragment, cut_points, identifier)

def calculate_child_values(children, matrix):
    return [calculate_target_value(child, matrix) for child in children]

def generate_table(parents_indices, fragments, children, target_values):
    table = [["номер родителя", "родитель", "потомок", "значение функции для потомка"]]
    for i, (parent_index, fragment, child, target_value) in enumerate(zip(parents_indices, fragments, children, target_values)):
        table.append([parent_index + 1, fragment, child, target_value])
    return table

def generate_best_individuals_table(sorted_individuals):
    best_individuals = sorted_individuals[:4]
    best_individuals_table = [["Номер строки", "Код", "Значение целевой функции", "Вероятность участия в размножении"]]
    total_value = sum(ind[2] for ind in best_individuals)
    for ind in best_individuals:
        target_value = ind[2]
        reproduction_probability = (best_individuals[0][2] + best_individuals[3][2] - target_value) / total_value
        row = [ind[0], ind[1], target_value, reproduction_probability]
        best_individuals_table.append(row)
    return best_individuals_table

def main():
    matrix = [[0, 1, 1, 5, 3],
              [1, 0, 3, 1, 5],
              [1, 3, 0, 11, 1],
              [5, 1, 11, 0, 1],
              [3, 5, 1, 1, 0]]

    original_sample = []
    while len(original_sample) < 4:
        new_individual = random.sample([1, 2, 3, 4, 5], 5)
        if new_individual not in original_sample:
            original_sample.append(new_individual)

    parent_table = [["номер строки исходной выборки", "код", "значение целевой функции"]]
    for i, sample in enumerate(original_sample, 1):
        target_value = calculate_target_value(sample, matrix)
        parent_table.append([i, sample, target_value])

    print("Текущее поколение:")
    print(tabulate(parent_table, headers="firstrow", tablefmt="grid"))

    number_of_repetitions = 4
    counter = 0
    while counter < number_of_repetitions:
        counter += 1

        parents_indices = random.sample(range(len(original_sample)), 2)
        remaining_indices = get_remaining_indices(len(original_sample), parents_indices)

        print("Выбранные пары родителей:", [(i + 1) for i in sorted(parents_indices)],
              [(j + 1) for j in sorted(remaining_indices)])

        couples_parent = [original_sample[idx] for idx in parents_indices]
        coples_remain = [original_sample[idx] for idx in remaining_indices]

        cut_points1 = sorted(random.sample(range(1, len(couples_parent[0])), 2))
        cut_points2 = sorted(random.sample(range(1, len(coples_remain[0])), 2))

        fragments_parent = [get_fragments(couples_parent[i], cut_points1) for i in range(2)]
        fragments_remain = [get_fragments(coples_remain[i], cut_points2) for i in range(2)]

        children = [
            create_child(couples_parent[0], fragments_parent[1][1], fragments_parent[0][2], cut_points1, 1),
            create_child(couples_parent[1], fragments_parent[0][1], fragments_parent[1][2], cut_points1, 2),
            create_child(coples_remain[0], fragments_remain[1][1], fragments_remain[0][2], cut_points2, 3),
            create_child(coples_remain[1], fragments_remain[0][1], fragments_remain[1][2], cut_points2, 4)
        ]

        target_values = calculate_child_values(children, matrix)
        fragments = fragments_parent + fragments_remain
        parents_indices_all = parents_indices + remaining_indices

        table_children = generate_table(parents_indices_all, fragments, children, target_values)
        print(tabulate(table_children, headers="firstrow", tablefmt="grid"))

        all_individuals = parent_table[1:] + [['N', child, target_value] for child, target_value in zip(children, target_values)]
        sorted_individuals = sorted(all_individuals, key=lambda x: x[2])
        best_individuals = sorted_individuals[:4]

        best_individuals_table = generate_best_individuals_table(sorted_individuals)
        print("Популяция поколения после отсечения худших особей:\n", tabulate(best_individuals_table, headers="firstrow", tablefmt="grid"))

        original_sample = [best_individuals[i][1] for i in range(4)]
        parent_table = [["номер строки исходной выборки", "код", "значение целевой функции"]]
        for i, sample in enumerate(original_sample, 1):
            target_value = calculate_target_value(sample, matrix)
            parent_table.append([i, sample, target_value])

        print("Текущее поколение:")
        print(tabulate(parent_table, headers="firstrow", tablefmt="grid"))

if __name__ == "__main__":
    main()
