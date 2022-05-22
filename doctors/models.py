from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import UserManager

# Create your models here.
class Doctor(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15,null=True)
    birthdate = models.DateField(null=True,blank=True)
    GENDER_OPTIONS = (('Male','Male'),('Female','Female'),('Other','Other'))
    gender = models.CharField(max_length=6,choices=GENDER_OPTIONS,null=True)
    location = models.TextField(null=True)
    spoken_languages = models.ManyToManyField("SpokenLanguage")
    diplomas = ArrayField(models.CharField(max_length=50,null=True,blank=True),null=True,blank=True)
    picture = models.ImageField(upload_to="doctor_pictures/",null=True,blank=True)


    REQUIRED_FIELDS = ['phone','gender','birthdate','diplomas','email']


class SpokenLanguage(models.Model):
    language = models.CharField(max_length=20)

    def __str__(self):
        return self.language



class Patient(models.Model):
    doctor = models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
    