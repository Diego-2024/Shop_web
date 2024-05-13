import random

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
# from babala.article.models import ArticleModelForm
from django.core.mail import send_mail
import threading
from .settings import EMAIL_HOST_USER
from django.http import JsonResponse
from babala.article.forms import Register, VerificationForm
from django.contrib import messages


# Create your views here.

def article_list(request):
    return HttpResponse('article_list函数')


def year_archive(request, year):
    return HttpResponse(f'year_archive函数接收参数year:{year}')


def month_archive(request, year, month):
    return HttpResponse(f'month_archive函数接受参数year:{year},month:{month}')


def article_detail(request, year, month, slug):
    return HttpResponse(f'article_detail函数接受参数'
                        f'year:{year},month:{month},slug:{slug}')


def get_hello(request):
    # return HttpResponse('Hello Django')
    return render(request, 'index.html')


# class GetRegister(View):
#     def get(self, request):
#         form = Register()
#         return render(request, 'register.html', {'form': form})
#
#     def post(self, request):
#         form = Register()
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             first_password = form.cleaned_data.get('first_password')
#             second_password = form.cleaned_data.get('second_password')
#             email = form.cleaned_data.get('email')
#             return HttpResponse('success')
#         else:
#             # username = request.POST['username']
#             print(form.errors)
#             return HttpResponse('fail')


# def bad_request(request):
#     return render(request, 'errors/page_400.html')
# def permission_denied(request):
#     return render(request, 'errors/page_403.html')
# def page_not_found(reque#             username = form.cleaned_data.get('username')
# #             password = form.cleaned_data.get('password')
# #             title = form.cleaned_data.get('title')
# #             content = form.cleaned_data.get('content')
# #             email = form.cleaned_data.get('email')
# #             reply = form.cleaned_data.get('reply')st):
#     return render(request, 'errors/page_404.html')
# def server_error(request):
#     return render(request, 'errors/page_500.html')

# def Register(request):
#     if request.method == "POST":
#         form = MessageBoardForm()
#         if form.is_valid():

#             return HttpResponse(f'Date is {username}')
#         else:
#             return HttpResponse('error')
#     else:
#         return render(request, 'register.html',
#                       {'form': MessageBoardForm()})

# @login_required
# def add_article(request):
#     if request.method == 'GET':
#         form = ArticleModelForm()
#     else:
#         form = ArticleModelForm(request.POST)
#         if form.is_valid():
#             return HttpResponse(f'验证成功')
#     return render(request, 'add_article.html',
#                   {'form': form})


