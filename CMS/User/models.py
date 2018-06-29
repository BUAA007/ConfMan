from django.db import models
from Meeting.models import *

# Create your models here.
class User(models.Model):
	username = models.CharField(
		max_length = 32,
		unique = True,
		)
	password = models.CharField(
		max_length = 32,
		)
	email = models.CharField(
		max_length = 32,
		)
	tel = models.CharField(
		max_length = 20,
		)
	favorite = models.ManyToManyField(Meeting)
	participate = models.ManyToManyField(Meeting)