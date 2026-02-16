from django.urls import path
from User import views
app_name='User'
urlpatterns = [
    path('HomePage/',views.HomePage,name='HomePage'),
    path('Myprofile/',views.Myprofile,name='Myprofile'),
    path('EditProfile/',views.EditProfile,name='EditProfile'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('logout/',views.logout,name='logout'),
    ]