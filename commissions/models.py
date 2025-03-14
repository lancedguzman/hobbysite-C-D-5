from django.db import models
from django.urls import reverse


class Commission(models.Model):
    """
    Represents a Commission object.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    people_required = models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    # Sort commissions by creation date in ascending order
    class Meta:
        ordering = ['created_on']  


    def __str__(self):
        return self.title
    

    def link(self):
        return reverse("commissions:commission", args=[str(self.id)])


class Comment(models.Model):
    """
    Represents a Comment object linked to a Commission.
    """
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    entry = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    # Sort commissions by creation date in descending order
    class Meta:
        ordering = ['-created_on'] 