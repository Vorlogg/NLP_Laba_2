from typing import Union
import re
from collections import defaultdict
from tqdm import tqdm

NGRAM = 4


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


def p_grams(count: int, word: str, corp: list[str]):
    # кол--во повторений нграм на кол-во повторений 1 го слова
    # ('теперь', 'отдыхай'):
    # print(bi[0]/corp.count('теперь'))
    return count / corp.count(word)




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

def perplection(p_ngram,len_words):
    try:
        n=-1/len_words
        rez=pow(p_ngram, -1/len_words)
        return rez
    except Exception as e:
        return 0


def train(word, gen: int,lambd):
    word_token = word_ty_token(word)
    word_ngram = word_ty_n_gram(word_token)
    word_p = otkat(word_ngram[-1], 0.0, all_count_words, ngram,lambd)
    word_3 = word_ngram[-1]
    max_p = 0
    word_p_gen = 0
    word_gen = []
    next_gen_word = ""
    perpl_start = perplection(word_p,len(word_3))
    print("перплексия до={p}".format(p=perpl_start))
    for i in word_3[1:]:
        word_gen.append(i)
    for j in range(gen):
        for i in ngram:
            if i[:3] == word_3[-3:]:
                word_p_gen = otkat(i, 0.2, all_count_words, ngram,lambd)
                if max_p < word_p_gen:
                    max_p = word_p_gen
                    next_gen_word = i[-1]


        if next_gen_word == "$":
            break

        max_p = 0
        word_p_gen = 0
        word_gen.append(next_gen_word)
        word_3 = word_gen

        print("gen:{e}{gen}".format(e=j, gen=word_gen))

    print("начальное слово= " + word + " p=" + str(word_p))
    # word_token_gen = word_ty_token(word_gen)
    word_gen_p=1
    word_ngram_gen = word_ty_n_gram(word_gen)
    for i in word_ngram_gen:
        word_gen_p*=otkat(i, 0.2, all_count_words, ngram,lambd)
    perpl_end = perplection(word_gen_p,len(word_gen))
    print("перплексия после={p}".format(p=perpl_end))


    print(word_gen)


# test_word = "Пушкин.txt"
test_word = "2.txt"

corpr, words, all_words, all_count_words = read_txt(test_word)

ngram = n_gram(words)
lam=[0.2,0.4,0.8]
train("вы", 30,lam)
