"""mines_book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login[/]', views.login, name="login"),
    url(r'^logout[/]', views.logout),

    url(r'^$', views.index, name="index"),

    # Search routes for json APIs
    url(r'^search/(?P<search_param>\w|.+)[/]$', views.search),

    url(r'^search_students_usernames[/]$', views.get_students_usernames),
    url(r'^search_students_usernames/(?P<search_param>\w|.+)[/]$', views.get_students_usernames),

    url(r'^search_students_not_in_group/(?P<group_id>[0-9]+)[/]$', views.get_students_not_in_group),
    url(r'^search_students_not_in_group/(?P<group_id>[0-9]+)/(?P<search_param>\w|.+)[/]$', views.get_students_not_in_group),

    url(r'^search_students_in_group/(?P<group_id>[0-9]+)[/]$', views.get_students_in_group),
    url(r'^search_students_in_group/(?P<group_id>[0-9]+)/(?P<search_param>\w|.+)[/]$', views.get_students_in_group),

    # Routes for user actions
    url(r'^students/(?P<student_username>\w|.+)/friend[/]$', views.friend_view, name="friend_view"),
    url(r'^students/(?P<student_username>\w|.+)/feed[/]$', views.user_feed, name="user_feed"),
    url(r'^students/(?P<student_username>\w|.+)/friends[/]$', views.user_friends, name="user_feed"),
    url(r'^students/(?P<student_username>\w|.+)/joined_groups[/]$', views.user_joined_groups, name="user_joined_groups"),
    url(r'^students/(?P<student_username>\w|.+)/followed_groups[/]$', views.user_followed_groups, name="user_followed_groups"),
    url(r'^students/(?P<student_username>\w|.+)/new_post[/]$', views.new_post_to_student, name="new_post_to_student"),
    url(r'^students/(?P<student_username>\w|.+)[/]$', views.student_view, name="student_view"),
    url(r'^students[/]$', views.students_view, name="students_view"),

    # Routes for comments and posts
    url(r'^new_comment/(?P<post_id>[0-9]+)[/]$', views.new_comment, name="new_comment"),
    url(r'^delete_post[/]$', views.delete_post, name="delete_post"),
    url(r'^delete_comment[/]$', views.delete_comment, name="delete_comment"),
    url(r'^edit_post/(?P<post_id>[0-9]+)[/]$', views.edit_post, name="edit_post"),
    url(r'^edit_comment/(?P<comment_id>[0-9]+)[/]$', views.edit_comment, name="edit_comment"),

    # Routes for group actions
    url(r'^groups/create[/]$', views.create_group, name="create_group"),
    url(r'^groups/(?P<group_id>\w|.+)/followers[/]$', views.group_followers, name="group_followers"),
    url(r'^groups/(?P<group_id>\w|.+)/members[/]$', views.group_members, name="group_members"),
    url(r'^groups/(?P<group_id>\w|.+)/new_post[/]$', views.new_post_to_group, name="new_post_to_group"),
    url(r'^groups/(?P<group_id>\w|.+)/edit[/]$', views.edit_group, name="edit_group"),
    url(r'^groups/(?P<group_id>\w|.+)/feed[/]$', views.group_feed, name="group_feed"),
    url(r'^groups/(?P<group_id>\w|.+)/follow[/]$', views.follow_view, name="follow_view"),
    url(r'^groups/(?P<group_id>\w|.+)/leave[/]$', views.leave_group, name="leave_group"),
    url(r'^groups/(?P<group_id>\w|.+)[/]$', views.group_view, name="group_view"),
    url(r'^groups[/]$', views.get_all_groups, name="all_groups"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
