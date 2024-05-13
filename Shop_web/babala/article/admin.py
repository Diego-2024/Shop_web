from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MyUser


# from babala.article.models import



class UserAdmin(admin.ModelAdmin):
    """
    创建UserAdmin类，继承于admin.ModelAdmin
    """
    #  配置展示列表，在User版块下的列表展示
    list_display = ('username', 'email')
    # 配置过滤查询字段，在User版块下右侧过滤框
    list_filter = ('username', 'email')
    # 配置可以搜索的字段，在User版块下右侧搜索框
    search_fields = (['username', 'email'])


class ArticleAdmin(admin.ModelAdmin):
    """
    创建UserAdmin类，继承于admin.ModelAdmin
    """
    fieldsets = (
        ('main', {
            'fields': (('id', 'title'), 'publish_date', 'user')
        }),
        ('Advance', {
            'classes': ('collapse',),
            'fields': ('content',),
        })
    )

    def upp_case_name(self, obj):
        return ("%s %s" % (obj.id, obj.title)).upper()

    upp_case_name.short_description = 'Name'



    #  配置展示列表，在Article版块下的列表展示
    list_display = ('id','title', 'content', 'publish_date')
    # 修改跳转链接
    # list_display_links = ('content',)
    # 显示编辑框
    # list_editable = ('title', 'publish_date')
    # 配置过滤查询字段，在User版块下右侧过滤框
    list_filter = ('title', 'user__username')  # list_filter应该是列表或元组
    # 配置可以搜索的字段，在User版块下右侧搜索框
    search_fields = ('title', 'content')  # search_fields应该是列表或元组





# 绑定User模型到UserAdmin管理后台
admin.site.register(MyUser, UserAdmin)
# 绑定User模型到UserAdmin管理后台

