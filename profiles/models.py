from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.CharField(max_length = 265, blank = True)
    city = models.CharField(max_length = 265, blank = True)
    avatar = models.ImageField(null = True, blank =True)

    def __str__(self):
        return self.user.username


class ProfileStatus(models.Model):
    user_profile = models.ForeignKey(Profile, on_delete = models.CASCADE)
    status_content = models.CharField(max_length = 265)
    status_image = models.ImageField(null = True, blank =True)
    created_at = models.DateTimeField(auto_now_add =True)
    updated_at = models.DateTimeField(auto_now =True)

    class Meta:
        verbose_name_plural = "Statuses"

    def __str__(self):
        return str(self.user_profile)
