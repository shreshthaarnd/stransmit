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
		if delta.days == 10:
			if not SentData.objects.filter(Mail_ID=x.Mail_ID).exists():
				obj=SentData(
					Mail_Date=x.Mail_Date,
					Mail_ID=x.Mail_ID,
					User_ID=x.User_ID,
					User_Email=x.User_Email,
					To_Email=x.To_Email,
					Message=x.Message
					)
				obj.save()
				MailData.objects.filter(Mail_ID=x.Mail_ID).delete()
	return 'Done'

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

def downloaddata(table):
	if table=='UserData':
		response = HttpResponse()
		response['Content-Disposition'] = 'attachment;filename=UserData.csv'
		writer = csv.writer(response)
		writer.writerow(["User_ID", "User_Name", "User_Email", "User_Phone", "User_Password", "Verify_Status", "Status"])
		obj1=UserData.objects.all()
		for x in obj1:
			writer.writerow([x.User_ID, x.User_Name, x.User_Email, x.User_Phone, x.User_Password, x.Verify_Status, x.Status])
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
		writer.writerow(["Mail_Date", "Mail_ID", "User_ID", "User_Email", "To_Email", "Message"])
		obj1=SentData.objects.all()
		for x in obj1:
			writer.writerow([x.Mail_Date, x.Mail_ID, x.User_ID, x.User_Email, x.To_Email, x.Message])
		return response