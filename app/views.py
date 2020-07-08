from django.shortcuts import render, redirect
from django.views.decorators.csrf import *
from app.models import *
from django.core.paginator import *
from django.core.mail import EmailMessage
from django.http import HttpResponse, Http404
import uuid
from app.myutil import *
import csv
import datetime
from django.conf import settings
import os
from django.conf import settings
# Create your views here.
def index(request):
	dic={'verify':False}
	return render(request,'index.html',dic)
def blog(request):
	return render(request,'blog.html',{})
def contact(request):
	return render(request,'contact.html',{})
def elements(request):
	return render(request,'elements.html',{})
def features(request):
	return render(request,'features.html',{})
def pricing(request):
	return render(request,'pricing.html',{})
def singleblog(request):
	return render(request,'single-blog.html',{})
def adminlogin(request):
	return render(request,'adminpages/login.html',{})
def adminindex(request):
	return render(request,'adminpages/index.html',{})
def registration(request):
	return render(request,'registration.html',{})
def userdashboard(request):
	try:
		uid=request.session['userid']
		userdata=UserData.objects.filter(User_ID=uid)
		dic={'userdata':userdata}
		return render(request,'userdashboard.html',dic)
	except:
		return Http404
@csrf_exempt
def edituserdata(request):
	try:
		uid=request.session['userid']
		userdata=UserData.objects.filter(User_ID=uid)
		userdata.update(
			User_Name=request.POST.get('name'),
			User_Phone=request.POST.get('phone'),
			User_Password=request.POST.get('password')
			)
		return HttpResponse("<script>alert('Details Updated Successfully'); window.location.replace('/userdashboard/')</script>")
	except:
		return Http404
import pandas as pd
@csrf_exempt
def sendbulkmails(request):
	if request.method=='POST':
		uid=request.session['userid']
		subject=request.POST.get('subject')
		message=request.POST.get('message')
		media=request.FILES['media']
		useremail=''
		for x in UserData.objects.filter(User_ID=uid):
			useremail=x.User_Email
		df=pd.read_csv(request.FILES['emailcsv'])
		for x in df['Email']:
			sendmailutil(x, subject, message, media, uid, useremail)
		return HttpResponse("<script>alert('Mails Sent Successfully'); window.location.replace('/userdashboard/')</script>")
@csrf_exempt
def usersendmail(request):
	try:
		uid=request.session['userid']
		toemail=request.POST.get('toemail')
		subject=request.POST.get('subject')
		message=request.POST.get('message')
		media=request.FILES['media']
		userdata=UserData.objects.filter(User_ID=uid)
		for i in userdata:
			m="M00"
			x=1
			mid=m+str(x)
			while MailData.objects.filter(Mail_ID=mid).exists():
				x=x+1
				mid=m+str(x)
			x=int(x)
			obj=MailData(
				Mail_Date=str(datetime.date.today()),
				Mail_ID=mid,
				User_ID=uid,
				User_Email=i.User_Email,
				To_Email=toemail,
				Message=message,
				MediaFile=media
				)
			obj.save()
			murl=''
			for x in MailData.objects.filter(Mail_ID=mid):
				murl=x.MediaFile
			msg='''Hi there!
A mail has been sent to you from '''+i.User_Email+''' with following message,

Subject : '''+subject+'''
Message : '''+message+'''

Media Link : http://127.0.0.1:8000/downloadmedia/?mid='''+mid+'''&mpath='''+str(murl)+'''

Thanks!,
S|Transmit.com'''
			sub='S|Transmit - New Mail Received'
			email=EmailMessage(sub,msg,to=[toemail])
			email.send()
		return HttpResponse("<script>alert('Mail Sent Successfully'); window.location.replace('/userdashboard/')</script>")
	except:
		return Http404
@csrf_exempt
def sendmail(request):
	if request.method=='POST':
		email=request.POST.get('email')
		toemail=request.POST.get('toemail')
		message=request.POST.get('message')
		media=request.FILES['media']
		u="U00"
		x=1
		uid=u+str(x)
		while UserData.objects.filter(User_ID=uid).exists():
			x=x+1
			uid=u+str(x)
		x=int(x)
		if UserData.objects.filter(User_Email=email, Verify_Status='Verified').exists():
			m="M00"
			x=1
			mid=m+str(x)
			while MailData.objects.filter(Mail_ID=mid).exists():
				x=x+1
				mid=m+str(x)
			x=int(x)
			uid=''
			for x in UserData.objects.filter(User_Email=email):
				uid=x.User_ID
			obj=MailData(
				Mail_Date=str(datetime.date.today()),
				Mail_ID=mid,
				User_ID=uid,
				User_Email=email,
				To_Email=toemail,
				Message=message,
				MediaFile=media
				)
			obj.save()
			murl=''
			for x in MailData.objects.filter(Mail_ID=mid):
				murl=x.MediaFile
			msg='''Hi there!
A mail has been sent to you from '''+email+''' with following message,

Message : '''+message+'''

Media Link : http://127.0.0.1:8000/downloadmedia/?mid='''+mid+'''&mpath='''+str(murl)+'''

Thanks!,
S|Transmit.com'''
			sub='S|Transmit - New Mail Received'
			email=EmailMessage(sub,msg,to=[toemail])
			email.send()
			return HttpResponse("<script>alert('Your mail has been sent successfully.'); window.location.replace('/index/')</script>")
		else:
			otp=uuid.uuid5(uuid.NAMESPACE_DNS, uid+str(datetime.datetime.now())+email).int
			otp=str(otp)
			otp=otp.upper()[0:6]
			request.session['userotp'] = otp
			request.session['userid'] = uid
			m="M00"
			x=1
			mid=m+str(x)
			while MailData.objects.filter(Mail_ID=mid).exists():
				x=x+1
				mid=m+str(x)
			x=int(x)
			request.session['mailid'] = mid
			obj=MailData(
				Mail_ID=mid,
				User_ID=uid,
				User_Email=email,
				To_Email=toemail,
				Message=message,
				MediaFile=media
				)
			obj.save()
			password=uuid.uuid5(uuid.NAMESPACE_DNS, uid+email).int
			password=str(otp)
			password=password.upper()[0:8]
			obj=UserData(
				User_ID=uid,
				User_Email=email,
				User_Password=password
				)
			obj.save()
			msg='''Hi there!
Your One Time Password (OTP) is,

'''+otp+'''

Thanks!,
S|Transmit.com'''
			sub='S|Transmit - One Time Password (OTP)'
			email=EmailMessage(sub,msg,to=[email])
			email.send()
			dic={'verify':True}
			return render(request,'index.html',dic)
@csrf_exempt
def verify(request):
	if request.method=='POST':
		otp=request.POST.get('otp')
		otpp=request.session['userotp']
		uid=request.session['userid']
		mid=request.session['mailid']
		if otp==otpp:
			UserData.objects.filter(User_ID=uid).update(Verify_Status='Verified')
			for x in MailData.objects.filter(Mail_ID=mid):
				msg='''Hi there!
A mail has been sent to you from '''+x.User_Email+''' with following message,

Message : '''+x.Message+'''

Media Link : http://127.0.0.1:8000/downloadmedia/?mid='''+mid+'''&mpath='''+str(x.MediaFile)+'''

Thanks!,
S|Transmit.com'''
				sub='S|Transmit - New Mail Received'
				email=EmailMessage(sub,msg,to=[x.To_Email])
				email.send()
				break
			for x in UserData.objects.filter(User_ID=uid):
				msg='''Hi there!
Your S|Transmit Account has been successfully created,

Login Email : '''+x.User_Email+'''
Login Password : '''+x.User_Password+'''

Thanks for being with us!,
S|Transmit.com'''
				sub='S|Transmit - Account Created!'
				email=EmailMessage(sub,msg,to=[x.User_Email])
				email.send()
				break
			return HttpResponse("<script>alert('Your mail has been sent successfully. And we have also sent the login credentials to your mail'); window.location.replace('/index/')</script>")
		else:
			dic={'verify':True,'msg':'Incorrect OTP'}
			return render(request,'index.html',dic)
def resendotp(request):
	try:
		otp=request.session['userotp']
		uid=request.session['userid']
		for x in UserData.objects.filter(User_ID=uid):
			msg='''Hi there!
Your One Time Password (OTP) is,

'''+otp+'''

Thanks!,
S|Transmit.com'''
			sub='S|Transmit - One Time Password (OTP)'
			email=EmailMessage(sub,msg,to=[x.User_Email])
			email.send()
			break
		dic={'verify':True,'msg':'OTP Sent Again'}
		return render(request,'index.html',dic)
	except:
		return redirect('/index/')

def downloadmedia(request):
	path=''
	mid=request.GET.get('mid')
	media=request.GET.get('mpath')
	if MailData.objects.filter(Mail_ID=mid,MediaFile=media).exists():
		file_path = os.path.join(settings.MEDIA_ROOT, media)
		if os.path.exists(file_path):
			with open(file_path, 'rb') as fh:
				response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
				response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
				return response
			raise Http404
	else:
		return HttpResponse("<script>alert('File Not Found'); window.location.replace('/index/')</script>")
def checkmediadel(request):
	return HttpResponse(checkmedia())
@csrf_exempt
def checklogin(request):
	if request.method=='POST':
		email=request.POST.get('email')
		password=request.POST.get('password')
		if UserData.objects.filter(User_Email=email,User_Password=password).exists():
			for x in UserData.objects.filter(User_Email=email):
				request.session['userid'] = x.User_ID
			return redirect('/userdashboard/')
		else:
			return HttpResponse("<script>alert('Incorrect Login Credentials'); window.location.replace('/index/')</script>")
	else:
		raise Http404