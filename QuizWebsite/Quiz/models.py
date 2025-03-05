from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    gender=models.CharField(max_length=10)
    age=models.IntegerField()
    score=models.IntegerField(default=0)


class Course(models.Model):
    cname = models.CharField(max_length=20,unique=True) 

class Quiz(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
