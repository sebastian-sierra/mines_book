from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """ - students are the users of the application
        - the fields correspond to useful information about EMN students
    """
    user = models.OneToOneField(User)
    profile_pic = models.ImageField(upload_to="students_profile_pics", null=True)
    prom = models.CharField(max_length=4)
    city = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=20, null=True)
    friends = models.ManyToManyField('self')
    OPTION_CHOICES = (
        ('GSI', 'GSI'),
        ('OMTI', 'OMTI'),
        ('GIPAD', 'GIPAD'),
        ('QSF', 'QSF'),
        ('GOPL', 'GOPL'),
        ('AII', 'AII'),
        ('NSTE', 'NSTE'),
        ('STAR', 'STAR'),
        ('GSE', 'GSE'),
        ('GE', 'GE'),
    )
    option = models.CharField(max_length=6, choices=OPTION_CHOICES)

    def __unicode__(self):
        return u'%s' % self.user.username


class Group(models.Model):
    """ groups of students as there are for example the BDE, BDA etc. at EMN
    """
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=500)
    admin = models.ForeignKey('Student', related_name="managed_groups")
    members = models.ManyToManyField('Student', related_name='groups_joined')
    followers = models.ManyToManyField('Student', related_name='groups_followed')
    profile_pic = models.ImageField(upload_to="groups_profile_pics", null=True)


class Post(models.Model):
    """ a post
    """
    content = models.CharField(max_length=500)
    author = models.ForeignKey('Student', related_name="posts_authored")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class PostToStudent(models.Model):
    """ a post to a student's wall
    """
    post = models.OneToOneField('Post')
    recipient = models.ForeignKey('Student', related_name="posts_received")


class PostToGroup(models.Model):
    """ a post to a group's wall
    """
    post = models.OneToOneField('Post')
    recipient = models.ForeignKey('Group', related_name="posts_received")


class Comment(models.Model):
    """ a comment to a post
    """
    content = models.CharField(max_length=200)
    author = models.ForeignKey('Student', related_name="comments_authored")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    post = models.ForeignKey('Post', related_name="comments")






