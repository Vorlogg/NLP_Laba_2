from typing import Union
import re
from collections import defaultdict
from tqdm import tqdm

NGRAM = 3


# def read_txt(file: str):
#     rezult = []
#     word_set = set()
#     with open(file, "r", encoding="utf-8") as f:
#         for i in f:
#             data = re.sub(r"[\n,?,–,…,.,!,«,»,—,\-,*,\t,\xa0-]|(\[.+\])|(<.+>)|(\(.+\))", "", i)
#             rez = data.lower().split()
#             if rez:
#                 rezult.append(rez)
#                 for j in rez:
#                     word_set.add(j)
#     return rezult, word_set

def read_txt(file: str):
    rezult_pr = []
    rezult_word = []
    all_words=[]
    with open(file, "r", encoding="utf-8") as f:
        for i in f:
            data = re.sub(r"[\n,?,–,:,L=;,…,.,!,«,»,—,\-,*,\t,\xa0-]|(\[.+\])|(<.+>)|(\(.+\))", "", i)
            rez = data.lower()
            if rez:
                if rez != "  " and rez != " " and rez != "   " and rez != "    ":
                    #подсчет уникальных слов
                    words=rez.split()
                    [all_words.append(i) for i in words]
                    #разбитие на предложения
                    rezult_pr.append(rez)
                    #разбитие на токены и добавление $
                    rez = "$ " * (NGRAM - 1) + rez + " $" * (NGRAM - 1)
                    rezult_words = rez.split()
                    rezult_word.append(rezult_words)

    # подсчет уникальных слов
    all_words=set(all_words)
    all_count_words=len(all_words)
    return rezult_pr, rezult_word,all_words,all_count_words


def n_gram(corp: list[list[str]]):
    rez = []
    for pr in corp:
        for ngrams in zip(*[pr[i:] for i in range(NGRAM)]):
            rez.append(ngrams)
    return rez


# ввел предложения в начало добваить $ $ кол-во нграм, получаем нграм с него и проходимся им по корпусу нграм считаем вероятности
# беру 2 последних слова и ищу в нграм
# 'моих', 'стихов', 'ты') для ты считаем вероятность

def find_word_count(word: str,ngram):
    word_n = ["$"] * (NGRAM - 1)
    words = word.lower().split()
    word_dickt=defaultdict(lambda:0.0)
    for w in words:
        word_n.append(w)
    rez = []
    for ngrams in zip(*[word_n[i:] for i in range(NGRAM)]):
        rez.append(ngrams)
        word_dickt[ngrams]=count_ngram(ngrams,ngram)
    return word_dickt

def count_ngram(word,ngram):
    sum=0
    for i in ngram:
        if i[len(i)-len(word):] == word:
           sum+=1
    return sum




def laplace(word, alpha:float,v:int,ngram):
    return (count_ngram(" ".join(word),ngram)+alpha)/(count_ngram(" ".join(word[:-1]),ngram)+alpha*v)



# def train(corp: list[str], n: int):
#     n_grams = n_gram(corp, n)
#     bigram = bigrams(corp)
#     bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)
#     for i in bigram:
#         # bi[i[0], i[1]] = count_word2(i[0], i[1], corp)
#         bi[i[0], i[1]] += 1
#     for i in n_grams:
#         rez = tuple([i[j] for j in range(n)])
#         tri[rez] += 1
#
#     model = defaultdict(lambda: 0.0)
#     for key, items in tqdm(tri.items()):
#         # v1=p_grams(int(items),str(key[0]),corp)
#         model[key] = items / corp.count(key[0])
#         # print(model[key])
#     print(model)
#
#     # print(tri)


def p_grams(count: int, word: str, corp: list[str]):
    # кол--во повторений нграм на кол-во повторений 1 го слова
    # ('теперь', 'отдыхай'):
    # print(bi[0]/corp.count('теперь'))
    return count / corp.count(word)


def all_count_word(corp: list[list[str]]):
    rez = 0
    for i in corp:
        rez += len(i)
    return rez


# def count_word2(word1: str, word2: str, corp: list[list[str]]):
#     rez = 0
#     for i in corp:
#         for j in range(len(i)):
#             if word1 == i[j - 1] and word2 == i[j]:
#                 rez += 1
#     return rez
def count_word2(word1: str, word2: str, corp: list[str]):
    rez = 0
    for i in range(len(corp) - 1):
        if word1 == corp[i - 1] and word2 == corp[i]:
            rez += 1
    return rez


def p_word(word: str, corp: list[str]):
    return corp.count(word.lower()) / len(corp)


def p_count_word2(word1: str, word2: str, corp: list[str]):
    rez = count_word2(word2, word1, corp) / corp.count(word2.lower())
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
test_word = "1.txt"
# test_word = "Толстой.txt"
# print(find_word(test_word, corp_text, 1))
corpr, words,all_count_words ,v= read_txt(test_word)
# print(all_count_words)
# print(corpr)
# print(words)
# print(n_gram(words))
ngram=n_gram(words)
print(ngram)
# word=find_word_count("Когда Потемкину в потемках",ngram)
# print(word)
# print(count_ngram(('$', '$', 'когда'),ngram))
# print(count_ngram(('$', 'когда'),ngram))
# wordd=('$', '$', 'когда')
# wordd=('$', '$', 'когда')
wordd=('$', '$', 'this')
print(laplace(wordd,0.2,v,ngram))





# train(corp, 3)
# # print(bigr)
# corp = ["this", "is", "the", "malt", "that", "lay", "in", "the", "house", "that", "jack", "built"]
# # corp=read_txt("1.txt")
# # train(corp, 3)
#
# # print(corp)
# # print(all_count_word(corp))
# w1 = p_word("this", corp)
# print(count_word2("is", "this", corp))
# w2 = p_count_word2("is", "this", corp)
# w3 = p_count_word2("is", "this", corp)
# w4 = p_count_word2("house", "the", corp)
# rez = w1 * w2 * w3 * w4
# print(rez)

# w1=count_word("that", corp)
# print(w1)
# w2=p_count_word2("that", "jack", corp)
# print(count_word2("that", "jack", corp))
# print(w2)
# rez1=count_word2("that", "jack", corp)/count_word("that", corp)
# print(rez1)
