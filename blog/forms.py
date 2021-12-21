from django import forms
from django.forms import ModelForm, Textarea
from .models import Post, Comment

class PositionForm(forms.Form):
    position = forms.CharField()

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body']
       