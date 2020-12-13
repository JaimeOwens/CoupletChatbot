import os
from typing import List   # python的类型注解，让人知道该传入什么样的类型参数
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction   # 双语评估替换, 比较候选文本翻译与其他一个或多个参考翻译的评价分数

sf = SmoothingFunction()


def calc_bleu(cand: List[int or str], ref: List[int or str]):
    return sentence_bleu([ref], cand, smoothing_function=sf.method1)     # sentence_bleu, 用于根据一个或多个参考语句来评估候选语句。


def calc_rouge_l(cand: List[int or str], ref: List[int or str], beta: float = 1.2):
    len_cand = len(cand)
    len_ref = len(ref)
    lengths = [[0 for j in range(len_ref + 1)] for i in range(len_cand + 1)]
    for i in range(len_cand):
        for j in range(len_ref):
            if cand[i] == ref[j]:
                lengths[i + 1][j + 1] = lengths[i][j] + 1
            elif lengths[i + 1][j] > lengths[i][j + 1]:
                lengths[i + 1][j + 1] = lengths[i + 1][j]
            else:
                lengths[i + 1][j + 1] = lengths[i][j + 1]
    lcs = lengths[-1][-1]
    eps = 1e-10
    r = lcs * 1.0 / (eps + len_ref)
    p = lcs * 1.0 / (eps + len_cand)
    f = ((1 + beta**2) * r * p) / (eps + r + beta ** 2 * p)
    return f

def calc_bert_score(cand: str, ref: str):
    res = os.popen('bert-score --lang zh -r "{0}" -c "{1}" --model bert-base-chinese'.format(ref, cand)).read()
    res = res.split(' ')
    return (float(res[2].strip()), float(res[4].strip()), float(res[-1].strip())) # P,R,F1
