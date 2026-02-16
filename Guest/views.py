from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from Guest.models import *
from .services import log_event
from .models import SecurityAlert, SecurityEvent
from django.db.models import Count
from django.http import JsonResponse
from datetime import timedelta
from django.db.models.functions import TruncMinute


def index(request):
    return render(request, 'Guest/index.html')


def Userregistration(request):
    disdata = tbl_district.objects.all()

    if request.method == 'POST':
        name = request.POST.get('text_name')
        email = request.POST.get('text_email')
        contact = request.POST.get('text_number')
        address = request.POST.get('text_address')
        gender = request.POST.get('gender')
        dob = request.POST.get('txt_dob')
        place = tbl_place.objects.get(id=request.POST.get('sel_place'))
        photo = request.FILES.get('file_photo')
        password = request.POST.get('text_password')

        tbl_user.objects.create(
            user_name=name,
            user_email=email,
            user_contact=contact,
            user_address=address,
            user_gender=gender,
            user_dob=dob,
            user_photo=photo,
            user_password=password,
            place=place
        )

        return render(request, 'Guest/Userregistration.html', {'dis': disdata})

    return render(request, 'Guest/Userregistration.html', {'dis': disdata})


def Ajaxplace(request):
    districtid = tbl_district.objects.get(id=request.GET.get('did'))
    placedata = tbl_place.objects.filter(district=districtid)
    return render(request, 'Guest/AjaxPlace.html', {'plc': placedata})


# ==========================
# LOGIN WITH SIEM LOGGING
# ==========================
def Login(request):
    if request.method == 'POST':
        email = request.POST.get('text_email', '').strip()
        password = request.POST.get('text_password', '')

        # log attempt
        log_event(
            event_type="LOGIN_ATTEMPT",
            request=request,
            actor=email,
            outcome="ATTEMPT",
            severity=2,
            details={"module": "Guest.Login"},
        )

        adminCount = tbl_adminregistration.objects.filter(
            adminregistration_email=email,
            adminregistration_password=password
        ).count()

        userCount = tbl_user.objects.filter(
            user_email=email,
            user_password=password
        ).count()

        if adminCount > 0:
            admindata = tbl_adminregistration.objects.get(
                adminregistration_email=email,
                adminregistration_password=password
            )
            request.session['aid'] = admindata.id

            log_event(
                event_type="LOGIN_SUCCESS",
                request=request,
                actor=email,
                outcome="SUCCESS",
                severity=1,
                details={"role": "admin", "admin_id": admindata.id},
            )
            return redirect('Admin:HomePage')

        elif userCount > 0:
            userdata = tbl_user.objects.get(user_email=email, user_password=password)
            request.session['uid'] = userdata.id

            log_event(
                event_type="LOGIN_SUCCESS",
                request=request,
                actor=email,
                outcome="SUCCESS",
                severity=1,
                details={"role": "user", "user_id": userdata.id},
            )
            return redirect('User:HomePage')

        else:
            # log failure (triggers rule 5 in 60s)
            log_event(
                event_type="LOGIN_FAILURE",
                request=request,
                actor=email,
                outcome="FAILURE",
                severity=4,
                details={"reason": "invalid_credentials"},
            )
            return render(request, 'Guest/Login.html', {"msg": "Invalid email or password"})

    return render(request, 'Guest/Login.html')

