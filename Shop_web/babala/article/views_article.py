from django.db.models import F
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.views import View
from django.shortcuts import render, redirect
from .models import MyUser, Goods, Cart, Orders, OrdersDetail
from .forms import LoginForm, VerificationForm, Register, ForgotPassword
from django.contrib.auth import authenticate, login, logout as django_logout
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import pymysql
from django.core.paginator import Paginator
from .forms import OrdersForm


def index(request):
    goods = Goods.objects.all()[:6]
    return render(request, 'index.html', {'Goods': goods})


class LoginFormView(View):
    def get(self, request, *args, **kwargs):
        """
        定义GET请求的方法GET请求
        """
        return render(request, 'login.html', {'form': LoginForm()})

    def post(self, request, *args, **kwargs):
        """
        定义POST请求的方法GET请求
        """
        # 将请求数据填充到LoginForm实例中
        form = LoginForm(request.POST)
        # 判断是否为有效表单
        if form.is_valid():
            # 使用form.cleaned_data获取请求的数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            Captcha = form.cleaned_data['captcha']
            # user = MyUser.objects.filter(username=username)
            code = self.request.session['image']
            if Captcha.lower() == code.lower():
                # try:
                user = MyUser.objects.get(username=username)
                encrypt_pwd = user.password
                if check_password(password, encrypt_pwd):
                    self.request.session['info'] = {'username': username}
                    try:
                        user_id = MyUser.objects.get(username=username).id
                        self.request.session['user_id'] = user_id
                    except MyUser.DoesNotExist:
                        return HttpResponse("用户不存在")
                    goods = Goods.objects.all()[:6]
                    return render(request, 'display.html', {'Goods': goods})
                # except:

                messages.add_message(request, messages.WARNING, '登录失败')
                return render(request, 'login.html',
                              {'form': form})
            else:
                messages.add_message(request, messages.WARNING, '验证码错误')
                return render(request, 'login.html', {'form': form})

        return render(request, 'login.html', {'form': form})  # 渲染模板


def goods_detail(request, goods_id):
    goods = Goods.objects.get(id=goods_id)
    goods.views_count = F('views_count') + 1
    goods.save(update_fields=['views_count'])
    return render(request, 'goods_detail.html', {'goods': goods})


def add_to_cart(request):
    goods_id = request.GET.get('goods_id')
    number = request.GET.get('number')
    user_id = int(request.session['user_id'])
    if goods_id and number:
        try:
            number = int(number)
            cart, created = Cart.objects.get_or_create(
                user_id=user_id,
                goods_id=goods_id,
                defaults={'number': number}
            )
            if not created:
                cart.number += number
                cart.save()
            messages.add_message(request, messages.WARNING, '商品已添加到购物车')
            return HttpResponseRedirect(f'/goods_detail/{goods_id}/')
        except ValueError:
            messages.add_message(request, messages.WARNING, '无效的商品数量')
            return HttpResponseRedirect(f'goods_detail/{goods_id}/')
    else:
        messages.add_message(request, messages.WARNING, '缺少必要的查询参数')
        return HttpResponseRedirect(f'/goods_detail/{goods_id}/')


class ShopCart(View):
    def get(self, request):
        user_id = int(self.request.session['user_id'])
        cart = Cart.objects.filter(user_id=user_id)
        return render(request, 'shop_cart.html', {'cart': cart})

    def post(self, request):
        return HttpResponse('哈哈')


def ClearCart(request):
    user_id = int(request.session['user_id'])
    Cart.objects.filter(user_id=user_id).delete()
    return HttpResponseRedirect('/shop_cart/')


class Pay(View):
    def get(self, request):
        form = OrdersForm()
        return render(request, 'pay.html', {'form': form})

    def post(self, request):
        form = OrdersForm(request.POST)
        if form.is_valid():
            receive_name = form.cleaned_data.get('receive_name')
            receive_address = form.cleaned_data.get('receive_address')
            receive_tel = form.cleaned_data.get('receive_tel')
            user_id = int(request.session.get('user_id', 0))
            user = MyUser.objects.get(id=user_id)
            with transaction.atomic():
                try:
                    orders = Orders.objects.create(
                        user=user,
                        receive_name=receive_name,
                        receive_address=receive_address,
                        receive_tel=receive_tel,
                        remark="快递",
                        addtime=datetime.now(),
                    )
                    # 获取当前用户的购物车项
                    cart_items = Cart.objects.filter(user_id=user_id)
                    # 遍历购物车项并创建OrdersDetail对象
                    orders_details = [
                        OrdersDetail(
                            order=orders,
                            goods=Goods.objects.get(pk=item.goods_id),
                            number=item.number,
                        )
                        for item in cart_items
                    ]
                    # 使用bulk_create来批量创建订单详情，减少数据库操作次数
                    OrdersDetail.objects.bulk_create(orders_details)
                    # 清空购物车
                    Cart.objects.filter(user_id=user_id).delete()
                    return HttpResponseRedirect('/orders_detail/')
                except Exception as e:
                    # 这里应该记录日志或者提供错误处理，而不是仅仅返回失败信息
                    return HttpResponse('快递数据添加失败，原因：' + str(e))
        else:
            # 这里应该把错误信息传回模板显示
            return render(request, 'pay.html', {'form': form})


def Orders_detail(request):
    user_id = int(request.session['user_id'])
    orders = Orders.objects.filter(user_id=user_id)
    # 初始化一个空的 OrdersDetail 实例列表
    orders_details = []
    # 检查 Orders 查询结果不为空
    if orders.exists():
        # 遍历 Orders 实例，并为每个实例获取相关的 OrdersDetail 实例
        for order in orders:
            # 使用 filter 而不是 join 来获取与 Orders 实例相关的 OrdersDetail 对象
            # 这里假设您想要获取所有与订单相关的详情，不仅限于一个
            order_details = OrdersDetail.objects.filter(order_id=order.id)
            orders_details.extend(order_details)
    return render(request, 'orders_detail.html', {'orders': orders_details})


class Display(View):
    def get(self, request):
        # 视图逻辑处理
        goods = Goods.objects.all()[:6]
        return render(request, 'display.html', {'Goods': goods})

    def post(self, request):
        # 视图逻辑处理
        goods = Goods.objects.all()[:6]
        return render(request, 'display.html', {'Goods': goods})


def Collaborative_Filtering():
    return



# 网页分页
class IndexView(View):
    """数据分页显示"""

    def get(self, request, supercat_id, page):
        """分页显示"""
        goods = Goods.objects.filter(supercat_id=supercat_id).order_by('id')
        paginator = Paginator(goods, 6)  # 每页显示6条数据

        # 尝试将page参数转换为整数，并检查页码是否有效
        try:
            page = int(page)
        except ValueError:
            page = 1

        if page < 1 or page > paginator.num_pages:
            page = 1

        # 获取第page页的Page实例对象
        shop_page = paginator.page(page)

        # 构造数据并返回
        context = {
            'shop_page': shop_page,
            'supercat_id': supercat_id,  # 将supercat_id传递给模板
            'pages': range(1, paginator.num_pages + 1),  # 显示所有页码
        }
        return render(request, 'page.html', context)


