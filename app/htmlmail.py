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

def sendplanmail(to_email, plan, date, txnid, payid, amount):
    message = EmailMultiAlternatives(
        subject='Congratulations! New Plan subscribed - Stransmit',
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email]
    )
    message.mixed_subtype = 'related'
    message.attach_alternative(planhtml(plan, date, txnid, payid, amount), "text/html")
    message.send(fail_silently=False)

def planhtml(plan, date, txnid, payid, amount):
    if plan == 'PL003':
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
            <p style="line-height:30px;text-align:left;">
                Congratulation! You have successfully subscribed to<br>
                <span style="font-size:25px;font-weight:bold;color:#ffc800;">Premium Plan</span><br>
                Date & Time : <span style="font-weight:bold;">'''+date+'''</span><br>
                Transaction ID : <span style="font-weight:bold;">'''+txnid+'''</span><br>
                Payment ID : <span style="font-weight:bold;">'''+payid+'''</span><br>
                <span style="font-weight:bold;font-size:20px;">Total Amount Received</span><br>
                <span style="font-weight:bold;font-size:20px;">Rs '''+amount+'''/-</span><br>
                <span style="font-weight:bold;">Note : </span>Your plan is valid for next one month from today.<br>
                Thanks for being with us!<br>Team Stransmit
            </p>
        </div>

</body>
    
</html>'''
    else:
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
            <p style="line-height:30px;text-align:left;">
                Congratulation! You have successfully subscribed to<br>
                <span style="font-size:25px;font-weight:bold;color:#ff0000;">Basic Plan</span><br>
                Date & Time : <span style="font-weight:bold;">'''+date+'''</span><br>
                Transaction ID : <span style="font-weight:bold;">'''+txnid+'''</span><br>
                Payment ID : <span style="font-weight:bold;">'''+payid+'''</span><br>
                <span style="font-weight:bold;font-size:20px;">Total Amount Received</span><br>
                <span style="font-weight:bold;font-size:20px;">Rs '''+amount+'''/-</span><br>
                <span style="font-weight:bold;">Note : </span>Your plan is valid for next one month from today.<br>
                Thanks for being with us!<br>Team Stransmit
            </p>
        </div>

</body>
    
</html>'''
    return html

def sendpassmail(to_email, link):
    message = EmailMultiAlternatives(
        subject='Stransmit - Account Recovery',
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email]
    )
    message.mixed_subtype = 'related'
    message.attach_alternative(passhtml(link), "text/html")
    message.send(fail_silently=False)

def passhtml(link):
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
            <p style="line-height:30px;text-align:left;">Hi There!<br>We got a new request to change your password please click the below button</p><br>
            <a style="float:left;background-color:#03a9fc;color:white;padding:20px;border-radius:10px;text-decoration:none;"href="'''+link+'''">Change Password</a>
        </div>

</body>
    
</html>'''
    return html

def sendpromotion(to_email):
    message = EmailMultiAlternatives(
        subject='Share Your Files Globally for FREE Upto 5GB - Stransmit',
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email]
    )
    message.mixed_subtype = 'related'
    message.attach_alternative(promotionhtml(), "text/html")
    message.send(fail_silently=False)
    return 'Done'

def promotionhtml():
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
            <p style="line-height:30px;text-align:left;">Hi there!<br>

<span>Hope you are doing good!</span><br>

We are from <a style="text-decoration:none;font-weight:bold;"href="https://srd.mobi">SRD (Shreshtha Research & Development),</a> after the ban of wetransfer.com in India we are facing problems to transfer files. So, our team has launched a new tool <a style="text-decoration:none;font-weight:bold;"href="https://stransmit.com">Stransmit.com</a> from which you can files to anybody in the globe. Stransmit.com brings you the capability to send upto <a style="text-decoration:none;font-weight:bold;"href="https://stransmit.com">5 GB file at a time for FREE.</a> And you can send upto 2 TB files for in our paid versions.<br><br>

<a style="text-decoration:none;font-weight:bold;"href="https://stransmit.com">Use Stransmit.com</a> (Made in India Made for World)<br>

<a style="text-decoration:none;font-weight:bold;"href="https://stransmit.com/pricing/">Select The Most Affordable Plan Here</a><br>

<a style="text-decoration:none;font-weight:bold;"href="https://stransmit.com">START SHARING FOR FREE NOW!</a>

<br><br>
                Thanks!<br>Team Stransmit
            </p>
        </div>

</body>
    
</html>'''
    return html

def reviewhtml():
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
        <div style="padding:20px;text-align:left;">
            <h1>Your review matters.</h1>
            <p style="line-height:30px;text-align:left;">Hi there!<br>

Thanks for choosing us, hope you are doing good. Please help us to improve our services. Your review is important to us.<br><br>

<a href="https://docs.google.com/forms/d/e/1FAIpQLSesidNbc2dWO0X82_F7vzyiWkE_YRWDN8Ot4kgr9xwzirKfVQ/viewform?usp=sf_link" style="background-color:#03a9fc;color:white;padding:20px;border-radius:10px;text-decoration: none;margin-top:100px; ">Send Review</a>
<br><br>
Thanks!<br>Team <a href="https://www.stransmit.com" style="text-decoration:none;color:black;">Stransmit</a>
            </p>
        </div>

</body>
    
</html>'''
    return html
def sendreview(to_email):
    message = EmailMultiAlternatives(
        subject='Hey! Please help us to improve our services. - Stransmit',
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=to_email
    )
    message.mixed_subtype = 'related'
    message.attach_alternative(reviewhtml(), "text/html")
    message.send(fail_silently=False)
    return 'Done'