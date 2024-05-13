from datetime import datetime, timedelta
import threading
import time
from io import BytesIO
from django.core.mail import send_mail
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as django_logout
from .models import MyUser
from .forms import LoginForm, VerificationForm, Register, ForgotPassword
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .captcha import *


class Getcode(View):
    def get(self, request):
        image, code = get_verify_code()
        # 图片以二进制形式写入
        buf = BytesIO()
        image.save(buf, 'jpeg')
        buf_str = buf.getvalue()
        # 把buf_str作为response返回前端，并设置首部字段
        response = HttpResponse(buf_str, content_type='image/jpeg')
        response.headers['Content-Type'] = 'image/jpeg'
        # 将验证码字符串储存在session中
        self.request.session['image'] = code
        return response


def Email(verification_code, email):
    EMAIL_HOST_USER = '3353580932@qq.com'
    t = threading.Thread(
        target=send_mail,
        args=(
            "您有一封邮件",  # 邮件标题
            f'您的验证码为：{verification_code}',  # 邮件内容（文本）
            EMAIL_HOST_USER,  # 发送邮件的邮箱地址
            [email],  # 接收邮件的邮箱地址列表
        ),
        kwargs={
            'html_message': f"<p>您的验证码为：</p><p>{verification_code}</p>"
        }
    )
    t.start()
    return JsonResponse({"code": 200, 'msg': '邮件发送成功，请查收'})


class GetRegister(View):
    def get(self, request):
        form = Register()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        last_send_time = self.request.session.get('last_send_time')
        form = ForgotPassword(request.POST)
        if not last_send_time or (datetime.now() - datetime.fromisoformat(last_send_time)) > timedelta(seconds=90):
            self.request.session['last_send_time'] = datetime.now().isoformat()
            if form.is_valid():
                email = form.cleaned_data.get('email')
                first_password = form.cleaned_data.get('first_password')
                second_password = form.cleaned_data.get('second_password')
                username = form.cleaned_data.get('username')
                if first_password != second_password:
                    messages.add_message(request, messages.INFO, '前后两次密码不一致')
                    return render(request, 'forgot_password.html', {'form': form})
                else:
                    Verification_code = random.randrange(10001, 99999)
                    self.request.session['Verification_code'] = Verification_code
                    self.request.session['username'] = username
                    self.request.session['password'] = first_password
                    self.request.session['email'] = email
                    self.request.session['type'] = 'register'
                    print(Verification_code)
                    Email(Verification_code, email)
                    return HttpResponseRedirect('/Verification/')
        else:
            messages.add_message(request, messages.INFO, '请等待90秒后再次尝试获取邮件。')
            return render(request, 'register.html',
                          {'form': form})


class Forgot(View):
    def get(self, request):
        form = ForgotPassword()
        return render(request, 'forgot_password.html', {'form': form})

    def post(self, request):
        last_send_time = self.request.session.get('last_send_time')
        form = ForgotPassword(request.POST)
        if not last_send_time or (datetime.now() - datetime.fromisoformat(last_send_time)) > timedelta(seconds=90):
            self.request.session['last_send_time'] = datetime.now().isoformat()
            if form.is_valid():
                email = form.cleaned_data.get('email')
                first_password = form.cleaned_data.get('first_password')
                second_password = form.cleaned_data.get('second_password')
                username = form.cleaned_data.get('username')
                if first_password != second_password:
                    messages.add_message(request, messages.INFO, '前后两次密码不一致')
                    return render(request, 'forgot_password.html', {'form': form})
                else:
                    Verification_code = random.randrange(10001, 99999)
                    self.request.session['Verification_code'] = Verification_code
                    self.request.session['username'] = username
                    self.request.session['password'] = first_password
                    self.request.session['email'] = email
                    self.request.session['type'] = 'Forgot'
                    print(Verification_code)
                    Email(Verification_code, email)
                    return HttpResponseRedirect('/Verification/')
        else:
            messages.add_message(request, messages.INFO, '请等待90秒后再次尝试获取邮件。')
            return render(request, 'forgot_password.html', {'form': form})


class Verification(View):
    def get(self, request):
        form = VerificationForm()
        return render(request, 'verification.html', {'form': form})

    def post(self, request):
        form = VerificationForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data.get('code')
            username = self.request.session['username']
            password = make_password(self.request.session['password'])
            Verification_code = int(self.request.session['Verification_code'])
            Type = self.request.session['type']
            if int(number) == Verification_code:
                if Type == 'register':
                    MyUser.objects.create(username=self.request.session['username'],
                                          password=password,  # 开启密码加密
                                          email=self.request.session['email'],
                                          addtime=datetime.now())
                    messages.add_message(request, messages.INFO, '注册成功')
                    return HttpResponseRedirect('/login/')
                if Type == 'Forgot':
                    try:
                        MyUser.objects.get(username=username)
                        MyUser.objects.filter(username=username).update(password=password)
                        messages.add_message(request, messages.INFO, '修改密码成功')
                        return HttpResponseRedirect('/login/')
                    except:
                        messages.add_message(request, messages.INFO, '用户名不存在')
                        return HttpResponseRedirect('/forgot_password/')

            else:
                messages.add_message(request, messages.INFO, '验证码错误，请重新输入')
                return render(request, 'Verification.html', {'form': form})
        else:
            # messages.add_message(request, messages.INFO, form.errors)
            return render(request, 'Verification.html', {'form': form})


def logout(request):
    """
    退出登录
    """
    django_logout(request)  # 清除response的cookie和django_session中记录
    return HttpResponseRedirect('/')
