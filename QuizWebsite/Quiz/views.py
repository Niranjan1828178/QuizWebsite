from django.shortcuts import render,redirect
from django.http import HttpResponse
import json
from .models import * 
import os
import random
from django.core.files.storage import default_storage
from django.conf import settings


from django.contrib.staticfiles.storage import staticfiles_storage

def load_questions():
    file_path = os.path.join(settings.BASE_DIR, 'Quiz', 'static', 'Quiz', 'question.json')
    with default_storage.open(file_path) as f:
        Questions = json.load(f)
    return Questions




def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(name=username,password=password):
            user=User.objects.get(name=username)
            request.session['uid'] = user.id
            return redirect('Course')
        else:
            return render(request, 'Quiz/Login.html', {'error': 'Invalid username or password'})
    return render(request, 'Quiz/Login.html', {'error': 'Invalid Method'})


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmPassword']
        gender = request.POST['gender']
        age = request.POST['age']
        if password!= confirm_password:
            return render(request, 'Quiz/Register.html', {'error': 'Passwords do not match'})
        if User.objects.filter(name=username).exists():
            return render(request, 'Quiz/Register.html', {'error': 'Username already exists'})
        user = User(name=username, email=email, password=password, gender=gender, age=age)
        user.save()
        return redirect('loginUser')
    return render(request, 'Quiz/Register.html')

def Courses(request):
    uid=request.session.get('uid')
    topics = list(Course.objects.values_list('cname', flat=True))
    courses = {"uid":uid,"topics": topics} #pass into context as before
    return render(request, 'Quiz/Course.html',courses)


def Quiz_gen(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        request.session['topic'] = topic
        if topic=="" or topic== None :
            return redirect('Course')
        q=[]
        nu=[]
        Questions=load_questions()
        Questions=Questions[topic]
        for _ in range(10):
            rn=random.randint(0,10)
            while rn in nu:
                rn=random.randint(0,10)
            nu.append(rn)
            q.append(Questions[rn])

        questions = {"topic":topic,"questions":q}
        return render(request, 'Quiz/Quiz.html',questions)

    return redirect('Course')
def Exam(request):
    if request.method == 'POST':
        topic = request.session.get('topic')
        uid =int( request.session.get('uid'))
        user=User.objects.get(id=uid)
        Questions=load_questions()
        question=Questions[topic]
        score=0
        wrong_answer=[]
        for q in question:
            correct_answer = q["options"][int(q["answer"])]
            selected_answer = request.POST.get(str(q["id"]))
            if selected_answer != None:
                if correct_answer == selected_answer:
                    score+=1
                else:
                    if wrong_answer:
                        t=True
                        for i in wrong_answer:
                            if q["subtopic"] ==i[0]:
                               t=False
                        if t:
                            da=[q["subtopic"],q["link"]]
                            wrong_answer.append(da)
                    else:
                        da=[q["subtopic"],q["link"]]
                        wrong_answer.append(da)
        course=Course.objects.get(cname=topic)
        if  Quiz.objects.filter(user=user, course=course).exists():
            q=Quiz.objects.get(user=user, course=course)
            q.score=score
            q.save()
        else:
            Quiz.objects.create(user=user, course=course, score=score).save()
        userlist=Quiz.objects.filter(user=uid)
        tscore=0
        for q in userlist:
            tscore+=q.score
        u=User.objects.get(id=uid)
        u.score=tscore
        u.save()
        data=Feedback(uid,topic,wrong_answer)
        return render(request,'Quiz/Feedback.html',data)
    return render(request, 'Quiz/Quiz.html')

def Feedback(uid,topic,wrong_answer):
    tid=Course.objects.get(cname=topic)
    user=Quiz.objects.get(user=uid,course=tid.id)
    per=(user.score/10)*100
    ur={"score":user.score,"topic":topic,"percentage":per,"improvement":wrong_answer}
    return ur

def Logout(request):
    request.session.flush()
    return redirect('Home')

def Reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user=User.objects.get(email=email)
        user.password=password
        user.save()
        return redirect('loginUser')
    return render(request, 'Quiz/Reset.html')

def profile(request):
    uid =int( request.session.get('uid'))
    userlist=User.objects.all().order_by('-score')
    user=User.objects.get(id=uid)
    rank=0
    k=0
    while True:
        if user.id==userlist[k].id:
            rank=k+1
            break
        k+=1
    data={"name":user.name,"email":user.email,"gender":user.gender,"age":user.age,"score":user.score,"rank":rank}
    print(data)
    return render(request, 'Quiz/Profile.html',data)

def Leaderboard(request):
    userlist=User.objects.all().order_by('-score','name')
    li=[]
    i=1
    for user in userlist:
        li.append({"name":user.name,"score":user.score,"rank":i})
        i+=1
    first=li[:3]

    leaderboard={"userlist":li[3:], "first":first}
    return render(request, 'Quiz/Leaderboard.html',leaderboard)
