from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Creates the Profile Model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=63)
    email_address = models.EmailField()

    def __str__(self):
        return self.display_name
