"""babala URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from . import views
from django.contrib import admin
from django.urls import path, re_path, include
# from django.conf.urls import url
# from babala.modeltest import views_model
# from babala.article import views_article
# from django.conf.urls import handler400, handler403, handler404, handler500

urlpatterns = [
    path('', include('article.urls')),
    path('admin/', admin.site.urls),
]

# handler400 = views.bad_request
# handler403 = views.permission_denied
# handler404 = views.page_not_found
# handler500 = views.server_error

