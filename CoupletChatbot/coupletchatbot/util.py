from coupletchatbot.models import Corpus, User
from django.core import serializers
from urllib import parse,request
import requests
import datetime
import json
import re
import random

couplet_p = re.compile(r'\“(.*)\”', re.S)
rasabotIP = '45.77.180.242'
rasabotPort = '5005'
rasaDialogURL = "http://{0}:{1}/webhooks/rest/webhook".format(rasabotIP, rasabotPort)
rasaIntentURL = "http://{0}:{1}/model/parse".format(rasabotIP, rasabotPort)

coupletIP = '45.32.23.74'
coupletPort = '5000'
coupletURL = 'http://{0}:{1}/CoupletAI/'.format(coupletIP, coupletPort)

def getCoupletRight(couplet_up):  
    params = {'coupletup': couplet_up}
    params = parse.urlencode(params)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
    response = request.Request(url='%s%s%s' % (coupletURL,'?', params), headers=headers)
    response = request.urlopen(response)
    response = response.read()
    return response.decode('utf8')

def getDialogContext(dialog):
    params = {'sender': 'chatbot', 'message': dialog}  
    response = requests.post(
        rasaDialogURL,
        data=json.dumps(params),
        headers={'Content-Type': 'application/json'}
    )
    dialog_return = response.text.encode('utf-8').decode("unicode-escape")
    dialog_return = dialog_return.strip('[]')
    if dialog_return == "":
        dialog_return = "抱歉，不知道说什么了"
    else:
        dialog_return = json.loads(dialog_return)
        dialog_return = dialog_return['text']
    
    params = {'text':dialog}  
    response = requests.post(
        rasaIntentURL,
        data=json.dumps(params),
        headers={'Content-Type': 'application/json'}
    )
    intent_return = response.text.encode('utf-8').decode("unicode-escape")
    intent_return = intent_return.strip('[]')
    intent_return = json.loads(intent_return)
    intent_return = intent_return['intent']
    intent_return = intent_return['name']

    return dialog_return, intent_return

def processSentence(raw_string, userid, sessionid):
    couplet_up =  re.findall(couplet_p, raw_string)
    intent = ""
    if len(couplet_up) != 0:
        couplet_c = '“' + couplet_up[0] + '”'
        dialog = raw_string.replace(couplet_c, '')
        couplet_down = getCoupletRight(str(couplet_up[0]))
        dialog_return, intent_return = getDialogContext(dialog)
        answer = dialog_return + "，“" + couplet_down + "”。"
        intent = intent_return
        Corpus.objects.create(id=None, userid=userid, uuid=sessionid, timestamp=datetime.datetime.now(), first_couplet=couplet_up[0], second_couplet=couplet_down, status=1, quality=1)
    else:
        answer, intent = getDialogContext(raw_string)
        answer = answer + "。"
    
    return answer, intent
    
def getBLEUandROUGH(couplet):
    params = {'coupletup': couplet}
    params = parse.urlencode(params)
    response = request.Request(url='%s%s%s' % (coupletURL,'?', params))
    response = request.urlopen(response)
    response = response.read()
    result = response.decode('utf8')
    result = result.split('#')
    # for i in range(len(result)):
    #    print(result[i])
    bleu = float(result[2])
    rougel = float(result[4])
    bert_p = float(result[6])
    bert_r = float(result[8])
    bert_f1 = float(result[10])
    r_bert_p = float(result[12])
    r_bert_r = float(result[14])
    r_bert_f1 = float(result[16]) 
    return bleu, rougel, bert_p, bert_r, bert_f1, r_bert_p, r_bert_r, r_bert_f1
