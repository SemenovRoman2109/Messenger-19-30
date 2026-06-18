from django.db import models
from user_app.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete= models.CASCADE )
    birth_date = models.DateField(null= True, blank= True)
    pseudonym = models.CharField(max_length= 50, null= True, blank= True)
    avatar = models.ImageField(null=True, blank=True, upload_to= 'profile_app/avatars')
    signature = models.ImageField(null=True, blank=True, upload_to= 'profile_app/signatures')
    is_image_signature = models.BooleanField(default=False)
    is_text_signature = models.BooleanField(default=False)
    
    def __str__(self):
        return f'profile: {self.user.email}'
        