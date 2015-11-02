# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=200)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=500)),
                ('profile_pic', models.ImageField(null=True, upload_to=b'groups_profile_pics')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=500)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PostToGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', models.OneToOneField(to='mines_book.Post')),
                ('recipient', models.ForeignKey(related_name='posts_received', to='mines_book.Group')),
            ],
        ),
        migrations.CreateModel(
            name='PostToStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', models.OneToOneField(to='mines_book.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('option', models.CharField(max_length=6)),
                ('profile_pic', models.ImageField(null=True, upload_to=b'students_profile_pics')),
                ('prom', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=20, null=True)),
                ('country', models.CharField(max_length=20, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='posttostudent',
            name='recipient',
            field=models.ForeignKey(related_name='posts_received', to='mines_book.Student'),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(related_name='posts_authored', to='mines_book.Student'),
        ),
        migrations.AddField(
            model_name='group',
            name='admin',
            field=models.ForeignKey(related_name='managed_groups', to='mines_book.Student'),
        ),
        migrations.AddField(
            model_name='group',
            name='followers',
            field=models.ManyToManyField(related_name='groups_followed', to='mines_book.Student'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(related_name='groups_joined', to='mines_book.Student'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(related_name='comments_authored', to='mines_book.Student'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(related_name='comments', to='mines_book.Post'),
        ),
    ]
