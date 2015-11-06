from django.forms import ModelForm, Textarea, ModelMultipleChoiceField
from mines_book.models import Group, Student, Post, Comment


class GroupForm(ModelForm):
    members = ModelMultipleChoiceField(queryset=Student.objects.all(), required=False)

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