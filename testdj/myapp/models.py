from django.db import models


# 有一个数据表就对应一个model,与数据库交互
# models.Model
# Create your models here.
class Grades(models.Model):
    gname = models.CharField(max_length=20)
    gdate = models.IntegerField()
    # gdate = models.DateTimeField()
    ggirlnum = models.IntegerField()
    gboynum = models.IntegerField()
    isDelete = models.BooleanField(default=False)
    def __str__(self):
        return '%s-%d-%d'%(self.gname, self.gboynum,self.ggirlnum)

class Students(models.Model):
    sname = models.CharField(max_length=20)
    sgender = models.BooleanField(default=True)
    sage = models.IntegerField()
    scontend = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)
    # 关联外键
    sgrade = models.ForeignKey('Grades', on_delete=models.CASCADE)

'''说明.不需要定义主键，在生成 时自动添加，并且值为自动添加'''