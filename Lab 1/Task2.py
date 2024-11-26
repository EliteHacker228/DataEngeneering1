# Задание 2, вариант 41


def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        return lines


# Фильтруем номера согласно условиям варианта 41 (выбираем положительные)
def filter_numbers(numbers):
    return filter(lambda number: number > 0, numbers)


def get_numbers(lines):
    numbers = []
    for line in lines:
        line_numbers = list(map(int, line.split(" ")))
        numbers.append(line_numbers)
    return numbers

def process_numbers_grid(numbers_grid):
    column_of_summed_rows = []
    for numbers_line in numbers_grid:
        filtered_numbers_line = filter_numbers(numbers_line)
        summed_numbers_line = sum(filtered_numbers_line)
        column_of_summed_rows.append(summed_numbers_line)
    return column_of_summed_rows

def write_to_file(path, column_of_summed_rows, total_sum):
    sep = "================================\n"
    with open(path, "w", encoding="utf-8") as file:
        for summed_coulmn in column_of_summed_rows:
            file.write(f"{summed_coulmn}\n")
        file.write(sep)
        file.write(str(total_sum))


lines = read_file("41/second_task.txt")
numbers = get_numbers(lines)
column_of_summed_rows = process_numbers_grid(numbers)
total_sum = sum(column_of_summed_rows)
write_to_file("second_task_result.txt", column_of_summed_rows, total_sum)
