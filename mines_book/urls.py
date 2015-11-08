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
    url(r'^login[/]', views.login),
    url(r'^logout[/]', views.logout),
    url(r'^search/(?P<search_param>\w|.+)[/]$', views.search),
    url(r'^search_students_usernames/(?P<search_param>\w|.+)[/]$', views.get_students_usernames),
    url(r'^search_students_not_in_group/(?P<group_id>[0-9]+)/(?P<search_param>\w|.+)[/]$', views.get_students_not_in_group),
    url(r'^students/(?P<student_username>\w|.+)/feed[/]$', views.user_feed, name="user_feed"),
    url(r'^students/(?P<student_username>\w|.+)/friends[/]$', views.user_friends, name="user_feed"),
    url(r'^students/(?P<student_username>\w|.+)/joined_groups[/]$', views.user_joined_groups, name="user_joined_groups"),
    url(r'^students/(?P<student_username>\w|.+)/new_post[/]$', views.new_post_to_student, name="new_post_to_student"),
    url(r'^students/edit[/]$', views.edit_student, name="edit_student"),
    url(r'^students/create[/]$', views.create_student, name="edit_student"),
    url(r'^students/(?P<student_username>\w|.+)[/]$', views.home, name="home"),
    url(r'^students[/]$', views.get_all_students, name="all_students"),
    url(r'^new_comment/(?P<post_id>[0-9]+)[/]$', views.new_comment, name="new_comment"),
    url(r'^groups/create[/]$', views.create_group, name="create_group"),
    url(r'^groups/(?P<group_id>\w|.+)/edit[/]$', views.edit_group, name="edit_group"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
