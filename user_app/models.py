from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser): 
    email = models.EmailField(unique=True)
    username = models.CharField(
        max_length = 150,
        unique = False,
        blank = True,
        null = True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Friendship(models.Model):
    from_user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'send_friendship')
    to_user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'received_friendship')
    created_at = models.DateTimeField(auto_now_add= True)
    status = models.CharField(max_length= 15, default= 'pending')
    
    class Meta:
        unique_together = ('from_user', 'to_user')

# unique_together в класі Meta моделі, допомагає вказати пара яких полів не може повторюватись разом