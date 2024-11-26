# Задание 3, вариант 41
from math import sqrt


def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        return lines


# Считаем среднее через целочисленное деление
def parse_lines(lines):
    res = []
    for line in lines:
        line_elements = line.split(" ")
        for i in range(len(line_elements)):
            if line_elements[i] == "N/A":
                replacer = (int(line_elements[i - 1]) + int(line_elements[i + 1])) // 2
                line_elements[i] = replacer
        res.append(list(map(int, line_elements)))
    return res


# Оставляем только положительные значения, корень квадратный из которых меньше 200
# (т.к. из отрицательного числа нельзя взять квадратный корень - отфильтровываем их)
def filtered_lines(lines):
    res = []
    for line in lines:
        _line = list(filter(lambda x: x > 0, line))
        _line = list(filter(lambda x: sqrt(x) < 200, _line))
        res.append(_line)
    return res

def sum_lines(lines):
    res = []
    for line in lines:
        res.append(sum(line))
    return res

def file_write(path, summed_lines):
    with open(path, "w", encoding="utf-8") as file:
        for line in summed_lines:
            file.write(f"{line}\n")

path = "41/third_task.txt"
lines = read_file(path)
parsed_lines = parse_lines(lines)
filtered_lines = filtered_lines(parsed_lines)
summed_lines = sum_lines(filtered_lines)
file_write("third_task_result.txt", summed_lines)