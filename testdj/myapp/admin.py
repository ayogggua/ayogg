from django.contrib import admin
# 站点管理
# Register your models here.
from .models import Grades, Students


# 界面管理
# 添加班级的时候添加五个学生

class StudentsInfo(admin.TabularInline):
    model = Students
    extra = 5


@admin.register(Students)#注册
class StudentsAdmin(admin.ModelAdmin):
    def gender(self):
        if self.sgender:
            return "男"
        else:
            return "女"
    gender.short_description = '性别'
    list_per_page = 5
    list_display = ['pk', 'sname', gender, 'sgrade','scontend', 'sage', 'isDelete']


@admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    inlines = [StudentsInfo]
    # 列表属性
    list_display = ['pk', 'gname', 'ggirlnum', 'gboynum', 'gdate', 'isDelete']
    # list_filter = []
    list_per_page = 5
    # 增加修改
    # 顺序
    # fields = []
    # 分组
    fieldsets = [
        ("num", {"fields": ['ggirlnum', 'gboynum']}),
        ("othoers", {"fields": ['gname', 'gdate', 'isDelete']}),
    ]



# 注册
# admin.site.register(Grades, GradesAdmin)
# admin.site.register(Students, StudentsAdmin)
