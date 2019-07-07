from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:num>/',views.detail,name = 'detail'),
    path('grades/', views.grades, name = 'grades'),
    path('students/',views.students, name = 'students'),
    path('grades/<int:num>/', views.gradein)
]
