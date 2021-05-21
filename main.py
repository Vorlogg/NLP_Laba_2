from typing import Union
import re
from collections import defaultdict
import statistics
from math import sqrt


def read_txt(file: str):
    rezult = []
    word_set = set()
    with open(file, "r", encoding="utf-8") as f:
        for i in f:
            data = re.sub(r"[\n,?,–,…,.,!,«,»,—,\-,*,\t,\xa0-]|(\[.+\])|(<.+>)|(\(.+\))", "", i)
            rez = data.lower().split()
            if rez:
                rezult.append(rez)
                for j in rez:
                    word_set.add(j)
    return rezult, word_set


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
    rez = count_word2(word2, word1, corp) / count_word(word2, corp)
    if rez == 0:
        rez = 1
    return rez


# def bgram(corp: list[list[str]], word_set: set, n:int,start_word:str):
#     nword=0
#     word=start_word
#     w1 = p_word(start_word, corp)
#     while nword<n:
#         for i in word_set:
#
#     return





test_word = "Пушкин.txt"
# print(find_word(test_word, corp_text, 1))
corp, set = read_txt(test_word)
# corp=[["this","is","the","malt"],["that","lay","in","the","house","that","jack","built"]]
# corp=read_txt("1.txt")
print(corp)
print(set)
print(all_count_word(corp))
w1 = p_word("this", corp)
print(count_word2("is", "this", corp))
w2 = p_count_word2("is", "this", corp)
w3 = p_count_word2("is", "this", corp)
w4 = p_count_word2("house", "the", corp)
print(w1)
print(w2)
print(w3)
print(w4)
rez = w1 * w2 * w3 * w4
print(rez)





# w1=count_word("that", corp)
# print(w1)
# w2=p_count_word2("that", "jack", corp)
# print(count_word2("that", "jack", corp))
# print(w2)
# rez1=count_word2("that", "jack", corp)/count_word("that", corp)
# print(rez1)

