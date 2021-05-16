from typing import Union
import re
from collections import defaultdict
import statistics
from math import sqrt


def read_txt(file: str) -> list[list[str]]:
    rezult = []
    with open(file, "r", encoding="utf-8") as f:
        for i in f:
            data = re.sub(r"[\n,?,–,…,.,!,«,»,—,\-,*,\t,\xa0-]|(\[.+\])|(<.+>)|(\(.+\))", "", i)
            rez = data.lower().split()
            if rez:
                rezult.append(rez)
    return rezult


def count_word(word: str, corp: list[list[str]]):
    rez = 0
    for i in corp:
        rez += i.count(word.lower())
    return rez


def all_count_word(corp: list[list[str]]):
    rez = 0
    for i in corp:
        rez += len(i)
    return rez


def count_word2(word1: str, word2: str, corp: list[list[str]]):
    rez = 0
    for i in corp:
        for j in range(len(i)):
            if word1 == i[j - 1] and word2 == i[j]:
                rez += 1
    return rez


def p_word(word: str, corp: list[list[str]]):
    return count_word(word, corp) / all_count_word(corp)


def p_count_word2(word1: str, word2: str, corp: list[list[str]]):
     rez= count_word2(word2, word1, corp) / count_word(word2,corp)
    if rez==0:
        rez=1
    return rez


test_word = "Пушкин.txt"
# print(find_word(test_word, corp_text, 1))
corp = read_txt(test_word)
corp=[["this","is","the","malt"],["that","lay","in","the","house","that","jack","built"]]
# corp=read_txt("1.txt")
print(corp)
print(all_count_word(corp))
# w1=count_word("that", corp)
# print(w1)
# w2=p_count_word2("that", "jack", corp)
# print(count_word2("that", "jack", corp))
# print(w2)
# rez1=count_word2("that", "jack", corp)/count_word("that", corp)
# print(rez1)

w1=p_word("this", corp)
print(count_word2("is", "this", corp))
w2=p_count_word2("is", "this", corp)

w3=p_count_word2("is", "this", corp)
w4=p_count_word2("house", "the", corp)
print(w1)
print(w2)
print(w3)
print(w4)
rez=w1*w2*w3*w4
print(rez)

def find_word(word: str, text: dict, errors: int) -> Union[list[str], str]:
    """Поиск слов"""
    rez = []
    for i in text[len(word)]:
        if method_hamming_distance(word.lower(), i) < errors:
            rez.append(i)
    for i in text[len(word) - 1]:
        if method_hamming_distance(word.lower(), i) < errors:
            rez.append(i)
    for i in text[len(word) + 1]:
        if method_hamming_distance(word.lower(), i) < errors:
            rez.append(i)
    if len(rez) != 0:
        return rez
    else:
        for index, items in corp_text.items():
            for i in items:
                if method_hamming_distance(word.lower(), i) < errors:
                    rez.append(i)
    return rez


def method_hamming_distance(word1: str, count_word2: str) -> int:
    rez = 0
    for char1, char2, in zip(word1, count_word2):
        if char1 != char2:
            rez += 1
    return rez


def list_word(words: list, text: dict, errors: int):
    rez = []
    for i in words:
        rez.append(find_word(i, text, errors))
    return rez


def standard_deviation(answer: list, input: list):
    x = []
    for index, items in enumerate(answer):
        if input[index] in items:
            x.append(1)
        else:
            x.append(0)
    x_mean = statistics.mean(x)
    rez = 0
    for i in x:
        rez += pow(i - x_mean, 2)
    return sqrt(rez / (len(x) - 1))


def mean_squared_error(answer: list, input: list):
    y = []
    sum_error = 0.0
    for index, items in enumerate(answer):
        if input[index] in items:
            y.append(1)
        else:
            y.append(0)
    for i in range(len(y)):
        sum_error += (1 - y[i] ** 2)
    mean_error = sum_error / float(len(y))
    return mean_error

# test_word = "Пушкин.txt"
# # print(find_word(test_word, corp_text, 1))
# print(read_txt(test_word))

# if __name__ == '__main__':
#     print("Введите название файла книгу")
#     file = input(">")
#     corp_text = read_txt(file)
#     while True:
#         print("Нажмите 1 чтобы проверить слово")
#         print("Нажмите 2 чтобы тестировать по метрики стандартным отклонением")
#         print("Нажмите 3 чтобы тестировать по метрики средней квадратичной ошибки")
#         print("Нажмите 4 чтобы выйти")
#         intp = input(">")
#         if intp == "1":
#             test_word = input(">")
#             print(find_word(test_word, corp_text, 1))
#         elif intp == "2":
#             words = [str(s) for s in input().split()]
#             new_words = list_word(words, corp_text, 1)
#             print(standard_deviation(new_words, words))
#         elif intp == "3":
#             words = [str(s) for s in input().split()]
#             new_words = list_word(words, corp_text, 1)
#             print(mean_squared_error(new_words, words))
#         elif intp == "4":
#             break
