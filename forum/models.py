from django.db import models

# Create your models here.
class post_category(models.Model):
    name = models.CharField(max_length=255, default="")
    description = models.TextField()
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class post(models.Model):
    title = models.CharField(max_length=255, default="")
    category = models.ForeignKey(post_category, on_delete=models.SET_NULL, null=True, related_name="category")
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)#only gets set when the model is created
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
