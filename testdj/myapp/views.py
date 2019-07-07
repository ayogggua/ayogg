from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse('超贼帅')
def detail(request,num):
    return HttpResponse("超哥%s"%num)

from .models import Grades
def grades(request):
    # 去模板里取数据
    grade_list = Grades.objects.all()
    # 将数据传递给模板，模板再渲染页面，将渲染好的页面返回给浏览器
    return render(request, 'myapp/grades.html', {"grades":grade_list})
from .models import Students
def students(request):
    student_list = Students.objects.all()
    return render(request, 'myapp/students.html', {"students":student_list})

def gradein(request,num):
    grade = Grades.objects.get(pk=num)
    student_list = grade.students_set.all()
    return render(request, 'myapp/students.html', {"students": student_list})

