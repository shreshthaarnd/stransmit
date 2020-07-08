from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',index),
    path('blog/',blog),
    path('contact/',contact),
    path('elements/',elements),
    path('features/',features),
    path('pricing/',pricing),
    path('singleblog/',singleblog),
    path('adminlogin/',adminlogin),
    path('adminindex/',adminindex),
    path('registration/',registration),
    path('userdashboard/',userdashboard),
    path('sendmail/',sendmail),
    path('verify/',verify),
    path('resendotp/',resendotp),
    path('downloadmedia/',downloadmedia),
    path('checkmediadel/',checkmediadel),
    path('checklogin/',checklogin),
    path('edituserdata/',edituserdata),
    path('usersendmail/',usersendmail),
    path('sendbulkmails/',sendbulkmails),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)