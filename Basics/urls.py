from django.urls import path
from Basics import views
from Basics import views

urlpatterns = [
    path('Sum/',views.Sum,name="Sum"),
    path('Sub/',views.Sub,name="Sub"),
    path('Data/',views.Data,name="Data"),
    path('large/',views.large,name="large"),
    path('Calculator/',views.Calculator,name="Calculator")
]