from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    class Meta:
        abstract = True
        model = Post
        fields = ('group', 'text')
