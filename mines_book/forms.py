from django.forms import ModelForm, Textarea, ModelMultipleChoiceField, CharField, PasswordInput
from mines_book.models import Group, Student, Post, Comment


class StudentForm(ModelForm):
    username = CharField(max_length=30)
    first_name = CharField(max_length=30)
    last_name = CharField(max_length=30)
    password = CharField(max_length=30, widget=PasswordInput(render_value=True), required=False)
    confirm_password = CharField(max_length=30, widget=PasswordInput(render_value=True), required=False)

    class Meta:
        model = Student
        exclude = ['user', 'friends']


class GroupForm(ModelForm):
    members = ModelMultipleChoiceField(queryset=Student.objects.all(), required=False)
    deleted_members = ModelMultipleChoiceField(queryset=Student.objects.all(), required=False)

    class Meta:
        model = Group
        fields = ["name", "description", "profile_pic", "members", "id"]
        widgets = {
            'description': Textarea(attrs={'rows': 4})
        }


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ["content"]


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]