from django import forms
from captcha.fields import CaptchaField


class MessageBoardForm(forms.Form):
    username = forms.CharField(label='账号')
    password = forms.CharField(label='密码')
    title = forms.CharField(max_length=3, label='标题', min_length=2,
                            error_messages={'min_length': '错误信息'})
    content = forms.CharField(widget=forms.Textarea, label='内容')
    email = forms.EmailField(label='邮箱')
    reply = forms.BooleanField(required=False, label='回复')


class Register(forms.Form):
    username = forms.CharField(label='账号')
    first_password = forms.CharField(label='第一次密码')
    second_password = forms.CharField(label='第二次密码')
    email = forms.EmailField(label='邮箱(接受验证码)')


class LoginForm(forms.Form):
    username = forms.CharField(
        label='姓名',
        required=True,
        min_length=3,
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "请输入用户名"
        }),
        error_messages={
            'required': '用户名不能为空',
            'min_length': '长度不能小于3个字符',
            'max_length': '长度不能超过10个字符',
        }
    )

    password = forms.CharField(
        label='密码',
        required=True,
        min_length=6,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control mb-0',
            'placeholder': "请输入密码"
        }),
        error_messages={
            'required': '用户名不能为空',
            'min_length': '长度不能少于6个字符',
            'max_length': '长度不能超过50个字符',
        }
    )

    captcha = forms.CharField(
        label='验证码',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-0',
            'placeholder': "请输入验证码"
        }),
        error_messages={
            'required': '验证码不能为空',
        }
    )


class VerificationForm(forms.Form):
    code = forms.CharField(
        label='验证码',
        required=True,
        max_length=5,
        min_length=5,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "请输入验证码"
        }),
        error_messages={
            'required': '验证码不能为空',
            'max_length': '请输入五位数验证码',
            'min_length': '请输入五位数验证码',
        }
    )


class ForgotPassword(forms.Form):
    username = forms.CharField(label='用户名')
    first_password = forms.CharField(label='第一次密码', min_length=6,
                                     error_messages={'min_length': '密码长度不得低于六位数'})
    second_password = forms.CharField(label='第二次密码', min_length=6,
                                      error_messages={'min_length': '密码长度不得低于六位数'})
    email = forms.EmailField(label='邮箱(接受验证码)')


class OrdersForm(forms.Form):
    receive_name = forms.CharField(label='收件人')
    receive_address = forms.CharField(label='收货地址')
    receive_tel = forms.IntegerField(label='电话')
    remake = forms.CharField(label='备注', required=False)
