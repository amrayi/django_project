from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    is_auther = models.BooleanField(default= False, verbose_name='وضعیت نویسندگی')
    special_user = models.DateTimeField(default= timezone.now, verbose_name='کاربر ویژه تا')
    email = models.EmailField(unique= True, verbose_name='ایمیل')
    phone_number = models.CharField(max_length=11, verbose_name='شماره تلفن')
        
    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False
    
    is_special_user.boolean = True
    is_special_user.short_description = 'وضعیت کاربر ویژه'
    
class VerificationCode(models.Model):
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)