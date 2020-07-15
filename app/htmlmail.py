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

@lru_cache()
def logo_data():
	with open('app/static/Stransmit.png', 'rb') as f:
		logo_data = f.read()
	logo = MIMEImage(logo_data)
	logo.add_header('Content-ID', '<logo>')
	return logo