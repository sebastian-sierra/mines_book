from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User)
    option = models.CharField(max_length=6)
    profile_pic = models.ImageField(upload_to="students_profile_pics", null=True)
    prom = models.CharField(max_length=5)
    city = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=20, null=True)
    friends = models.ManyToManyField('self')

    def __unicode__(self):
        return u'%s' % self.user.username


class Group(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    admin = models.ForeignKey('Student', related_name="managed_groups")
    members = models.ManyToManyField('Student', related_name='groups_joined')
    followers = models.ManyToManyField('Student', related_name='groups_followed')
    profile_pic = models.ImageField(upload_to="groups_profile_pics", null=True)


class Post(models.Model):
    content = models.CharField(max_length=500)
    author = models.ForeignKey('Student', related_name="posts_authored")
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class PostToStudent(models.Model):
    post = models.OneToOneField('Post')
    recipient = models.ForeignKey('Student', related_name="posts_received")


class PostToGroup(models.Model):
    post = models.OneToOneField('Post')
    recipient = models.ForeignKey('Group', related_name="posts_received")


class Comment(models.Model):
    content = models.CharField(max_length=200)
    author = models.ForeignKey('Student', related_name="comments_authored")
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    post = models.ForeignKey('Post', related_name="comments")






