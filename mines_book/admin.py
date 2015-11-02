from django.contrib import admin

from .models import Student, Group, Post, PostToStudent, Comment

admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Post)
admin.site.register(PostToStudent)
admin.site.register(Comment)
