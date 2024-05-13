from django.db import models

# Create your models here.
from django.db import models  # 引入django.db.models模块
from django.forms import ModelForm, Textarea, DateInput, TextInput
from django import forms
from django.contrib.auth.models import AbstractUser


class MyUser(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    username = models.CharField(max_length=30)  # 用户名
    password = models.CharField(max_length=30)  # 密码
    email = models.EmailField(unique=True)  # 邮箱，Django提供了EmailField
    phone = models.IntegerField(unique=True, null=True, blank=True)  # 手机号
    consumption = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 消费额
    addtime = models.DateTimeField()  # 注册时间

    def __str__(self):
        return self.username


class Admin(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    manager = models.CharField(max_length=30, unique=True)  # 管理员账号
    password = models.CharField(max_length=30)  # 管理员密码

    def __str__(self):
        return self.manager


class SuperCat(models.Model):
    id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=30)
    addtime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name


class SubCat(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    cat_name = models.CharField(max_length=30)
    addtime = models.DateTimeField(auto_now_add=True)
    super_cat = models.ForeignKey(SuperCat, on_delete=models.CASCADE)  # 外键关联大分类

    def __str__(self):
        return self.cat_name


class Goods(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    name = models.CharField(max_length=50)
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='goods/')  # Django提供了ImageField和FileField
    introduction = models.TextField()
    views_count = models.IntegerField(default=0)
    comment = models.TextField(null=True)
    is_sale = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    supercat = models.ForeignKey(SuperCat, on_delete=models.CASCADE)  # 外键关联大分类
    subcat = models.ForeignKey(SubCat, on_delete=models.CASCADE, null=True, blank=True)  # 外键关联子分类，可为空

    def update_name_prefix(self):
        # 检查 name 是否包含 '手机_'，如果包含则替换为 '数码_'
        if '手机_' in self.name:
            self.name = self.name.replace('手机_', '数码_')

    def __str__(self):
        return self.name


class Cart(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)  # 外键关联商品
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # 外键关联用户
    number = models.IntegerField(default=0)

    def __str__(self):
        return f"Cart {self.id} for user {self.user.username}"


class Orders(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # 外键关联用户
    receive_name = models.CharField(max_length=50)
    receive_address = models.CharField(max_length=50)
    receive_tel = models.CharField(max_length=50)
    remark = models.TextField(blank=True)  # 可以为空
    addtime = models.DateTimeField()


    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    @classmethod
    def create_or_get(cls, user, receive_name, receive_address, receive_tel, remark, addtime):
        pass


class OrdersDetail(models.Model):
    id = models.AutoField(primary_key=True)  # 自增主键
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)  # 外键关联商品
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)  # 外键关联订单
    number = models.IntegerField(default=0)

    def __str__(self):
        return f"Order detail {self.id} for order {self.order.id}"
