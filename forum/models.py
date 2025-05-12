from django.db import models
from user_management.models import Profile

# Create your models here.
class ThreadCategory(models.Model):
    name = models.CharField(max_length=255, default="")
    description = models.TextField()
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Thread(models.Model):
    title = models.CharField(max_length=255, default="")
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='thread_author')
    category = models.ForeignKey(ThreadCategory, on_delete=models.SET_NULL, null=True, related_name="category")
    entry = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"{self.title} by {self.author}"

class Comment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, related_name='comment_author')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="thread")
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"{self.author} commented on {self.thread.title}"