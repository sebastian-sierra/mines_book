from django.http import HttpResponse, QueryDict, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from forms import GroupForm, PostForm, CommentForm, StudentForm
from models import Group, Post, PostToStudent, Student, Comment, PostToGroup
from utils import make_search_dict, make_dropdown_dict
import json
from django.contrib.auth.decorators import login_required


def index(req):
    if req.user.is_authenticated():
        return redirect('student_view', student_username=req.user.username)
    else:
        return redirect('/login/')


def login(req):
    if req.user.is_authenticated():
        return redirect('student_view', student_username=req.user.username)

    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password_login']
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(req, user)
            return redirect('student_view', student_username=username)

    student_form = StudentForm()
    return render(req, 'mines_book/login.html', context={"form": student_form})


@login_required
def logout(req):
    auth_logout(req)
    student_form = StudentForm()
    return render(req, 'mines_book/login.html', context={"form": student_form})


@login_required
def student_view(req, student_username):
    try:
        user = User.objects.filter(username=student_username)[0]
    except:
        raise Http404("The user does not exist")
    new_post_form = PostForm()
    edit_student_form = StudentForm(initial={"first_name": user.first_name, "last_name": user.last_name},
                                    instance=user.student)
    context = {"user": user, "posts": user.student.posts_received.all().order_by('-post__date_created'),
               "post_form": new_post_form, "student_form": edit_student_form}
    return render(req, 'mines_book/user.html', context)


def students_view(req):
    if req.method == "POST":
        if not req.user.is_authenticated():
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
                student = Student.objects.create(user=user, option=option, prom=prom, profile_pic=profile_pic,
                                                 city=city,
                                                 country=country)
                user.save()
                student.save()
                user = authenticate(username=username, password=password)
                auth_login(req, user)

        if req.user.is_authenticated():
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
                password = form.cleaned_data['password']
                if password != "" and password == form.cleaned_data['confirm_password']:
                    req.user.set_password(form.cleaned_data['password'])
                    req.user.save()
                    user = authenticate(username=student.user.username, password=password)
                    auth_login(req, user)
                student.save()
                student.user.save()

        return redirect('student_view', student_username=student.user.username)

    if req.method == "DELETE":
        req.user.delete()
        return redirect('login')

    if not req.user.is_authenticated():
        return redirect('login')

    students = Student.objects.all()
    return render(req, "mines_book/all_students.html", {"students": students})


@login_required
def friend_view(req, student_username):
    if req.method == "PUT":
        friend = User.objects.get(username=student_username).student
        req.user.student.friends.add(friend)
    elif req.method == "DELETE":
        friend = User.objects.get(username=student_username).student
        req.user.student.friends.remove(friend)
    return redirect('student_view', student_username=friend.user.username)


@login_required
def get_all_groups(req):
    groups = Group.objects.all()
    return render(req, "mines_book/all_groups.html", {"groups": groups})


@login_required
def user_feed(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    new_post_form = PostForm()
    context = {"user": user, "posts": user.student.posts_received.all().order_by('-post__date_created'),
               "post_form": new_post_form, "recipient_type": "student"}
    return render(req, 'mines_book/feed.html', context)


@login_required
def user_friends(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    context = {"students": user.student.friends.all()}
    return render(req, 'mines_book/student_cards.html', context)


@login_required
def user_joined_groups(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    new_group_form = GroupForm()
    context = {"groups": user.student.groups_joined.all(), "form": new_group_form, "student": user, "action": "create"}
    return render(req, 'mines_book/group_cards.html', context)


@login_required
def user_followed_groups(req, student_username):
    user = User.objects.filter(username=student_username)[0]
    new_group_form = GroupForm()
    context = {"groups": user.student.groups_followed.all(), "form": new_group_form, "student": user,
               "action": "create"}
    return render(req, 'mines_book/group_cards.html', context)


@login_required
def group_view(req, group_id):
    try:
        group = Group.objects.get(pk=group_id)
    except:
        raise Http404("The group does not exist")
    if req.method == "GET":
        group_form = GroupForm(instance=group)
        post_form = PostForm(instance=group)
        posts = group.posts_received.order_by("-post__date_created")
        return render(req, 'mines_book/group.html',
                      context={"group": group, "group_form": group_form, "post_form": post_form, "posts": posts})

    if req.method == "DELETE":
        group.delete()
        response_data = {'msg': 'Group was deleted.'}
        return HttpResponse(json.dumps(response_data), content_type='application/json')


@login_required
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
            return redirect('group_view', group_id=group.id)

    return redirect('student_view', student_username=user.username)


@login_required
def edit_group(req, group_id):
    group = Group.objects.get(pk=group_id)
    if req.user == group.admin.user:
        if req.method == "POST":
            form = GroupForm(req.POST, req.FILES, instance=group)
            if form.is_valid():
                group.name = form.cleaned_data['name']
                group.description = form.cleaned_data['description']
                group.profile_pic = form.cleaned_data['profile_pic']
                group.members.add(req.user.student, *form.cleaned_data['members'])
                group.members.remove(*form.cleaned_data['deleted_members'])
                group.save()
                return redirect('group_view', group_id=group.id)

        group = Group.objects.get(pk=group_id)
        edit_group_form = GroupForm(instance=group)
        context = {"form": edit_group_form, "group": group, "action": "edit"}
        return render(req, 'mines_book/group_form.html', context)
    raise Exception("Please don't try to hack the application.")


@login_required
def group_feed(req, group_id):
    posts = Group.objects.get(pk=group_id).posts_received.order_by("-post__date_created")
    new_post_form = PostForm()
    context = {"posts": posts,
               "post_form": new_post_form, "recipient_type": "group"}
    return render(req, 'mines_book/feed.html', context)


@login_required
def group_members(req, group_id):
    members = Group.objects.get(pk=group_id).members.all()
    context = {"students": members}
    return render(req, 'mines_book/student_cards.html', context)


@login_required
def group_followers(req, group_id):
    followers = Group.objects.get(pk=group_id).followers.all()
    context = {"students": followers}
    return render(req, 'mines_book/student_cards.html', context)


@login_required
def follow_view(req, group_id):
    group = Group.objects.get(pk=group_id)
    if req.method == "PUT":
        group.followers.add(req.user.student)
        msg = {"status": "success"}
    elif req.method == "DELETE":
        group.followers.remove(req.user.student)
        msg = {"status": "success"}
    return HttpResponse(json.dumps(msg), content_type='application/json')


@login_required
def new_post_to_group(req, group_id):
    user = req.user
    if req.method == 'POST':
        form = PostForm(req.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            content = cleaned_data['content']
            post = Post(content=content, author=user.student)
            post.save()
            recipient = Group.objects.get(pk=group_id)
            post_to_group = PostToGroup(post=post, recipient=recipient)
            post_to_group.save()

            context = {'post': post_to_group}
            return render(req, 'mines_book/post_card.html', context)
    raise Exception("The form is not valid.")


@login_required
def search(req, search_param):
    students = User.objects.filter(username__contains=search_param)
    groups = Group.objects.filter(name__contains=search_param)
    search_dict = make_search_dict(students, groups)
    return HttpResponse(json.dumps(search_dict), content_type='application/json')


@login_required
def get_students_usernames(req, search_param=None):
    students = User.objects.exclude(username=req.user.username)
    if search_param is not None:
        students = students.filter(username__startswith=search_param)
    r = make_dropdown_dict(students)
    return HttpResponse(json.dumps(r), content_type='application/json')


@login_required
def get_students_in_group(req, group_id, search_param=None):
    students_in = Group.objects.get(pk=group_id).members.all().exclude(user__username=req.user.username)
    users_in = User.objects.filter(student__in=students_in)
    if search_param is not None:
        users_in = users_in.filter(username__startswith=search_param)
    r = make_dropdown_dict(users_in)
    return HttpResponse(json.dumps(r), content_type='application/json')


@login_required
def get_students_not_in_group(req, group_id, search_param=None):
    students_in = Group.objects.get(pk=group_id).members.all()
    students_not_in = User.objects.exclude(student__in=students_in)
    if search_param is not None:
        students_not_in.filter(username__startswith=search_param)
    r = make_dropdown_dict(students_not_in)
    return HttpResponse(json.dumps(r), content_type='application/json')


@login_required
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
    raise Exception("The form is not valid.")


@login_required
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
    raise Exception("The form is not valid.")


@login_required
def delete_post(req):
    post = Post.objects.get(pk=int(QueryDict(req.body).get('postpk')))
    if req.user == post.author.user:
        if req.method == 'DELETE':
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
    raise Exception("Please don't try to hack the application.")


@login_required
def delete_comment(req):
    comment = Comment.objects.get(pk=int(QueryDict(req.body).get('commentpk')))
    if req.user == comment.author.user:
        if req.method == 'DELETE':
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
    raise Exception("Please don't try to hack the application.")


@login_required
def edit_post(req, post_id):
    post = Post.objects.get(pk=post_id)
    if req.user == post.author.user:
        if req.method == 'PUT':
            new_content = QueryDict(req.body).get('content')
            post.content = new_content
            post.save()
            msg = {'content': post.content}
            return HttpResponse(json.dumps(msg), content_type='application/json')
    raise Exception("Please don't try to hack the application.")


@login_required
def edit_comment(req, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if req.user == comment.author.user:
        if req.method == 'PUT':
            new_content = QueryDict(req.body).get('content')
            comment.content = new_content
            comment.save()
            msg = {'content': comment.content}
            return HttpResponse(json.dumps(msg), content_type='application/json')
    raise Exception("Please don't try to hack the application.")
