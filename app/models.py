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

class PayData(models.Model):
	Pay_Date=models.DateTimeField(auto_now=True)
	Pay_ID=models.CharField(max_length=100, primary_key=True)
	Plan_ID=models.CharField(max_length=7)
	User_ID=models.CharField(max_length=50)
	Status=models.CharField(max_length=20, default='Not Availiable')
	class Meta:
		db_table="PayData"

class PaymentData(models.Model):
	Pay_ID=models.CharField(max_length=100, primary_key=True)
	CURRENCY=models.CharField(max_length=100, default='None', blank=True)
	GATEWAYNAME=models.CharField(max_length=100, default='None', blank=True)
	RESPMSG=models.CharField(max_length=1000, default='None', blank=True)
	BANKNAME=models.CharField(max_length=100, default='None', blank=True)
	PAYMENTMODE=models.CharField(max_length=100, default='None', blank=True)
	RESPCODE=models.CharField(max_length=100, default='None', blank=True)
	TXNID=models.CharField(max_length=100, default='None', blank=True)
	TXNAMOUNT=models.CharField(max_length=100, default='None', blank=True)
	STATUS=models.CharField(max_length=100, default='None', blank=True)
	BANKTXNID=models.CharField(max_length=100, default='None', blank=True)
	TXNDATE=models.CharField(max_length=100, default='None', blank=True)
	CHECKSUMHASH=models.CharField(max_length=100, default='None', blank=True)
	class Meta:
		db_table="PaymentData"