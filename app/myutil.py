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