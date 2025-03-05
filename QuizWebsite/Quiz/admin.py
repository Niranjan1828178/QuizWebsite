from django.contrib import admin
from .models import *
# Register your models here


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'password', 'gender', 'age','score')
    list_filter = ('gender', 'age')
    search_fields = ['name', 'email']
    ordering = ('name','score')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('cname',)

class QuizAdmin(admin.ModelAdmin):
    list_display = ('user', 'course','score')

admin.site.register(User, UserAdmin)

admin.site.register(Course, CourseAdmin)

admin.site.register(Quiz, QuizAdmin)
