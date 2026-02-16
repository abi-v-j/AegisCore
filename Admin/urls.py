from django.urls import path
from Admin import views
app_name='Admin'
urlpatterns = [
    path('HomePage/',views.HomePage,name="HomePage"),
    path('District/',views.District,name="District"),
    path('deldistrict/<int:did>',views.deldistrict,name='deldistrict'),
    path('editdistrict/<int:eid>',views.editdistrict,name='editdistrict'),
    path('Category/',views.Category,name="Category"),
    path('delCategory/<int:did>',views.delCategory,name="delCategory"),
    path('editCategory/<int:eid>',views.editCategory,name='editCategory'),
    path('AdminRegistration/',views.AdminRegistration,name="AdminRegistration"),
    path('delAdminRegistration/<int:did>',views.delAdminRegistration,name="delAdminRegistration"),
    path('editAdminRegistration/<int:eid>',views.editAdminRegistration,name="editAdminRegistration"),
    path('Place/',views.Place,name="Place"),
    path('delplace/<int:did>',views.delplace,name='delplace'),
    path('editplace/<int:eid>',views.editplace,name='editplace'),
    path('Userlist/',views.Userlist,name="Userlist"),
    path('logout/',views.logout,name='logout'),


     # SIEM (AegisCore) inside Guest app
    path("dashboard/", views.siem_dashboard, name="siem_dashboard"),
    path("alerts/", views.siem_alerts, name="siem_alerts"),
    path("alerts/<int:alert_id>/ack/", views.siem_ack, name="siem_ack"),

    path("events-per-minute/", views.siem_events_per_minute_api, name="siem_events_per_minute_api"),
    path("top-ips/", views.siem_top_ips_api, name="siem_top_ips_api"),
    path("top-users/", views.siem_top_users_api, name="siem_top_users_api"),
]