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
               path('add_a_person/', views.add_a_person, name='add-person'),
               path('get_a_person/', views.get_a_person, name='retrieve-person'),
               path('delete_a_person/', views.delete_a_person, name='delete-person'),
               path('request_approval/', views.request_approval, name='request-approval'),
               path('update_person/', views.update_person, name='update-person'),

               ]
