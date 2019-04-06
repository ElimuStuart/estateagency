from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from tinymce import HTMLField


User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    content = HTMLField('Content')
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={
            'id': self.id
        })

    def get_update_url(self):
        return reverse('post_update', kwargs={
            'id': self.id
        })

    def get_delete_url(self):
        return reverse('post_delete', kwargs={
            'id': self.id
        })

    @property
    def get_comments(self):
        return self.comments.all()

    
class Comment(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
