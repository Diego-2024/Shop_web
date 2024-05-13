from django.contrib import admin

from django.urls import path, re_path, include
from . import views_article, make_user
from babala.ganyu import views



#
urlpatterns = [
    path('', views_article.index, name='index'),
    # path('<int:year>/', views.year_archive, name='year_archive'),
    # path('<int:year>/<int:month>/', views.month_archive, name='month_archive'),
    # path('<int:year>/<int:month>/<slug:slug>/', views.article_detail, name='article_detail'),
    # path('current', views.get_current_datetime, name='current_datetime'),
    # path('register', views.Register, name='register'),
    path('login/', views_article.LoginFormView.as_view(), name='login'),
    path('logout/', make_user.logout, name='logout'),
    path('code/', make_user.Getcode.as_view(), name='captcha_image'),
    # path('set_session/', views_article.set_session, name='set_session'),
    # path('get_session/', views_article.get_session, name='get_session'),
    path('register/', make_user.GetRegister.as_view(), name='register'),
    path('forgot_password/', make_user.Forgot.as_view(), name='forgot_password'),
    path('Verification/', make_user.Verification.as_view(), name='verification'),
    path('display/', views_article.Display.as_view(), name='display'),
    path('goods_detail/<int:goods_id>/', views_article.goods_detail, name='goods_detail'),
    path('index/<int:supercat_id>/page/<int:page>/', views_article.IndexView.as_view(), name='index'),
    path('cart_add/', views_article.add_to_cart, name='cart_add'),
    path('shop_cart/', views_article.ShopCart.as_view(), name='shop_cart'),
    path('pay/', views_article.Pay.as_view(), name='pay'),
    path('orders_detail/', views_article.Orders_detail, name='orders_detail'),
    path('clear_cart/', views_article.ClearCart, name='clear_cart'),
]