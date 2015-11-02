from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login


def login(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(req, user)
            return redirect('home', student_username=username)

    return render(req, 'mines_book/login.html')


def home(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    context = {"user": user, "posts": user.student.posts_received.all()}
    return render(req, 'mines_book/user.html', context)


def user_feed(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    context = {"user": user, "posts": user.student.posts_received.all()}
    return render(req, 'mines_book/user_feed.html', context)


def user_friends(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    context = {"students": user.student.friends.all()}
    return render(req, 'mines_book/student_cards.html', context)

def user_joined_groups(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    context = {"groups": user.student.groups_joined.all()}
    return render(req, 'mines_book/group_cards.html', context)
