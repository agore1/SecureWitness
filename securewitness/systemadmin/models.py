from django.db import models
from django.contrib.auth.models import User
     
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    is_admin = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])