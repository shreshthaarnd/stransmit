from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request,'index.html',{})
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
	return render(request,'userdashboard.html',{})