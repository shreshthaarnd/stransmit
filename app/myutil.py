from django.shortcuts import render, redirect
from django.views.decorators.csrf import *
from app.models import *
from django.core.paginator import *
from django.core.mail import EmailMessage
from django.http import HttpResponse
import uuid
from app.myutil import *
import csv
import datetime
from django.conf import settings
import os

def checkmedia():
	for x in MailData.objects.all():
		mdate=x.Mail_Date
		myear=mdate[:4]
		mmonth=mdate[5:7]
		mday=mdate[8:10]
		tdate=datetime.date.today()
		delta=tdate-datetime.date(int(myear), int(mmonth), int(mday))
		if GetPlanID(x.User_ID) == 'PL001' and delta.days < 10:
			if not SentData.objects.filter(Mail_ID=x.Mail_ID).exists():
				obj=SentData(
					Mail_Date=x.Mail_Date,
					Mail_ID=x.Mail_ID,
					User_ID=x.User_ID,
					User_Email=x.User_Email,
					To_Email=x.To_Email,
					Subject=x.Subject,
					Message=x.Message,
					MediaSize=GetFileSize(x.MediaFile)
					)
				obj.save()
				MailData.objects.filter(Mail_ID=x.Mail_ID).delete()
		if GetPlanID(x.User_ID) == 'PL002' and delta.days < 20:
			if not SentData.objects.filter(Mail_ID=x.Mail_ID).exists():
				obj=SentData(
					Mail_Date=x.Mail_Date,
					Mail_ID=x.Mail_ID,
					User_ID=x.User_ID,
					User_Email=x.User_Email,
					To_Email=x.To_Email,
					Message=x.Message,
					MediaSize=GetFileSize(x.MediaFile)
					)
				obj.save()
				MailData.objects.filter(Mail_ID=x.Mail_ID).delete()
		if GetPlanID(x.User_ID) == 'PL003' and delta.days < 30:
			if not SentData.objects.filter(Mail_ID=x.Mail_ID).exists():
				obj=SentData(
					Mail_Date=x.Mail_Date,
					Mail_ID=x.Mail_ID,
					User_ID=x.User_ID,
					User_Email=x.User_Email,
					To_Email=x.To_Email,
					Message=x.Message,
					MediaSize=GetFileSize(x.MediaFile)
					)
				obj.save()
				MailData.objects.filter(Mail_ID=x.Mail_ID).delete()
	return 'Done'

def GetPlanID(uid):
	response=''
	for x in UserPlanData.objects.filter(User_ID=uid):
		response=x.Plan_ID
	return response
def sendmailutil(email, subject, message, media, userid, useremail):
	m='M00'
	x=1
	mid=m+str(x)
	while MailData.objects.filter(Mail_ID=mid).exists():
		x=x+1
		mid=m+str(x)
	x=int(x)
	obj=MailData(
		Mail_Date=str(datetime.date.today()),
		Mail_ID=mid,
		User_ID=userid,
		User_Email=useremail,
		To_Email=email,
		Message=message,
		MediaFile=media
		)
	obj.save()
	murl=''
	for x in MailData.objects.filter(Mail_ID=mid):
		murl=x.MediaFile
	msg='''Hi there!
A mail has been sent to you from '''+useremail+''' with following message,

Subject : '''+subject+'''
Message : '''+message+'''

Media Link : http://127.0.0.1:8000/downloadmedia/?mid='''+mid+'''&mpath='''+str(murl)+'''

Thanks!,
S|Transmit.com'''
	sub='S|Transmit - New Mail Received'
	email=EmailMessage(sub,msg,to=[email])
	email.send()
def checksession(request):
	try:
		uid=request.session['userid']
		return True
	except:
		return False

def checkplan(userid):
	for x in UserPlanData.objects.filter(User_ID=userid):
		delta=datetime.date.today()-x.Plan_Date
		if delta.days > 30:
			UserPlanData.objects.filter(User_ID=userid).update(Plan_ID='PL001')

def downloaddata(table):
	if table=='UserData':
		response = HttpResponse()
		response['Content-Disposition'] = 'attachment;filename=UserData.csv'
		writer = csv.writer(response)
		writer.writerow(["User_Date", "User_ID", "User_Name", "User_Email", "User_Phone", "User_Password", "Verify_Status", "Status"])
		obj1=UserData.objects.all()
		for x in obj1:
			writer.writerow([x.User_Date, x.User_ID, x.User_Name, x.User_Email, x.User_Phone, x.User_Password, x.Verify_Status, x.Status])
		return response
	if table=='MailData':
		response = HttpResponse()
		response['Content-Disposition'] = 'attachment;filename=MailData.csv'
		writer = csv.writer(response)
		writer.writerow(["Mail_Date", "Mail_ID", "User_ID", "User_Email", "To_Email", "Subject", "Message", "MediaFile"])
		obj1=MailData.objects.all()
		for x in obj1:
			writer.writerow([x.Mail_Date, x.Mail_ID, x.User_ID, x.User_Email, x.To_Email, x.Subject, x.Message, x.MediaFile])
		return response
	if table=='SentData':
		response = HttpResponse()
		response['Content-Disposition'] = 'attachment;filename=SentData.csv'
		writer = csv.writer(response)
		writer.writerow(["Mail_Date", "Mail_ID", "User_ID", "User_Email", "To_Email", "Subject", "Message", "MediaSize"])
		obj1=SentData.objects.all()
		for x in obj1:
			writer.writerow([x.Mail_Date, x.Mail_ID, x.User_ID, x.User_Email, x.To_Email, x.Subject, x.Message, x.MediaSize])
		return response
	if table=='UserPlanData':
		response = HttpResponse()
		response['Content-Disposition'] = 'attachment;filename=UserPlanData.csv'
		writer = csv.writer(response)
		writer.writerow(["Plan_Date", "Plan_ID", "User_ID", "Pay_ID"])
		obj1=UserPlanData.objects.all()
		for x in obj1:
			writer.writerow([x.Plan_Date, x.Plan_ID, x.User_ID, x.Pay_ID])
		return response
	if table=='PayData':
		response = HttpResponse()
		response['Content-Disposition'] = 'attachment;filename=PayData.csv'
		writer = csv.writer(response)
		writer.writerow(["Pay_Date", "Pay_ID", "Plan_ID", "User_ID", "Status"])
		obj1=PayData.objects.all()
		for x in obj1:
			writer.writerow([x.Pay_Date, x.Pay_ID, x.Plan_ID, x.User_ID, x.Status])
		return response
	if table=='PaymentData':
		response = HttpResponse()
		response['Content-Disposition'] = 'attachment;filename=PaymentData.csv'
		writer = csv.writer(response)
		writer.writerow(["Pay_ID", "CURRENCY", "GATEWAYNAME", "RESPMSG", "BANKNAME", "PAYMENTMODE", "RESPCODE", "TXNID", "TXNAMOUNT", "STATUS", "BANKTXNID", "TXNDATE", "CHECKSUMHASH"])
		obj1=PaymentData.objects.all()
		for x in obj1:
			writer.writerow([x.Pay_ID, x.CURRENCY, x.GATEWAYNAME, x.RESPMSG, x.BANKNAME, x.PAYMENTMODE, x.RESPCODE, x.TXNID, x.TXNAMOUNT, x.STATUS, x.BANKTXNID, x.TXNDATE, x.CHECKSUMHASH])
		return response

import boto3
def GetFileSize(media):
	s3 = boto3.client('s3',
         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
         aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY)
	response = s3.head_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key='media/'+str(media))
	size = response['ContentLength']
	return sizify(size)

def sizify(value):
	value = value / 1073741824.0
	return value

def GetPlanMailDifference(MailId):
	response=False
	for x in MailData.objects.filter(Mail_ID=MailId):
		plandate=''
		for y in UserPlanData.objects.filter(User_ID=x.User_ID):
			plandate=y.Plan_Date
		mdate=x.Mail_Date
		myear=mdate[:4]
		mmonth=mdate[5:7]
		mday=mdate[8:10]
		tdate=datetime.date.today()
		delta=datetime.date(int(myear), int(mmonth), int(mday))-plandate
		if delta.days > 0:
			response = True
		else:
			response = False
	return response

def Get30DaysMailsSize(userid):
	size=0.0
	for x in SentData.objects.filter(User_ID=userid):
		if GetPlanMailDifference(x.Mail_ID):
			mdate=x.Mail_Date
			myear=mdate[:4]
			mmonth=mdate[5:7]
			mday=mdate[8:10]
			tdate=datetime.date.today()
			delta=tdate-datetime.date(int(myear), int(mmonth), int(mday))
			if delta.days < 30:
				size=size+float(x.MediaSize)
	return size

def checkmediasize(userid):
	mails=MailData.objects.filter(User_ID=userid)
	size=0.0
	for x in mails:
		size=size+GetFileSize(x.MediaFile)
	size=size+Get30DaysMailsSize(userid)
	if GetPlanID(userid) == 'PL002':
		if size > 1000.0:
			return False
		else:
			return True
	elif GetPlanID(userid) == 'PL003':
		if size > 2000.0:
			return False
		else:
			return True
	elif GetPlanID(userid) == 'PL001':
		if size > 50.0:
			return False
		else:
			return True