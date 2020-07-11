from django.shortcuts import render, redirect
from django.views.decorators.csrf import *
from app.models import *
from django.core.paginator import *
from django.core.mail import EmailMessage
from django.http import *
import uuid
from app.myutil import *
import csv
import datetime
from django.conf import settings
import os
from django.conf import settings
# Create your views here.
def download(request):
	return render(request,'download.html',{})
def index(request):
	dic={'verify':False,'checksession':checksession(request)}
	return render(request,'index.html',dic)
def blog(request):
	return render(request,'blog.html',{})
def contact(request):
	dic={'checksession':checksession(request)}
	return render(request,'contact.html',dic)
def forgotpass(request):
	return render(request,'forgotpass.html',{})
@csrf_exempt
def sendpassword(request):
	email=request.POST.get('email')
	if UserData.objects.filter(User_Email=email).exists():
		for x in UserData.objects.filter(User_Email=email):
			msg='''Hi '''+x.User_Name+'''!
Your Password is : '''+x.User_Password+'''

Thanks!,
Stransmit.com'''
			sub='Stransmit - Account Recovery Email'
			email=EmailMessage(sub,msg,to=[email])
			email.send()
			break
		return HttpResponse("<script>alert('Password has been sent to your email, you may proceed for login.'); window.location.replace('/index/')</script>")
	else:
		return HttpResponse("<script>alert('Incorrect Email, Account not found with this email.'); window.location.replace('/forgotpass/')</script>")
def sendquery(request):
	name=request.POST.get('name')
	email=request.POST.get('email')
	subject=request.POST.get('subject')
	message=request.POST.get('message')
	msg='''Hi there!
New Query Message,

Name : '''+name+'''
Email : '''+email+'''
Subject : '''+subject+'''
Message : '''+message+'''

Thanks!,
Stransmit.com'''
	sub='Stransmit - New Query Received'
	email=EmailMessage(sub,msg,to=['stransmitdotcom@gmail.com'])
	email.send()
	return HttpResponse("<script>alert('Thanks for contacting us!'); window.location.replace('/contact/')</script>")
def elements(request):
	return render(request,'elements.html',{})
def features(request):
	return render(request,'features.html',{})
def pricing(request):
	return render(request,'pricing.html',{})
def singleblog(request):
	return render(request,'single-blog.html',{})
def registration(request):
	return render(request,'registration.html',{})
def logout(request):
	try:
		del request.session['userid']
		request.session.flush()
		return redirect('/index/')
	except:
		return redirect('/index/')
def userdashboard(request):
	try:
		uid=request.session['userid']
		userdata=UserData.objects.filter(User_ID=uid)
		mails=MailData.objects.filter(User_ID=uid)
		smails=SentData.objects.filter(User_ID=uid)
		dic={'userdata':userdata,
			'mails':reversed(mails),
			'smails':reversed(mails)}
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
def downloadmailcsv(request):
	file_path = os.path.join(settings.MEDIA_ROOT, 'mails.csv')
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
		raise Http404
import pandas as pd
@csrf_exempt
def sendbulkmails(request):
	if request.method=='POST':
		uid=request.session['userid']
		subject=request.POST.get('subject')
		message=request.POST.get('message')
		media=request.FILES['media']
		emailcsv=request.FILES['emailcsv']
		useremail=''
		for x in UserData.objects.filter(User_ID=uid):
			useremail=x.User_Email
		df=pd.read_csv(emailcsv)
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

Media Link : https://stransmit.com/downloadmedia/?mid='''+mid+'''&mpath='''+str(murl)+'''

Thanks!,
Stransmit.com'''
			sub='Stransmit - New Mail Received'
			email=EmailMessage(sub,msg,to=[toemail])
			email.send()
		return HttpResponse("<script>alert('Mail Sent Successfully'); window.location.replace('/userdashboard/')</script>")
	except:
		return Http404
@csrf_exempt
def saveuser(request):
	if request.method=='POST':
		name=request.POST.get('name')
		email=request.POST.get('email')
		mobile=request.POST.get('mobile')
		password=request.POST.get('password')
		u="U00"
		x=1
		uid=u+str(x)
		while UserData.objects.filter(User_ID=uid).exists():
			x=x+1
			uid=u+str(x)
		x=int(x)
		otp=uuid.uuid5(uuid.NAMESPACE_DNS, uid+str(datetime.datetime.today())+name+mobile+password+email).int
		otp=str(otp)
		otp=otp.upper()[0:6]
		request.session['userotp'] = otp
		obj=UserData(
			User_Date=datetime.date.today(),
			User_ID=uid,
			User_Name=name,
			User_Email=email,
			User_Phone=mobile,
			User_Password=password
			)
		if UserData.objects.filter(User_Email=email).exists():
			return HttpResponse("<script>alert('User Already Exists'); window.location.replace('/index/')</script>")
		else:
			obj.save()
			request.session['useridd'] = uid
			msg='''Hi there!
Your Stransmit Verification OTP is,

'''+otp+'''

Thanks!,
Stransmit.com'''
			sub='Stransmit - Verification One Time Password (OTP)'
			email=EmailMessage(sub,msg,to=[email])
			email.send()
			return render(request,'verify.html',{})
def verifyuser(request):
	return render(request,'verify.html',{})
@csrf_exempt
def verify2(request):
	if request.method=='POST':
		otp=request.POST.get('otp')
		otpp=request.session['userotp']
		uid=request.session['useridd']
		if otp==otpp:
			UserData.objects.filter(User_ID=uid).update(Verify_Status='Verified')
			request.session['userid'] = uid
			return HttpResponse("<script>alert('Account Verified!'); window.location.replace('/userdashboard/')</script>")
		else:
			return HttpResponse("<script>alert('Incorrect OTP'); window.location.replace('/verifyuser/')</script>")
def resendotp2(request):
	try:
		otp=request.session['userotp']
		uid=request.session['useridd']
		for x in UserData.objects.filter(User_ID=uid):
			msg='''Hi there!
Your One Time Password (OTP) is,

'''+otp+'''

Thanks!,
Stransmit.com'''
			sub='Stransmit - One Time Password (OTP)'
			email=EmailMessage(sub,msg,to=[x.User_Email])
			email.send()
			break
		return HttpResponse("<script>alert('Sent Successfully!'); window.location.replace('/verifyuser/')</script>")
	except:
		return redirect('/index/')
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

Media Link : https://stransmit.com/downloadmedia/?mid='''+mid+'''&mpath='''+str(murl)+'''

This media is only availiable for 10 Days.

Thanks!,
Stransmit.com'''
			sub='Stransmit - New Mail Received'
			email=EmailMessage(sub,msg,to=[toemail])
			email.send()
			return HttpResponse("<script>alert('Your mail has been sent successfully.'); window.location.replace('/index/')</script>")
		else:
			otp=uuid.uuid5(uuid.NAMESPACE_DNS, uid+str(datetime.datetime.now())+email).int
			otp=str(otp)
			otp=otp.upper()[0:6]
			request.session['userotp'] = otp
			request.session['useridd'] = uid
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
			password=str(password)
			password=password.upper()[0:8]
			obj=UserData(
				User_Date=datetime.date.today(),
				User_ID=uid,
				User_Email=email,
				User_Password=password
				)
			obj.save()
			msg='''Hi there!
Your One Time Password (OTP) is,

'''+otp+'''

Thanks!,
Stransmit.com'''
			sub='Stransmit - One Time Password (OTP)'
			email=EmailMessage(sub,msg,to=[email])
			email.send()
			dic={'verify':True}
			return render(request,'index.html',dic)
@csrf_exempt
def verify(request):
	if request.method=='POST':
		otp=request.POST.get('otp')
		otpp=request.session['userotp']
		uid=request.session['useridd']
		mid=request.session['mailid']
		if otp==otpp:
			UserData.objects.filter(User_ID=uid).update(Verify_Status='Verified')
			for x in MailData.objects.filter(Mail_ID=mid):
				msg='''Hi there!
A mail has been sent to you from '''+x.User_Email+''' with following message,

Message : '''+x.Message+'''

Media Link : https://stransmit.com/downloadmedia/?mid='''+mid+'''&mpath='''+str(x.MediaFile)+'''

This media is only availiable for 10 Days.

Thanks!,
Stransmit.com'''
				sub='Stransmit - New Mail Received'
				email=EmailMessage(sub,msg,to=[x.To_Email])
				email.send()
				break
			for x in UserData.objects.filter(User_ID=uid):
				msg='''Hi there!
Your Stransmit Account has been successfully created,

Login Email : '''+x.User_Email+'''
Login Password : '''+x.User_Password+'''

Thanks for being with us!,
Stransmit.com'''
				sub='Stransmit - Account Created!'
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
		uid=request.session['useridd']
		for x in UserData.objects.filter(User_ID=uid):
			msg='''Hi there!
Your One Time Password (OTP) is,

'''+otp+'''

Thanks!,
Stransmit.com'''
			sub='Stransmit - One Time Password (OTP)'
			email=EmailMessage(sub,msg,to=[x.User_Email])
			email.send()
			break
		dic={'verify':True,'msg':'OTP Sent Again'}
		return render(request,'index.html',dic)
	except:
		return redirect('/index/')
import boto3
import mimetypes
s3 = boto3.client('s3',
         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
         aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY)
s32 = boto3.resource('s3',
         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
         aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY)
from wsgiref.util import FileWrapper
def downloadmedia(request):
	path=''
	mid=request.GET.get('mid')
	media=request.GET.get('mpath')
	if MailData.objects.filter(Mail_ID=mid,MediaFile=media).exists():
		for x in MailData.objects.filter(Mail_ID=mid,MediaFile=media):
			filename2=str(x.MediaFile)[11:int(len(str(x.MediaFile))+1)]
			bucket = s32.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
			for s3_object in bucket.objects.all():
				path, filename = os.path.split(s3_object.key)
				if filename == filename2:
					with open(filename, 'wb') as f:
						s3.download_fileobj(str(settings.AWS_STORAGE_BUCKET_NAME), s3_object.key, f)
				fl_path = filename2
				file_path = filename2
				file_wrapper = FileWrapper(open(file_path,'rb'))
				file_mimetype, _ = mimetypes.guess_type(file_path)
				response = HttpResponse(file_wrapper, content_type=file_mimetype )
				response['X-Sendfile'] = file_path
				response['Content-Length'] = os.stat(file_path).st_size
				response['Content-Disposition'] = 'attachment; filename=%s' % file_path
				return response
	else:
		return HttpResponse("<script>alert('File Not Found'); window.location.replace('/index/')</script>")
@csrf_exempt
def checklogin(request):
	if request.method=='POST':
		email=request.POST.get('email')
		password=request.POST.get('password')
		if UserData.objects.filter(User_Email=email,User_Password=password).exists():
			if UserData.objects.filter(User_Email=email,Verify_Status='Verified').exists():
				for x in UserData.objects.filter(User_Email=email):
					request.session['userid'] = x.User_ID
				return redirect('/userdashboard/')
			else:
				otp=uuid.uuid5(uuid.NAMESPACE_DNS, str(datetime.datetime.today())+password+email).int
				otp=str(otp)
				otp=otp.upper()[0:6]
				msg='''Hi there!
Your Stransmit Verification OTP is,

'''+otp+'''

Thanks!,
Stransmit.com'''
				sub='Stransmit - Verification One Time Password (OTP)'
				email=EmailMessage(sub,msg,to=[email])
				email.send()
				for x in UserData.objects.filter(User_Email=email):
					request.session['useridd'] = x.User_ID
				request.session['userotp'] = otp
				return render(request,'verify.html',{})
		else:
			return HttpResponse("<script>alert('Incorrect Login Credentials'); window.location.replace('/index/')</script>")
	else:
		raise Http404
def adminlogin(request):
	return render(request,'adminpages/login.html',{})
@csrf_exempt
def adminchecklogin(request):
	email=request.POST.get('email')
	password=request.POST.get('password')
	if email=='admin@stransmit.com' and password=='2Baramttpochna@Stransmit':
		request.session['adminid'] = email
		return redirect('/adminindex/')
	else:
		return HttpResponse("<script>alert('Incorrect Login Credentials'); window.location.replace('/adminlogin/')</script>")
def adminindex(request):
	try:
		adminid=request.session['adminid']
		users=len(UserData.objects.all())
		mails=len(MailData.objects.all())+len(SentData.objects.all())
		return render(request,'adminpages/index.html',{'users':users,'mails':mails})
	except:
		raise Http404
def checkmediadel(request):
	try:
		adminid=request.session['adminid']
		checkmedia()
		return HttpResponse("<script>alert('Deleted Successfully'); window.location.replace('/adminindex/')</script>")
	except:
		raise Http404
def adminlogut(request):
	try:
		del request.session['adminid']
		request.session.flush()
		return redirect('/adminlogin/')
	except:
		return redirect('/index/')
def downloaddatabase(request):
	try:
		aid=request.session['admin']
		return render(request,'adminpages/datatables.html',{})
	except:
		return redirect('/shoppanelpages404/')
def downloadCSV(request):
	try:
		aid=request.session['adminid']
		table=request.GET.get('tablename')
		return downloaddata(table)
	except:
		return redirect('/shoppanelpages404/')
def adminuserlist(request):
	return render(request,'adminpages/userlist.html',{})
def adminblockeduser(request):
	return render(request,'adminpages/blockeduser.html',{})
def adminsentmaillist(request):
	return render(request,'adminpages/sentmaillist.html',{})