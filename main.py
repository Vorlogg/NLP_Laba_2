from typing import Union
import re
from collections import defaultdict
from tqdm import tqdm

NGRAM = 4


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
    all_words = []
    with open(file, "r", encoding="utf-8") as f:
        for i in f:
            data = re.sub(r"[\n,?,–,:,L=;,…,.,!,«,»,—,\-,*,\t,\xa0-]|(\[.+\])|(<.+>)|(\(.+\))", "", i)
            rez = data.lower()
            if rez:
                if rez != "  " and rez != " " and rez != "   " and rez != "    ":
                    # подсчет уникальных слов
                    words = rez.split()
                    [all_words.append(i) for i in words]
                    # разбитие на предложения
                    rezult_pr.append(rez)
                    # разбитие на токены и добавление $
                    rez = "$ " * (NGRAM - 1) + rez + " $" * (NGRAM - 1)
                    rezult_words = rez.split()
                    rezult_word.append(rezult_words)

    # подсчет уникальных слов
    all_words = set(all_words)
    all_count_words = len(all_words)
    return rezult_pr, rezult_word, all_words, all_count_words


def n_gram(corp: list[list[str]]):
    rez = []
    for pr in corp:
        for ngrams in zip(*[pr[i:] for i in range(NGRAM)]):
            rez.append(list(ngrams))
    return rez


# ввел предложения в начало добваить $ $ кол-во нграм, получаем нграм с него и проходимся им по корпусу нграм считаем вероятности
# беру 2 последних слова и ищу в нграм
# 'моих', 'стихов', 'ты') для ты считаем вероятность

def find_word_count(word: str, ngram):
    word_n = ["$"] * (NGRAM - 1)
    words = word.lower().split()
    word_dickt = defaultdict(lambda: 0.0)
    for w in words:
        word_n.append(w)
    rez = []
    for ngrams in zip(*[word_n[i:] for i in range(NGRAM)]):
        print(ngrams)
        rez.append(ngrams)
        word_dickt[ngrams] = count_ngram(ngrams, ngram)
    return word_dickt


def dict_word_p(ngram):
    word_dict = defaultdict(lambda: 0.0)
    for i in ngram:
        word_dict[tuple(i)] = laplace(i, 0.2, all_count_words, ngram)
    return word_dict


def count_ngram(word, ngram):
    sum = 0
    for i in ngram:
        if i[len(i) - len(word):] == word:
            sum += 1
    return sum


def laplace(word, alpha: float, v: int, ngram):
    word_count_1 = count_ngram(word, ngram)
    word_count_2 = count_ngram(word[:-1], ngram)
    return (word_count_1 + alpha) / (word_count_2 + alpha * v)
    # return (count_ngram(" ".join(word),ngram)+alpha)/(count_ngram(" ".join(word[:-1]),ngram)+alpha*v)


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


test_word = "Пушкин.txt"
test_word = "2.txt"
# test_word = "Толстой.txt"
# print(find_word(test_word, corp_text, 1))
corpr, words, all_words, all_count_words = read_txt(test_word)
# print(all_count_words)
# print(corpr)
# print(words)
# print(n_gram(words))
ngram = n_gram(words)
print(ngram)
word = find_word_count("This is the malt", ngram)
print(word)
# print(count_ngram(('$', '$', 'когда'),ngram))
# print(count_ngram(('$', 'когда'),ngram))
# wordd=('$', '$', 'когда')
# wordd=('$', '$', 'когда')
wordd = ['$', '$', '$', 'this']

print(laplace(wordd, 0.0, all_count_words, ngram))

def otkat(word, alpha: float, v: int, ngram, lambd):
    sum=0
    for i in lambd:
        sum+=i*laplace(word,alpha,v,ngram)
    return sum

def word_ty_token(rez: str):
    # разбитие на токены и добавление $
    rez = "$ " * (NGRAM - 1) + rez.lower()
    rezult_words = rez.split()
    return rezult_words


def word_ty_n_gram(corp: list[str]):
    # разбитие на n gram
    rez = []
    for ngrams in zip(*[corp[i:] for i in range(NGRAM)]):
        rez.append(list(ngrams))
    return rez


def train(word, gen: int,lambd):
    word_token = word_ty_token(word)
    word_ngram = word_ty_n_gram(word_token)
    word_p = otkat(word_ngram[-1], 0.0, all_count_words, ngram,lambd)
    word_3 = word_ngram[-1]
    max_p = 0
    word_p_gen = 0
    word_gen = []
    next_gen_word = ""
    for i in word_3[1:]:
        word_gen.append(i)
    for j in range(gen):
        for i in ngram:
            if i[:3] == word_3[-3:]:
                word_p_gen = otkat(i, 0.0, all_count_words, ngram,lambd)
                if max_p < word_p_gen:
                    max_p = word_p_gen
                    next_gen_word = i[-1]

        max_p=0
        word_p_gen=0
        if next_gen_word == "$":
            break
        word_gen.append(next_gen_word)
        word_3 = word_gen
        print("gen:{e}{gen}".format(e=j, gen=word_gen))

    print("начальное слово= " + word + " p=" + str(word_p))

    print(word_gen)


# train("This is the",5)
# train
lam=[0.2,0.4,0.8]
train("была", 30,lam)
# print(dict_word_p(ngram))

#
# words_p={}
# for i in ngram:
#     words_p[i]=laplace(i,0.2,all_count_words,ngram)
# print(words_p)


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
