from django import forms
from django.forms import ModelForm, Textarea
from .models import Post, Comment, Profile

class PositionForm(forms.Form):
    position = forms.CharField()

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'email', 'twitter']