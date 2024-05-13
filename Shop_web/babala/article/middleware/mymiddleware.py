from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleWare(MiddlewareMixin):
    """中间件判断是否登录"""
    def process_request(self, request):
        # 1、排除那些不需要登录就能访问的页面
        # request.path_info  获取当前用户请求的URL
        path = [
              '/', '/login/', '/register/', '/code/', '/forgot_password/'
        ]
        if request.path_info in path:
            return
        # 2、读取当前访问的用户的session信息，如果能读到，说明以登录过，就可以继续向后走
        info_dict = request.session.get("info")
        if info_dict:
            return
        # 3、没有登录过，重新回到登录页面
        return HttpResponseRedirect('/login/')
