from django.db import models
from datetime import date
from django.conf import settings
# Create your models here.
class UserData(models.Model):
	User_Date=models.CharField(max_length=15, default=date.today())
	User_ID=models.CharField(max_length=50, primary_key=True)
	User_Name=models.CharField(max_length=50, default='None')
	User_Email=models.CharField(max_length=50)
	User_Phone=models.CharField(max_length=14, default='None')
	User_Password=models.CharField(max_length=20, default='None')
	Verify_Status=models.CharField(max_length=20, default='Unverified')
	Status=models.CharField(max_length=20, default='Active')
	class Meta:
		db_table="UserData"

class MailData(models.Model):
	Mail_Date=models.CharField(max_length=15, default=date.today())
	Mail_ID=models.CharField(max_length=50, primary_key=True)
	User_ID=models.CharField(max_length=50)
	User_Email=models.CharField(max_length=50)
	To_Email=models.CharField(max_length=50)
	Subject=models.CharField(max_length=200, default="no-subject")
	Message=models.CharField(max_length=500)
	MediaFile=models.FileField(upload_to='mediafiles/')
	class Meta:
		db_table="MailData"

class SentData(models.Model):
	Mail_Date=models.CharField(max_length=15, default=date.today())
	Mail_ID=models.CharField(max_length=50, primary_key=True)
	User_ID=models.CharField(max_length=50)
	User_Email=models.CharField(max_length=50)
	To_Email=models.CharField(max_length=50)
	Message=models.CharField(max_length=500)
	MediaSize=models.CharField(max_length=70)
	class Meta:
		db_table="SentData"

class UserPlanData(models.Model):
	Plan_Date=models.DateField(auto_now=True)
	Plan_ID=models.CharField(max_length=7, default='PL001')
	User_ID=models.CharField(max_length=50)
	Pay_ID=models.CharField(max_length=20, default='Not Availiable')
	class Meta:
		db_table="UserPlanData"