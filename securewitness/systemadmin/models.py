from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
     
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    is_admin = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
#    def get_or_create_user_profile(user):
 #       profile = None
 #       try:
 #           profile = user.userprofile
 ##       except UserProfile.DoesNotExist:
  #          profile = UserProfile.objects.create()
  #      return profile

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])