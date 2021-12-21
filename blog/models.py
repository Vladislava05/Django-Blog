from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

Reviews = 'Reviews'
News = 'News'
Articles = 'Articles'

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    body = RichTextField(blank=True, null=True)
    
    date = models.DateTimeField(auto_now_add=True)
    
    CATEGORY = [
        (Reviews, 'Reviews'),
        (News, 'News'),
        (Articles, 'Articles')
    ]
    category = models.CharField(
        max_length=10,
        choices = CATEGORY,
        default = 'IT'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')

    class Meta:
        ordering = ['-date']

class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments",
        on_delete=models.CASCADE, 
    )
    name = models.CharField(max_length=200)
    body = models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)
    
    
    

class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')