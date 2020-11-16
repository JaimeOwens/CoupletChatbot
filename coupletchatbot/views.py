from coupletchatbot.models import User
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from . import forms
from . import models
import os

def index(request):
    pass
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = make_password(login_form.cleaned_data['password'], "a")
            try:
                user = models.User.objects.get(email=email)
                if password == user.password:
                    return redirect('/index/')
                else:
                    print(user.password)
                    print(make_password(password))
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
                        password = make_password(password1, "a")
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
    if request.is_ajax():
        ajax_string = 'ajax request'
    else:
        ajax_string = 'not ajax request'
    resp = HttpResponse(ajax_string)
    return resp

def dialog(request):
    pass
    return render(request, 'ajax.html')