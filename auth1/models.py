from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

BLOOD_GROUPS = [
	('A+', 'A+'),
	('A-', 'A-'),
	('B+', 'B+'),
	('B-', 'B-'),
	('AB+', 'AB+'),
	('AB-', 'AB-'),
	('O+', 'O+'),
	('O-', 'O-'),
]

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user



class RegisterUser(AbstractBaseUser):
	username				= models.CharField(max_length=50, unique=True)
	name					= models.CharField(max_length=100)
	email					= models.EmailField(max_length=100, unique=True)
	# password1				= models.CharField(max_length=50) #To hide them from
	# password2				= models.CharField(max_length=50) #admin pannel
	contact_number			= models.CharField(max_length=15)
	address					= models.CharField(max_length=250, null=True, blank=True)
	date_of_birth			= models.DateField(null=True, blank=True) #Fix
	nid						= models.CharField(max_length=13, null=True, blank=True)
	blood_group				= models.CharField(max_length=8, choices=BLOOD_GROUPS, null=True, blank=True)
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)
	last_donated			= models.DateField(verbose_name='last_donated', auto_now_add=False, null=True, blank=True)
	donation_count			= models.IntegerField(default=0)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'password']

	objects = MyAccountManager()

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

	def __str__(self):
		return self.username


class Notification(models.Model):
	message = models.CharField(max_length=255)
	receiver = models.ManyToManyField(RegisterUser, related_name='receiver')
	read_by = models.ManyToManyField(RegisterUser, related_name='read_by', blank=True, null=True)
	context = models.IntegerField(null=True)
	creation_date = models.DateTimeField(default=timezone.now)
	



# class ReadFlag(model.Model):
# 	user = models.ManyToManyField(RegisterUser, on_delete=models.CASCADE)
# 	read_status = models.BooleanField(default=False)



