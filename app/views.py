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
from app.htmlmail import *

def emaildownload(request):
	mail=open('app/templates/email.html', 'r')
	#sendemail(mail.read())
	return render(request,'email.html',{})
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
			sendforgotpassword(x.User_Password, email)
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
	try:
		uid=request.session['userid']
		pid=GetPlanID(uid)
		dic={'checksession':checksession(request),
			'plan':pid}
		return render(request,'stransmitpricing.html',dic)
	except:
		dic={'checksession':checksession(request)}
		return render(request,'stransmitpricing.html',dic)
def singleblog(request):
	return render(request,'single-blog.html',{})
def registration(request):
	return render(request,'registration.html',{})
def logout(request):
	try:
		del request.session['userid']
		return redirect('/index/')
	except:
		return redirect('/index/')
def userdashboard(request):
	try:
		uid=request.session['userid']
		pid=GetPlanID(uid)
		userdata=UserData.objects.filter(User_ID=uid)
		mails=MailData.objects.filter(User_ID=uid)
		smails=SentData.objects.filter(User_ID=uid)
		dic={'userdata':userdata,
			'plan':pid,
			'mails':reversed(mails),
			'smails':reversed(smails)}
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
		fromemail=''
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
			if checkmediasize(uid):
				obj.save()
				murl=''
				fromemail=i.User_Email
				for x in MailData.objects.filter(Mail_ID=mid):
					murl=x.MediaFile
				link='https://stransmit.com/downloadmedia/?mid='+mid+'&mpath='+str(murl)
				sendemail(subject, message, toemail, fromemail, link)
				return HttpResponse("<script>alert('Mail Sent Successfully!'); window.location.replace('/userdashboard/')</script>")
			else:
				return HttpResponse("<script>alert('Media Limit Exceed! Kindly Upgrade Your Plan.'); window.location.replace('/userdashboard/')</script>")
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
			sendotp(otp, email)
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
			UserPlanData(User_ID=uid).save()
			request.session['userid'] = uid
			for x in UserData.objects.filter(User_ID=uid):
				sendaccountdetails(x.User_Email, x.User_Password)
				break
			return HttpResponse("<script>alert('Account Verified!'); window.location.replace('/userdashboard/')</script>")
		else:
			return HttpResponse("<script>alert('Incorrect OTP'); window.location.replace('/verifyuser/')</script>")
def resendotp2(request):
	try:
		otp=request.session['userotp']
		uid=request.session['useridd']
		for x in UserData.objects.filter(User_ID=uid):
			sendotp(otp, x.User_Email)
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
		if UserData.objects.filter(User_Email=email, Verify_Status='Verified', Status='Active').exists():
			m="M00"
			x=1
			mid=m+str(x)
			while MailData.objects.filter(Mail_ID=mid).exists():
				x=x+1
				mid=m+str(x)
			x=int(x)
			request.session['mailid'] = mid
			uid=''
			for x in UserData.objects.filter(User_Email=email):
				uid=x.User_ID
				request.session['useridd'] = x.User_ID
			obj=MailData(
				Mail_Date=str(datetime.date.today()),
				Mail_ID=mid,
				User_ID=uid,
				User_Email=email,
				To_Email=toemail,
				Message=message,
				MediaFile=media
				)
			if checkmediasize(uid):
				obj.save()
				dic={'useremail':email}
				return render(request, 'password.html', dic)
			else:
				return HttpResponse("<script>alert('Your Monthly Limit Exceeds! Kindly Upgrade Your Plan'); window.location.replace('/index/')</script>")
		else:
			if UserData.objects.filter(User_Email=email, Verify_Status='Verified', Status='Deactive').exists():
				return HttpResponse("<script>alert('Your account is Deactivated by the Admin. Kindly send query from Contact Page.'); window.location.replace('/index/')</script>")
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
				sendotp(otp, email)
				dic={'verify':True}
				return render(request,'index.html',dic)

def forgotpass2(request):
	uid=request.session['useridd']
	email=''
	for x in UserData.objects.filter(User_ID=uid):
		sendforgotpassword(x.User_Password, x.User_Email)
		email=x.User_Email
		break
	dic={'useremail':email, 'msg':'Password has been sent to your email.'}
	return render(request, 'password.html', dic)

@csrf_exempt
def password(request):
	uid=request.session['useridd']
	mid=request.session['mailid']
	password=request.POST.get('password')
	if UserData.objects.filter(User_ID=uid, User_Password=password).exists():
		for x in MailData.objects.filter(Mail_ID=mid):
			link='https://stransmit.com/downloadmedia/?mid='+mid+'&mpath='+str(x.MediaFile)
			sendemail('no-subject', x.Message, x.To_Email, x.User_Email, link)
			break
		request.session['userid'] = uid
		return HttpResponse("<script>alert('Your mail has been sent successfully.'); window.location.replace('/userdashboard/')</script>")
	else:
		uemail=''
		for x in UserData.objects.filter(User_ID=uid):
			uemail=x.User_Email
		dic={'msg':'Incorrect Password','useremail':uemail}
		return render(request, 'password.html', dic)
@csrf_exempt
def verify(request):
	if request.method=='POST':
		otp=request.POST.get('otp')
		otpp=request.session['userotp']
		uid=request.session['useridd']
		mid=request.session['mailid']
		if otp==otpp:
			UserData.objects.filter(User_ID=uid).update(Verify_Status='Verified')
			UserPlanData(User_ID=uid).save()
			for x in MailData.objects.filter(Mail_ID=mid):
				link='https://stransmit.com/downloadmedia/?mid='+mid+'&mpath='+str(x.MediaFile)
				sendemail('no-subject', x.Message, x.To_Email, x.User_Email, link)
				break
			for x in UserData.objects.filter(User_ID=uid):
				sendaccountdetails(x.User_Email, x.User_Password)
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
			sendotp(otp, x.User_Email)
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
import requests
def downloadmedia2(request):
	path=''
	mid=request.GET.get('mid')
	media=request.GET.get('mpath')
	if MailData.objects.filter(Mail_ID=mid,MediaFile=media).exists():
		for x in MailData.objects.filter(Mail_ID=mid,MediaFile=media):
			filename=str(x.MediaFile)[11:int(len(str(x.MediaFile))+1)]
			url = x.MediaFile.url
			r = requests.get(url, allow_redirects=True)
			filedownload = open(filename, 'wb').write(r.content)
			return render(request,'download2.html',{'filename':filename})
	else:
		return HttpResponse("<script>alert('File Not Found'); window.location.replace('/index/')</script>")
def downloadmedia3(request):
	filename=request.GET.get('filename')
	fl_path = filename
	file_path = filename
	file_wrapper = FileWrapper(open(filename, 'rb'))
	file_mimetype, _ = mimetypes.guess_type(file_path)
	response = HttpResponse(file_wrapper, content_type=file_mimetype )
	response['X-Sendfile'] = file_path
	response['Content-Length'] = os.stat(file_path).st_size
	response['Content-Disposition'] = 'attachment; filename=%s' % file_path
	os.remove(filename)
	return response

def downloadmedia(request):
	path=''
	mid=request.GET.get('mid')
	media=request.GET.get('mpath')
	return render(request,'download.html',{'mid':mid,'mpath':media})
@csrf_exempt
def checklogin(request):
	if request.method=='POST':
		email=request.POST.get('email')
		password=request.POST.get('password')
		if UserData.objects.filter(User_Email=email,User_Password=password, Status='Active').exists():
			if UserData.objects.filter(User_Email=email,Verify_Status='Verified').exists():
				for x in UserData.objects.filter(User_Email=email):
					request.session['userid'] = x.User_ID
				checkplan(request.session['userid'])
				return redirect('/userdashboard/')
			else:
				otp=uuid.uuid5(uuid.NAMESPACE_DNS, str(datetime.datetime.today())+password+email).int
				otp=str(otp)
				otp=otp.upper()[0:6]
				email2=request.POST.get('email')
				sendotp(otp, email)
				for x in UserData.objects.filter(User_Email=email2):
					request.session['useridd'] = x.User_ID
				request.session['userotp'] = otp
				return render(request,'verify.html',{})
		else:
			if UserData.objects.filter(User_Email=email,Status='Deactive').exists():
				return HttpResponse("<script>alert('Your account is Deactivated by the Admin. Kindly send a query from Contact Page.'); window.location.replace('/index/')</script>")
			else:
				return HttpResponse("<script>alert('Incorrect Login Email or Password'); window.location.replace('/index/')</script>")	
	else:
		raise Http404

import app.Checksum as Checksum
def checkout(request):
	plan=request.GET.get('plan')
	uid=request.session['userid']
	l="PY00"
	x=1
	lid=l+str(x)
	while PayData.objects.filter(Pay_ID=lid).exists():
		x=x+1
		lid=l+str(x)
	x=int(x)
	obj=PayData(
		Pay_ID=lid,
		Plan_ID=plan,
		User_ID=uid,
		)
	obj.save()
	amount = 0
	if plan == 'PL002':
		amount=299
	elif plan == 'PL003':
		amount=399
	dic={
			'ORDER_ID':lid,
			'TXN_AMOUNT':str(amount),
			'CUST_ID':uid,
			'INDUSTRY_TYPE_ID':'Retail',
			'CHANNEL_ID':'WEB',
			'WEBSITE':'DEFAULT',
			'CALLBACK_URL':'https://stransmit.com/verifypayment/'
	}
	MERCHANT_KEY = 'UvLwriZgMrbFs65E'
	MID = 'iogjiL69888304358895'
	data_dict = {'MID':MID}
	data_dict.update(dic)
	param_dict = data_dict
	param_dict['CHECKSUMHASH'] =Checksum.generateSignature(data_dict, MERCHANT_KEY)
	param_dict.update({'checksession':checksession(request),
			'plan':plan})
	return render(request,'checkout.html',param_dict)

import cgi
@csrf_exempt
def verifypayment(request):
		MERCHANT_KEY = 'UvLwriZgMrbFs65E'
		MID = 'iogjiL69888304358895'
		CURRENCY=request.POST.get('CURRENCY')
		GATEWAYNAME=request.POST.get('GATEWAYNAME')
		RESPMSG=request.POST.get('RESPMSG')
		BANKNAME=request.POST.get('BANKNAME')
		PAYMENTMODE=request.POST.get('PAYMENTMODE')
		RESPCODE=request.POST.get('RESPCODE')
		TXNID=request.POST.get('TXNID')
		TXNAMOUNT=request.POST.get('TXNAMOUNT')
		ORDERID=request.POST.get('ORDERID')
		STATUS=request.POST.get('STATUS')
		BANKTXNID=request.POST.get('BANKTXNID')
		TXNDATE=request.POST.get('TXNDATE')
		CHECKSUMHASH=request.POST.get('CHECKSUMHASH')
		respons_dict = {
						'MERCHANT_KEY':MERCHANT_KEY,
						'CURRENCY':CURRENCY,
						'GATEWAYNAME':GATEWAYNAME,
						'RESPMSG':RESPMSG,
						'BANKNAME':BANKNAME,
						'PAYMENTMODE':PAYMENTMODE,
						'MID':MID,
						'RESPCODE':RESPCODE,
						'TXNID':TXNID,
						'TXNAMOUNT':TXNAMOUNT,
						'ORDERID':ORDERID,
						'STATUS':STATUS,
						'BANKTXNID':BANKTXNID,
						'TXNDATE':TXNDATE,
						'CHECKSUMHASH':CHECKSUMHASH
		}
		checksum=respons_dict['CHECKSUMHASH']
		if 'GATEWAYNAME' in respons_dict:
			if respons_dict['GATEWAYNAME'] == 'WALLET':
				respons_dict['BANKNAME'] = 'null';
		obj=PaymentData(
			Pay_ID=ORDERID,
			CURRENCY=CURRENCY,
			GATEWAYNAME=str(GATEWAYNAME),
			RESPMSG=RESPMSG,
			BANKNAME=str(BANKNAME),
			PAYMENTMODE=str(PAYMENTMODE),
			RESPCODE=RESPCODE,
			TXNID=str(TXNID),
			TXNAMOUNT=TXNAMOUNT,
			STATUS=STATUS,
			BANKTXNID=BANKTXNID,
			TXNDATE=str(TXNDATE),
			CHECKSUMHASH=str(CHECKSUMHASH)
			)
		obj.save()
		obj=PayData.objects.filter(Pay_ID=ORDERID)
		for x in obj:
			request.session['userid']=str(x.User_ID)
		custid=request.session['userid']
		data_dict = {
			'MID':respons_dict['MID'],
			'ORDER_ID':ORDERID,
			'TXN_AMOUNT':TXNAMOUNT,
			'CUST_ID':custid,
			'INDUSTRY_TYPE_ID':'Retail',
			'CHANNEL_ID':'WEB',
			'WEBSITE':'DEFAULT',
			'CALLBACK_URL':'https://stransmit.com/verifypayment/'
			}
		checksum =Checksum.generateSignature(data_dict, MERCHANT_KEY)
		verify = Checksum.verifySignature(data_dict, MERCHANT_KEY, checksum)
		if verify:
			if respons_dict['RESPCODE'] == '01':
				obj=PayData.objects.filter(Pay_ID=ORDERID)
				obj.update(Status='Success')
				dic={}
				for x in obj:
					request.session['userid'] = x.User_ID
					UserPlanData.objects.filter(User_ID=x.User_ID).delete()
					UserPlanData(
						Plan_ID=x.Plan_ID,
						User_ID=x.User_ID,
						Pay_ID=x.Pay_ID
						).save()
					for y in UserData.objects.filter(User_ID=x.User_ID):
						sendplanmail(y.User_Email, x.Plan_ID, TXNDATE, TXNID, ORDERID, TXNAMOUNT)
					dic={'TXNID':TXNID,
						'PAYID':ORDERID,
						'PLAN':x.Plan_ID,
						'TXNDATE':TXNDATE,
						'checksession':checksession(request)}
				return render(request,'paymentsuccess.html',dic)
			else:
				obj=PayData.objects.filter(Pay_ID=ORDERID)
				obj.update(Status='Failed')
				dic={}
				for x in obj:
					request.session['userid'] = x.User_ID
					dic={'TXNID':TXNID,
						'PAYID':ORDERID,
						'TXNDATE':TXNDATE,
						'RESPMSG':RESPMSG,
						'checksession':checksession(request)}
				return render(request,'paymentfailure.html',dic)
		else:
			obj=PayData.objects.filter(Pay_ID=ORDERID)
			obj.update(Status='Failed')
			dic={}
			for x in obj:
				request.session['userid'] = x.User_ID
				dic={'TXNID':TXNID,
					'PAYID':ORDERID,
					'TXNDATE':TXNDATE,
					'RESPMSG':RESPMSG,
					'checksession':checksession(request)}
			return render(request,'paymentfailure.html',dic)

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
		return redirect('/adminlogin/')
	except:
		return redirect('/index/')
def downloaddatabase(request):
	try:
		aid=request.session['admin']
		return render(request,'adminpages/datatables.html',{})
	except:
		raise Http404
def downloadCSV(request):
	try:
		aid=request.session['adminid']
		table=request.GET.get('tablename')
		return downloaddata(table)
	except:
		raise Http404
def adminuserlist(request):
	try:
		aid=request.session['adminid']
		dic={'data':UserData.objects.all()}
		return render(request,'adminpages/userlist.html',dic)
	except:
		raise Http404
def adminblockuser(request):
	try:
		aid=request.session['adminid']
		uid=request.GET.get('user')
		UserData.objects.filter(User_ID=uid).update(Status='Deactive')
		return redirect('/adminuserlist/')
	except:
		raise Http404
def adminunblockuser(request):
	try:
		aid=request.session['adminid']
		uid=request.GET.get('user')
		UserData.objects.filter(User_ID=uid).update(Status='Active')
		return redirect('/adminuserlist/')
	except:
		raise Http404
def adminblockeduser(request):
	return render(request,'adminpages/blockeduser.html',{})
def adminsentmaillist(request):
	try:
		aid=request.session['adminid']
		dic={'data':MailData.objects.all(),'data2':SentData.objects.all()}
		return render(request,'adminpages/sentmaillist.html',dic)
	except:
		raise Http404
'''def uploaddata(request):
	df=pd.read_csv('app/data/UserData.csv')
	for x in range(0,len(df)):
		data=df.loc[x]
		obj=UserData(
			User_Date=data.User_Date,
			User_ID=data.User_ID,
			User_Name=data.User_Name,
			User_Email=data.User_Email,
			User_Phone=data.User_Phone,
			User_Password=data.User_Password,
			Verify_Status=data.Verify_Status,
			Status=data.Status
			)
		obj.save()
	df=pd.read_csv('app/data/MailData.csv')
	for x in range(0,len(df)):
		data=df.loc[x]
		obj=MailData(
			Mail_Date=data.Mail_Date,
			Mail_ID=data.Mail_ID,
			User_ID=data.User_ID,
			User_Email=data.User_Email,
			To_Email=data.To_Email,
			Subject=data.Subject,
			Message=data.Message,
			MediaFile=data.MediaFile
			)
		obj.save()
		return HttpResponse('Done')'''

def paymentfailure(request):
	return render(request,'paymentfailure.html',{})
def paymentsuccessmail(request):
	return render(request,'successmail.html',{})
def adminusersubcription(request):
	try:
		aid=request.session['adminid']
		dic={'data':UserPlanData.objects.all()}
		return render(request,'adminpages/usersubcription.html',dic)
	except:
		raise Http404
def paymentsuccess(request):
	return render(request,'paymentsuccess.html',{})
def adminpaydata(request):
	try:
		aid=request.session['adminid']
		dic={'data':PayData.objects.all()}
		return render(request,'adminpages/paydata.html',dic)
	except:
		raise Http404
def adminpaymentdata(request):
	try:
		aid=request.session['adminid']
		dic={'data':PaymentData.objects.all()}
		return render(request,'adminpages/paymentdata.html',dic)
	except:
		raise Http404
def adminsitemap(request):
	try:
		aid=request.session['adminid']
		return render(request,'adminpages/sitemap.html',{})
	except:
		raise Http404
@csrf_exempt
def adminsavesitemap(request):
	if request.method=='POST':
		smap=request.POST.get('sitemap')
		Sitemap.objects.all().delete()
		obj=Sitemap(Sitemap=smap).save()
		return HttpResponse("<script>alert('Saved Successfully'); window.location.replace('/adminsitemap/')</script>")
def sitemap(request):
	dic={'data':Sitemap.objects.all()}
	return render(request,'sitemap.xml',dic)
def adminkeyword(request):
	try:
		aid=request.session['adminid']
		return render(request,'adminpages/keyword.html',{})
	except:
		raise Http404
def admindescription(request):
	try:
		aid=request.session['adminid']
		return render(request,'adminpages/description.html',{})
	except:
		raise Http404
def admindownload(request):
	try:
		aid=request.session['adminid']
		return render(request,'adminpages/download.html',{})
	except:
		raise Http404
@csrf_exempt
def forgotpassword(request):
	email=request.POST.get('email')
	uid=''
	for x in UserData.objects.filter(User_Email=email):
		uid=x.User_ID
	uid_encrypt=str(uuid.uuid5(uuid.NAMESPACE_DNS, uid))
	email_encrypt=str(uuid.uuid5(uuid.NAMESPACE_DNS, email))
	link='https://stransmit.com/change/?get1='+uid_encrypt+'&get2='+email_encrypt
	sendpassmail(email, link)
	return HttpResponse("<script>alert('Check Your Mail Please!'); window.location.replace('/index/')</script>")
@csrf_exempt
def forgotpassword2(request):
	email=request.GET.get('email')
	uid=''
	for x in UserData.objects.filter(User_Email=email):
		uid=x.User_ID
	uid_encrypt=str(uuid.uuid5(uuid.NAMESPACE_DNS, uid))
	email_encrypt=str(uuid.uuid5(uuid.NAMESPACE_DNS, email))
	link='https://stransmit.com/change/?get1='+uid_encrypt+'&get2='+email_encrypt
	sendpassmail(email, link)
	dic={'useremail':email,'msg':'Please check your mail. We have sent a mail to change your password.'}
	return render(request, 'password.html', dic)
@csrf_exempt
def forgotpassword3(request):
	email=request.GET.get('email')
	uid=''
	for x in UserData.objects.filter(User_Email=email):
		uid=x.User_ID
	uid_encrypt=str(uuid.uuid5(uuid.NAMESPACE_DNS, uid))
	email_encrypt=str(uuid.uuid5(uuid.NAMESPACE_DNS, email))
	link='https://stransmit.com/change/?get1='+uid_encrypt+'&get2='+email_encrypt
	sendpassmail(email, link)
	return HttpResponse("<script>alert('Check Your Mail Please!'); window.location.replace('/userdashboard/')</script>")
def change(request):
	uid_encrypt=request.GET.get('get1')
	email_encrypt=request.GET.get('get2')
	uid=''
	email=''
	for x in UserData.objects.all():
		uid=str(uuid.uuid5(uuid.NAMESPACE_DNS, x.User_ID))
		email=str(uuid.uuid5(uuid.NAMESPACE_DNS, x.User_Email))
		if uid==uid_encrypt and email==email_encrypt:
			uid=x.User_ID
			email=x.User_Email
			break
	request.session['useridd']=uid
	return render(request,'changepass.html',{})
@csrf_exempt
def savepassword(request):
	if request.method=='POST':
		new=request.POST.get('new')
		cnew=request.POST.get('cnew')
		if new == cnew:
			UserData.objects.filter(User_ID=request.session['useridd']).update(User_Password=new)
			request.session['userid'] = request.session['useridd']
			return HttpResponse("<script>alert('Password changed successfully!'); window.location.replace('/userdashboard/')</script>")
		else:
			dic={'msg':'Password did not match'}
			return render(request,'changepass.html',dic)
	else:
		return redirect('/index/')
def changemail(request):
	return render(request,'changemail.html',{})
def privacy(request):
	return render(request,'privacy.html',{})
def disclaimer(request):
	return render(request,'disclaimer.html',{})
def termcondition(request):
	return render(request,'termcondition.html',{})
def promotion(request):
	return render(request,'promotion.html',{})