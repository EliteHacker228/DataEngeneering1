# Задание 1, вариант 41

def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        lines = file.readlines()
        return lines


def text_to_words(text):
    words = []
    for line in text:
        _line = (line
                 .replace("'", "")
                 .replace("?", "")
                 .replace("!", "")
                 .replace(".", "")
                 .replace(",", "")
                 .replace("-", " ")
                 .lower()
                 .strip())
        words += _line.split(" ")
    return words


def calc_freq(words):
    word_freq = {}
    for word in words:
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1

    word_freq_sorted = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return word_freq_sorted


def vowel_part_and_count(words):
    vowels = ['a', 'e', 'i', 'o', 'u']
    vowels_count = 0
    total_count = 0
    for word in words:
        if word.startswith(tuple(vowels)):
            vowels_count += 1
        total_count += 1
    return (vowels_count, total_count)


def write_words_freq_to_file(words_freq, path):
    with open(path, "w", encoding="utf-8") as file:
        for word, freq in words_freq:
            file.write(f"{word}:{freq}\n")


def append_vowels_to_file(vowels, path):
    vow_count = vowels[0]
    vow_part = round(vow_count / vowels[1], 2)
    sep = "================================\n"
    with open(path, "a", encoding="utf-8") as file:
        file.write(sep)
        file.write(f"Vowels count:{vow_count}\n")
        file.write(f"Vowels part:{vow_part}\n")

path = "41/first_task.txt"
lines = read_file(path)
words = text_to_words(lines)
words_freq = calc_freq(words)
vowels = vowel_part_and_count(words)
write_words_freq_to_file(words_freq, "first_task_result.txt")
append_vowels_to_file(vowels, "first_task_result.txt")
