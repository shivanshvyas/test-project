from django.db import models
from django.contrib.auth.models import AbstractUser

STATUS = ((0, "Pending"), (1, "Approve"), (2, "Rejected"), (3, "Block"))
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class Products(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200,blank=False, default='')
    published = models.BooleanField(default=False)

class class_name(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    class Meta:
    	managed = True
    	db_table = 'tbl_class'
    def __str__(self):
    	if self.name:
    		return "{} ({})".format(self.name, self.id)
   
class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password, **extra_fields):
        
        
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
	class_name = models.ForeignKey(class_name, on_delete=models.CASCADE, related_name="addresses",null=True,blank=True)
	first_name = models.CharField(max_length=50, null=True, blank=True)
	# username = None
	# USERNAME_FIELD = 'email'
	# REQUIRED_FIELDS = []
	username = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	email = models.CharField(max_length=100, null=True, blank=True,unique=True)
	email_verifY = models.BooleanField(default=False)
	date_of_birth = models.CharField(max_length=100, null=True, blank=True)
	image = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
	status = models.PositiveIntegerField(default=0, choices=STATUS)
	# objects = CustomUserManager()

	class Meta:
		managed = True
		db_table = 'tbl_user'
	def __str__(self):
		if self.email:
			return "{} ({})".format(self.email, self.id)