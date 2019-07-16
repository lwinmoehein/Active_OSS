"""sun_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
    """
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url,include
from polls import views

urlpatterns = [
               path('polls/', include('polls.urls')),
               path('get_a_person/', views.get_a_person, name='retrieve-person'),
               path('delete_a_person/', views.delete_a_person, name='delete-person'),
               path('request_approval/', views.request_approval, name='request-approval'),
               path('update_person/', views.update_person, name='update-person'),
         #      path('write_pdf_view/', views.write_pdf_view, name='write-pdf-view'),
               path('data_visualization/', views.data_visualization, name='data-visualization'),
               path('homepage/', views.homepage, name='homepage'),
               path('add_person/', views.add_person, name='add_person'),
               path('register_crime_record/', views.register_crime_record, name='register-crime-record'),
               path('request_crime_record/', views.request_crime_record, name='request_crime_record'),

               ]
