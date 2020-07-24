from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
from functools import lru_cache
import mimetypes

def bodyhtml(link, subject, message, email):
	html='''<!doctype html>
<html class="no-js" lang="zxx">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body style="text-align:center;">

        <div style="background-color:black;padding:20px;">
            <img src="https://stransmit.com/static/Stransmit.png" style="width:200px;">
        </div>
        <div style="padding:20px;">
            <span style="font-size:20px;font-weight:bold;">Message from '''+str(email)+'''</span><br>
            <span style="font-size:20px;font-weight:bold;">'''+str(subject)+'''</span>
            <p style="margin-top:20px;margin-bottom:30px;">'''+str(message)+'''</p>
            <a href="'''+str(link)+'''" style="background-color:#03a9fc;color:white;padding:20px;border-radius:10px;text-decoration: none; ">Download Media</a>
        </div>

</body>
    
</html>'''
	return html

def sendemail(subject, message2, to_email, from_email, link):
	message = EmailMultiAlternatives(
    	subject=subject+' - '+from_email,
    	body='',
    	from_email=settings.EMAIL_HOST_USER,
    	to=[to_email]
	)
	message.mixed_subtype = 'related'
	message.attach_alternative(bodyhtml(link, subject, message2, from_email), "text/html")
	message.send(fail_silently=False)

def sendforgotpassword(password, to_email):
    message = EmailMultiAlternatives(
        subject='Stransmit - Account Recovery',
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email]
    )
    message.mixed_subtype = 'related'
    message.attach_alternative(passwordhtml(to_email, password), "text/html")
    message.send(fail_silently=False)

def passwordhtml(to_email, password):
    html='''<!doctype html>
<html class="no-js" lang="zxx">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body style="text-align:center;">

        <div style="background-color:black;padding:20px;">
            <img src="https://stransmit.com/static/Stransmit.png" style="width:200px;">
        </div>
        <div style="padding:20px;">
            <p style="text-align:left;line-height:30px;">Hi There!<br>Your Password for the Account '''+to_email+'''<br>
                <span style="font-size:25px;font-weight:bold;">'''+password+'''</span><br>
                Thanks for being with us!<br>Team <a href="https://stransmit.com" style="text-decoration:none;">Stransmit</a>
            </p>
        </div>

</body>
    
</html>'''
    return html

def sendotp(otp, to_email):
    message = EmailMultiAlternatives(
        subject='Stransmit - Account Verification Email',
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email]
    )
    message.mixed_subtype = 'related'
    message.attach_alternative(otphtml(to_email, otp), "text/html")
    message.send(fail_silently=False)

def otphtml(to_email, otp):
    html='''<!doctype html>
<html class="no-js" lang="zxx">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body style="text-align:center;">

        <div style="background-color:black;padding:20px;">
            <img src="https://stransmit.com/static/Stransmit.png" style="width:200px;">
        </div>
        <div style="padding:20px;">
            <p style="text-align:left;line-height:30px;">Hi There!<br>Your One Time Password (OTP) for account verification of '''+to_email+''' is,<br>
                <span style="font-size:25px;font-weight:bold;">'''+otp+'''</span><br>
                Thanks for being with us!<br>Team <a href="https://stransmit.com" style="text-decoration:none;">Stransmit</a>
            </p>
        </div>

</body>
    
</html>'''
    return html

def sendaccountdetails(to_email, password):
    message = EmailMultiAlternatives(
        subject='Stransmit - Account Credentials',
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email]
    )
    message.mixed_subtype = 'related'
    message.attach_alternative(accounthtml(to_email, password), "text/html")
    message.send(fail_silently=False)

def accounthtml(to_email, password):
    html='''<!doctype html>
<html class="no-js" lang="zxx">
<head>
    <meta charset="utf-8">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>

<body style="text-align:center;">

        <div style="background-color:black;padding:20px;">
            <img src="https://stransmit.com/static/Stransmit.png" style="width:200px;">
        </div>
        <div style="padding:20px;">
            <p style="text-align:left;line-height:30px;">Congratulations! <br>Thanks for creating your Account on stransmit.com. Send 50GB free mails per month with our free plans and you can also send upto 2TB mails per month with our paid plans. Check our plans <a href="https://stransmit.com/pricing/" style="text-decoration:none;">Click here.</a><br><span style="font-weight:bold;">Your account credential are as follows,</span><br>
            <span style="font-size:18px;font-weight:bold;">User Email: '''+to_email+'''</span><br>
            <span style="font-size:18px;font-weight:bold;">User Password: '''+password+'''</span><br>  
                Thanks for being with us!<br>Team <a href="https://stransmit.com" style="text-decoration:none;">Stransmit</a>
            </p>
        </div>

</body>
    
</html>'''
    return html