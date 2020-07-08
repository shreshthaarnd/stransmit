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

def sendmail(email, subject, message, media, userid, useremail):
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