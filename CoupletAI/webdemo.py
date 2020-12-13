import os
import sys
import json
import torch
from flask import Flask, request, render_template
import argparse
from main import init_model_by_key
from module import Tokenizer, init_model_by_key
from module.metric import *

# 如果要增加域名映射，参考https://zhuanlan.zhihu.com/p/45471645

MODEL_PATH = sys.argv[1]
class Context(object):
    def __init__(self, path):
        print(f"loading pretrained model from {path}")
        self.device = torch.device('cpu')
        model_info = torch.load(path, map_location='cpu')
        self.tokenizer = model_info['tokenzier']
        self.model = init_model_by_key(model_info['args'], self.tokenizer)
        self.model.load_state_dict(model_info['model'])
        self.model.to(self.device)
        self.model.eval()

    def predict(self, s):
        input_ids = torch.tensor(self.tokenizer.encode(s)).unsqueeze(0).to(self.device)
        with torch.no_grad():
            logits = self.model(input_ids).squeeze(0)
        pred = logits.argmax(dim=-1).tolist()
        pred = self.tokenizer.decode(pred)
        return pred

    def evaluate(self, ref, can):
        if len(ref) == 2:
            r_bert_p, r_bert_r, r_bert_f1 = calc_bert_score(ref[0], ref[1])
        bert_p, bert_r, bert_f1 = calc_bert_score(ref, can)
        ref = self.tokenizer.encode(ref[0])
        can = self.tokenizer.encode(can)
        ref = list(filter(lambda x: x != self.tokenizer.pad_id, ref))
        can = list(filter(lambda x: x != self.tokenizer.pad_id, can))
        bleu = calc_bleu(ref, can)
        rl = calc_rouge_l(ref, can)
        return '#bleu#{0}#rougel#{1}#bert_p#{2}#bert_r#{3}#bert_f1#{4}#r_bert_p#{5}#r_bert_r#{6}#r_bert_f1#{7}'.format(round(bleu, 9), round(rl, 8), bert_p, bert_r, bert_f1, bert_p/r_bert_p, bert_r/r_bert_r, bert_f1/r_bert_f1)

   
app = Flask(__name__)
ctx = Context(MODEL_PATH)

@app.route('/CoupletAI/<coupletup>')
def api(coupletup):
    if coupletup:
        couplet = coupletup
        coupletup = couplet.split('&')[0]
        coupletdown = ctx.predict(coupletup)
        if '&' in couplet:
       	    ref = couplet.split('&')
            return ctx.evaluate(ref, coupletdown)
        return coupletdown
    return 'Not support None string.'

@app.route('/CoupletAI/', methods=['GET'])
def index():
    couplet = request.args.get("coupletup")
    if couplet:
        coupletup = couplet.split('&')[0]
        coupletdown = ctx.predict(coupletup)
        if '&' in couplet:
            ref = couplet.split('&')
            return ctx.evaluate(ref, coupletdown)
        return coupletdown
    return 'Not support None string.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
