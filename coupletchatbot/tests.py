from django.test import TestCase
import json
import random
from . import util
import xlwt


dialogs = {
    'greet': ['你好','你好啊','早上好','晚上好','中午好','hello','hi','见到你很高兴','见到你很开心','嗨','哈喽','喂','在吗','你在吗','有人在吗'],
    'goodbye': ['googbye','bye','bye bye','再见','回见','回头见','下次见','下次再见','拜','拜拜','下次聊','下次再聊','有空再聊','有事下次聊','有事下次再聊','就这样吧','先这样吧','好了先这样','好的先这样吧'],
    'affirm': ['yes','是的','好的','当然','可以','行','还行','同意','赞成','赞同','对的','嗯','ok'],
    'deny': ['no','不','不行','不可以','不是的','不赞成','不认同','否认','否定','不是这样的','不好','拒绝'],
    'thanks': ['谢谢','感谢','非常感谢','thanks','thank you'],
    'whoareyou': ['你是谁','请问你是谁','请你介绍一下','自我介绍一下','请你自我介绍一下','你是？','哪位？','你叫什么？','你叫什么名字？'],
    'whattodo': ['你支持什么功能','你有什么功能','你能干什么','你能做什么'],
    'couplet': ['我出个上联','出个上联','我出上联','你准备好对联游戏了吗','接受我的挑战吧','接受挑战吧','我想对对子','我想对联','我想对','上联是','这是上联','这是我的上联',
            '试试看吧','试试看','试一下','你会这个吗','你会吗','请给我一个下联','给我一个下联','给个下联','求下联','下联是什么','这条对应的下联是什么呢','对应的下联是什么呢',
            '下联是啥','有对应的下联吗','我想知道你的答案','我想知道答案','我想知道下联','我想要下联','想要下联'],
    'goodanswer': ['好答案','很好的答案','很棒的答案','不错的答案','绝妙的答案','答得好','答得棒','赞','非常好','很好','有道理','我从你这里学到了','学到了'],
    'badanswer': ['不好的答案','差劲的答案','不怎么样','回答有问题','无法解答我的疑惑','答非所问','不知道你在说什么','重新来过吧','重来吧','这个答案不好','拉倒','拉倒吧']
}

class CoupletTestCase(TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
        with open('testdata/300.json', 'r', encoding='utf8') as fp:
            self.jsondata = json.loads(fp.read())     

    def splitPoetry(self,content):
        content = content.split()
        couplet = content[random.randint(0, len(content)-1)]
        print(couplet)
        couplet = couplet.split('，')
        if len(couplet) == 2:
            first_couplet = couplet[0]
            second_couplet = couplet[1]
            second_couplet = second_couplet[:-1]
            couplet = first_couplet + '&' + second_couplet
        else:  
            couplet = "苔痕上阶绿&草色入帘青"
        return couplet

    def getTestCouplet(self):
        poetry_index = random.randint(0, 299)
        poetry = self.jsondata[poetry_index]
        return self.splitPoetry(poetry['contents'])

    def getDialog(self):
        intent = random.sample(dialogs.keys(), 1)
        intent = intent[0]
        dialog = random.choice(dialogs[intent]) 
        return dialog, intent

    def testAccuracy(self):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('sheet0')
        for i in range(1000):
            print(i)
            dialog, intent = self.getDialog()
            couplet = self.getTestCouplet()
            if couplet == "":
                continue
            print(dialog, intent, couplet)
            
            dialog_return, intent_return = util.getDialogContext(dialog)
            bleu, rough = util.getBLEUandROUGH(couplet)
            print(dialog_return, intent_return)
            print(bleu, rough)

            worksheet.write(i, 0, dialog)
            worksheet.write(i, 1, dialog_return)
            worksheet.write(i, 2, intent)
            worksheet.write(i, 3, intent_return)
            worksheet.write(i, 4, couplet)
            worksheet.write(i, 5, bleu)
            worksheet.write(i, 6, rough)
            
            self.assertEqual(intent, intent_return)

        workbook.save('testdata/test_result.xlsx')


        