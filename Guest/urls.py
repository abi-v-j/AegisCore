from django.urls import path
from Guest import views

app_name = 'Guest'

urlpatterns = [
    path('', views.index, name="index"),
    path('Userregistration/', views.Userregistration, name="Userregistration"),
    path('Ajaxplace/', views.Ajaxplace, name="Ajaxplace"),
    path('Login/', views.Login, name="Login"),

   

]
