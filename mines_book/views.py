from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models import ImageField
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from forms import GroupForm, PostForm
from models import Group, Post, PostToStudent
from utils import serialize_groups, serialize_students, serialize_students_select
import json


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
    new_post_form = PostForm()
    context = {"user": user, "posts": user.student.posts_received.all(), "form": new_post_form}
    return render(req, 'mines_book/user.html', context)


def user_feed(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    new_post_form = PostForm()
    context = {"user": user, "posts": user.student.posts_received.all(), "form": new_post_form}
    return render(req, 'mines_book/user_feed.html', context)

def user_profile(req, student_username):
    user = User.objects.get(username=student_username)[0]
    context = {"student": user.student}

def user_friends(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    context = {"students": user.student.friends.all()}
    return render(req, 'mines_book/student_cards.html', context)


def user_joined_groups(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    new_group_form = GroupForm()
    context = {"groups": user.student.groups_joined.all(), "form": new_group_form, "student": user}
    return render(req, 'mines_book/group_cards.html', context)


def new_group(req):
    user = req.user
    if req.method == 'POST':
        form = GroupForm(req.POST, req.FILES)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            name = cleaned_data['name']
            description = cleaned_data['description']
            profile_pic = req.FILES['profile_pic']
            group = Group(name=name, description=description, profile_pic=profile_pic, admin=user.student)
            group.save()
            members = cleaned_data['members']
            if members.count() > 0:
                group.members.add(user.student, *members)
            else:
                group.members.add(user.student)

            return redirect('home', student_username=user.username)
    return redirect('home', student_username=user.username)


def edit_group(req, group_id):

    if req.method == "POST":
        form = GroupForm(req.POST, req.FILES)
        if form.is_valid():
            group = Group.objects.get(pk=group_id)
            group.name = form.cleaned_data['name']
            group.description = form.cleaned_data['description']
            group.profile_pic = form.cleaned_data['profile_pic']
            group.members.add(req.user.student, *form.cleaned_data['members'])
            group.save()
            return redirect('home', student_username=group.admin.user.username)

    group = Group.objects.get(pk=group_id)
    edit_group_form = GroupForm(instance=group)
    context = {"form": edit_group_form, "group": group}
    return render(req, 'mines_book/group_form.html', context)


def search(req, search_param):
    students = User.objects.filter(username__contains=search_param)
    groups = Group.objects.filter(name__contains=search_param)
    d = {
        "results": {
            "category1": {
                "name": "Students",
                "results": serialize_students(students)
            },
            "category2": {
                "name": "Groups",
                "results": serialize_groups(groups)
            }
        },

    }
    return HttpResponse(json.dumps(d), content_type='application/json')


def get_students_usernames(req, search_param):
    students = User.objects.filter(username__startswith=search_param).exclude(username=req.user.username)
    serialize_students_select(students)
    r = {
        "success": "true",
        "results": serialize_students_select(students)
    }
    return HttpResponse(json.dumps(r), content_type='application/json')


def get_students_not_in_group(req, group_id, search_param):
    students_not_in = Group.objects.get(pk=group_id).members.all()
    students = User.objects.filter(username__startswith=search_param).exclude(student__in=students_not_in)
    serialize_students_select(students)
    r = {
        "success": "true",
        "results": serialize_students_select(students)
    }
    return HttpResponse(json.dumps(r), content_type='application/json')

def new_post_to_student(req, student_username):
    user = req.user
    if req.method == 'POST':
        form = PostForm(req.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            content = cleaned_data['content']
            post = Post(content=content, author=user.student)
            post.save()
            recipient = User.objects.filter(username=student_username)[0]
            post_to_student = PostToStudent(post=post, recipient=recipient.student)
            post_to_student.save()

            context = {'post':post_to_student}
            return render(req, 'mines_book/post_card.html', context)
    return redirect('home', student_username=user.username)