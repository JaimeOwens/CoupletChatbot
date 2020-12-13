from coupletchatbot.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from . import forms
from . import models
from . import util
import uuid
import json

def index(request):
    print(request.COOKIES.get('userid'))
    status = request.COOKIES.get('userid')
    if not status:
        return render(request, 'index.html')
    else:
        return redirect('/dialog/')

def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(email=email)
                if password == user.password:
                    rep = redirect('/index/')
                    sessionid = str(uuid.uuid1())
                    rep.set_cookie('userid', user.userid)
                    rep.set_cookie('username', user.username)
                    rep.set_cookie('uuid', sessionid)
                    request.session[user.userid] = sessionid
                    return rep
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
            return render(request, 'login.html', locals())
        else:
            message = "请检查填写的内容！"
            return redirect('/login/')
    login_form = forms.LoginForm()
    return render(request, 'login.html', locals())

def register(request):
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():  
            email = register_form.cleaned_data['email']
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:  
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(email=email)
                if same_name_user: 
                    message = '邮箱已经存在，请重新选择邮箱！'
                    return render(request, 'register.html', locals())
                else:
                    try:
                        password = password1
                        User.objects.get_or_create(userid=None, email=email, username=username, password=password, avatar=None)
                    except Exception as e:
                        print(e)
                    return redirect('/index/')
        else:
            message = "请检查填写的内容！"
            return redirect("/register/")
    register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())

def input(request):
    intent = '' 
    if request.is_ajax():
        userid = request.COOKIES.get('userid')
        sessionid = request.session.get(userid)
        if sessionid == None:
            request.session[userid] = str(uuid.uuid1())
            sessionid = request.session.get(userid)     
        ajax_string, intent = util.processSentence(request.GET["text"], userid, sessionid)
        print(ajax_string, intent)
        if intent == 'goodbye':
            del request.session[userid]
    else:
        ajax_string = 'not ajax request'
    return_dict = {'text':ajax_string, 'intent':intent}
    resp = HttpResponse(json.dumps(return_dict),content_type='application/json')
    return resp

def dialog(request):
    pass
    return render(request, 'dialog.html')

def change(request):
    pass
    return render(request, 'change.html')

def person(request):
    pass
    return render(request, 'person.html')

