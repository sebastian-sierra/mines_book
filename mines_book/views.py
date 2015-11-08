from django.core import serializers
from django.core.urlresolvers import reverse
from django.db.models import ImageField
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, QueryDict
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from forms import GroupForm, PostForm, CommentForm, StudentForm
from models import Group, Post, PostToStudent, Student, Comment
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

    student_form = StudentForm()
    return render(req, 'mines_book/login.html', context={"form": student_form})


def logout(req):
    auth_logout(req)
    return render(req, 'mines_book/login.html')


def home(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    new_post_form = PostForm()
    edit_student_form = StudentForm(initial={"first_name": user.first_name, "last_name": user.last_name,
                                             "password": "Not Changed", "confirm_password": "Not Changed2"},
                                    instance=user.student)
    context = {"user": user, "posts": user.student.posts_received.all().order_by('-post__date_created'),
               "post_form": new_post_form, "student_form": edit_student_form}
    return render(req, 'mines_book/user.html', context)


def create_student(req):
    if req.method == "POST":
        form = StudentForm(req.POST, req.FILES)
        password = req.POST['password']
        if form.is_valid() and password == form.cleaned_data['confirm_password']:
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            user = User.objects.create(username=username, first_name=first_name, last_name=last_name)
            user.set_password(password)
            option = form.cleaned_data['option']
            prom = form.cleaned_data['prom']
            profile_pic = form.cleaned_data['profile_pic']
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            student = Student.objects.create(user=user, option=option, prom=prom, profile_pic=profile_pic, city=city,
                                             country=country)
            user.save()
            student.save()
            user = authenticate(username=username, password=password)
            auth_login(req, user)

            return redirect('home', student_username=user.username)

    return redirect('login')


def edit_student(req):
    if req.method == "POST":
        form = StudentForm(req.POST, req.FILES, instance=req.user.student)
        if form.is_valid():
            student = req.user.student
            student.user.first_name = form.cleaned_data['first_name']
            student.user.last_name = form.cleaned_data['last_name']
            student.option = form.cleaned_data['option']
            student.prom = form.cleaned_data['prom']
            student.profile_pic = form.cleaned_data['profile_pic']
            student.city = form.cleaned_data['city']
            student.country = form.cleaned_data['country']
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                student.user.set_password(form.cleaned_data['password'])
            student.save()
            student.user.save()

    return redirect('home', student_username=req.user.username)


def delete_student(req):
    user = req.user
    user.delete()
    return redirect('login')


def get_all_students(req):
    students = Student.objects.all()
    return render(req, "mines_book/all_students.html", {"students": students})


def user_feed(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    new_post_form = PostForm()
    context = {"user": user, "posts": user.student.posts_received.all().order_by('-post__date_created'),
               "post_form": new_post_form}
    return render(req, 'mines_book/user_feed.html', context)


def user_friends(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    context = {"students": user.student.friends.all()}
    return render(req, 'mines_book/student_cards.html', context)


def user_joined_groups(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    new_group_form = GroupForm()
    context = {"groups": user.student.groups_joined.all(), "form": new_group_form, "student": user, "action": "create"}
    return render(req, 'mines_book/group_cards.html', context)


def create_group(req):
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
    group = Group.objects.get(pk=group_id)
    if req.method == "POST":
        form = GroupForm(req.POST, req.FILES, instance=group)
        if form.is_valid():
            group.name = form.cleaned_data['name']
            group.description = form.cleaned_data['description']
            group.profile_pic = form.cleaned_data['profile_pic']
            group.members.add(req.user.student, *form.cleaned_data['members'])
            group.save()
            return redirect('home', student_username=group.admin.user.username)

    group = Group.objects.get(pk=group_id)
    edit_group_form = GroupForm(instance=group)
    context = {"form": edit_group_form, "group": group, "action": "edit"}
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

            context = {'post': post_to_student}
            return render(req, 'mines_book/post_card.html', context)
    return redirect('home', student_username=user.username)


def new_comment(req, post_id):
    user = req.user
    if req.method == 'POST':
        post = Post.objects.get(pk=post_id)
        comment_id = "id_comment_%s_for_" + post_id
        form = CommentForm(req.POST, auto_id=comment_id)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            content = cleaned_data['content']

            comment = Comment(content=content, post=post, author=user.student)
            comment.save()

            context = {"comment": comment}
            return render(req, 'mines_book/comments.html', context)
    return redirect('home', student_username=user.username)


def delete_post(req):
    if req.method == 'DELETE':

        post = Post.objects.get(pk=int(QueryDict(req.body).get('postpk')))
        post.delete()

        response_data = {'msg': 'Post was deleted.'}

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


def delete_comment(req):
    if req.method == 'DELETE':

        comment = Comment.objects.get(pk=int(QueryDict(req.body).get('commentpk')))
        comment.delete()

        response_data = {'msg': 'Comment was deleted.'}

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )