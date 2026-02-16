from django.shortcuts import render,redirect
from Admin.models import *
from Guest.models import *

from Guest.services import log_event
from django.db.models import Count
from django.http import JsonResponse
from datetime import timedelta
from django.db.models.functions import TruncMinute
# Create your views here.
def District(request):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        #select qry
        districtData=tbl_district.objects.all()
        if request.method=='POST':
            name=request.POST.get('text_name')
            #ins qry
            tbl_district.objects.create(district_name=name)
            return render(request,'Admin/District.html',{'msg':'Inserted'})
        else:
            return render(request,'Admin/District.html',{'districtData':districtData})
    

def HomePage(request):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        return render(request,'Admin/HomePage.html')


def deldistrict(request,did):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        tbl_district.objects.get(id=did).delete()
        return render(request,'Admin/District.html')

def editdistrict(request,eid):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        editdata=tbl_district.objects.get(id=eid)
        if request.method=='POST':
            name=request.POST.get('text_name')  
            editdata.district_name=name
            editdata.save()
            return render(request,'Admin/District.html',{'msg':'Updated'}) 
        else:
            return render(request,'Admin/District.html',{'editdata':editdata}) 

def Category(request):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        CategoryData=tbl_category.objects.all()
        if request.method=='POST':
            name=request.POST.get('text_name')
            tbl_category.objects.create(category_name=name)
            return render(request,'Admin/Category.html',{'msg':'Inserted'})
        else:
            return render(request,'Admin/Category.html',{'CategoryData':CategoryData})
def delCategory(request,did):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        tbl_category.objects.get(id=did).delete()
        return render(request,'Admin/Category.html',{'msg':'Delete'})  

def editCategory(request,eid):  
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        editdata=tbl_category.objects.get(id=eid)
        if request.method=='POST':
            name=request.POST.get('text_name')
            editdata.category_name=name
            editdata.save()
            return render(request,'Admin/Category.html',{'msg':'Updated'})  
        else:
                return render(request,'Admin/Category.html',{'editdata':editdata})
             



def AdminRegistration(request):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        admin=tbl_adminregistration.objects.all()
        if request.method=='POST':
            name=request.POST.get('text_name')
            email=request.POST.get('text_email')
            password=request.POST.get('text_password')
            tbl_adminregistration.objects.create(adminregistration_name=name,adminregistration_email=email,adminregistration_password=password)
            return render(request,'Admin/AdminRegistration.html',{'msg':'Inserted'})
        else:
            return render(request,'Admin/AdminRegistration.html',{'admindata':admin})

def delAdminRegistration(request,did):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        tbl_adminregistration.objects.get(id=did).delete()
        return render(request,'Admin/AdminRegistration.html',{'msg':'Deleted'}) 

def editAdminRegistration(request,eid):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        editdata=tbl_adminregistration.objects.get(id=eid)
        if request.method=='POST':
            name=request.POST.get('text_name')
            email=request.POST.get('text_email')
            password=request.POST.get('text_password')
            editdata.adminregistration_name=name
            editdata.adminregistration_email=email
            editdata.adminregistration_password=password
            editdata.save()
            return render(request,'Admin/AdminRegistration.html',{'msg':'Updated'}) 
        else:
            return render(request,'Admin/AdminRegistration.html',{'editdata':editdata})
def Place(request):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        place=tbl_place.objects.all()
        dis=tbl_district.objects.all()
        if request.method=='POST':
            name=request.POST.get('text_name') 
            districtid=tbl_district.objects.get(id=request.POST.get('selname'))
            tbl_place.objects.create(place_name=name,district=districtid)
            return render(request,'Admin:place.html',{'msg':'Inserted'})
        else:
            return render(request,'Admin/Place.html',{'district':dis,'place':place})

def delplace(request,did):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        tbl_place.objects.get(id=did).delete()
        return render(request,'Admin/place.html',{'msg':'Deleted'})

def editplace(request,eid):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        dis=tbl_district.objects.all()
        editdata=tbl_place.objects.get(id=eid)
        if request.method=='POST':
            name=request.POST.get('text_name')
            districtid=tbl_district.objects.get(id=request.POST.get('selname'))
            editdata.place_name=name
            editdata.district=districtid
            editdata.save()
            return render(request,'Admin/Place.html',{'msg':'Updated'})  
        else:
            return render(request,'Admin/Place.html',{'editdata':editdata,'district':dis})
    
def Userlist(request):
    if 'aid' not in request.session:
        return redirect("Guest:Login")
    else:
        Userlist=tbl_user.objects.all()
        return render(request, 'Admin/Userlist.html',{'Userlist':Userlist})
            
def logout(request):
    del request.session['aid']
    return redirect("Guest:Login")





# ==========================
# ALERT PAGES
# ==========================
def siem_dashboard(request):
    total_events = SecurityEvent.objects.count()
    total_alerts = SecurityAlert.objects.count()
    open_alerts = SecurityAlert.objects.filter(status="OPEN").count()

    return render(request, "Admin/siem_dashboard.html", {
        "total_events": total_events,
        "total_alerts": total_alerts,
        "open_alerts": open_alerts,
    })


def siem_alerts(request):
    alerts = SecurityAlert.objects.all().order_by("-created_at")[:200]
    return render(request, "Admin/siem_alerts.html", {"alerts": alerts})


def siem_ack(request, alert_id):
    alert = get_object_or_404(SecurityAlert, id=alert_id)

    if request.method == "POST":
        note = request.POST.get("note", "").strip()
        alert.status = "ACK"
        alert.acknowledged_at = timezone.now()
        alert.ack_note = note
        alert.save()
        return redirect("Admin:siem_alerts")

    return render(request, "Admin/siem_ack.html", {"alert": alert})


def siem_dashboard(request):
    total_events = SecurityEvent.objects.count()
    total_alerts = SecurityAlert.objects.count()
    open_alerts = SecurityAlert.objects.filter(status="OPEN").count()

    # last 60 minutes default summary
    minutes = 60
    since = timezone.now() - timedelta(minutes=minutes)

    top_ips = (SecurityEvent.objects
               .filter(event_type="LOGIN_FAILURE", ts__gte=since)
               .values("src_ip")
               .annotate(total=Count("id"))
               .order_by("-total")[:10])

    top_users = (SecurityEvent.objects
                 .filter(event_type="LOGIN_FAILURE", ts__gte=since)
                 .exclude(actor="")
                 .values("actor")
                 .annotate(total=Count("id"))
                 .order_by("-total")[:10])

    return render(request, "Admin/siem_dashboard.html", {
        "total_events": total_events,
        "total_alerts": total_alerts,
        "open_alerts": open_alerts,
        "top_ips": top_ips,
        "top_users": top_users,
        "minutes": minutes,
    })


def siem_events_per_minute_api(request):
    """
    JSON for Chart.js
    /Guest/siem/events-per-minute/?minutes=60
    """
    minutes = int(request.GET.get("minutes", 60))
    minutes = max(5, min(minutes, 24 * 60))  # clamp 5..1440

    since = timezone.now() - timedelta(minutes=minutes)

    # group by minute
    rows = (SecurityEvent.objects
            .filter(ts__gte=since)
            .annotate(minute=TruncMinute("ts"))
            .values("minute")
            .annotate(total=Count("id"))
            .order_by("minute"))

    labels = []
    values = []
    for r in rows:
        # format label "HH:MM"
        labels.append(r["minute"].strftime("%H:%M"))
        values.append(r["total"])

    return JsonResponse({"labels": labels, "values": values})


def siem_top_ips_api(request):
    """
    JSON for Top IPs
    /Guest/siem/top-ips/?minutes=60
    """
    minutes = int(request.GET.get("minutes", 60))
    minutes = max(5, min(minutes, 24 * 60))
    since = timezone.now() - timedelta(minutes=minutes)

    rows = (SecurityEvent.objects
            .filter(event_type="LOGIN_FAILURE", ts__gte=since)
            .values("src_ip")
            .annotate(total=Count("id"))
            .order_by("-total")[:10])

    return JsonResponse({"data": list(rows)})


def siem_top_users_api(request):
    """
    JSON for Top Usernames attacked
    /Guest/siem/top-users/?minutes=60
    """
    minutes = int(request.GET.get("minutes", 60))
    minutes = max(5, min(minutes, 24 * 60))
    since = timezone.now() - timedelta(minutes=minutes)

    rows = (SecurityEvent.objects
            .filter(event_type="LOGIN_FAILURE", ts__gte=since)
            .exclude(actor="")
            .values("actor")
            .annotate(total=Count("id"))
            .order_by("-total")[:10])

    return JsonResponse({"data": list(rows)})
