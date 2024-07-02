from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class Demo(models.Model):
    id = models.AutoField(primary_key=True)
    name =models.CharField(max_length=15)
    
    

################  creating a custom user model instead of using default provided by django ################

class CustomUserManager(UserManager):
    ## method is a private method intended for internal use within the user manager class. It directly creates and saves a user instance to the database.
    def _create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError("Email couldn't fetched !!")
        email =  self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    ## method is a public method that provides an interface for creating a regular user. It sets default values and then calls the _create_user method to perform the actual creation and saving of the user instance.
    def create_user(self, email=None,password=None,**extra_fields):
        extra_fields.setdefault('is_superuser', False )
        extra_fields.setdefault('is_staff', False )
        return self._create_user(email=email,password=password,**extra_fields)

    def create_superuser(self,email=None,password=None,**extra_fields):
        extra_fields.setdefault('is_superuser', True )
        extra_fields.setdefault('is_staff', True )
        return self._create_user(email=email,password=password,**extra_fields)


class User(AbstractBaseUser,PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=30,unique=True)
    password = models.CharField(max_length=255)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    img = models.CharField(max_length=255 , null=True)
    phone = models.CharField(
        max_length=10,
        validators=[MinLengthValidator(10), MaxLengthValidator(10)],
        unique=True
    )
    address = models.ForeignKey('FullAddress' , on_delete=models.CASCADE,blank=True , null=True , related_name="user_fullAddress")
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'




class FullAddress(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="FullAddress")
    state = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30 , null=True)
    area = models.CharField(max_length=40)
    landmark = models.CharField(max_length=40 , null=True)
    residency = models.CharField(max_length=30)
    house_no = models.CharField(max_length=10)
    pincode =models.CharField(max_length=8)
    
    def __str__(self):
        return f"{self.house_no}, {self.residency}, {self.area}, {self.city}, {self.state}"
    
    class Meta:
        verbose_name = 'FullAddress'
        verbose_name_plural = 'FullAddresses'
