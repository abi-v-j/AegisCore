from django.shortcuts import render, redirect
from Guest.models import *
# Create your views here.
def HomePage(request):
    if 'uid' not in request.session:
        return redirect("Guest:Login")
    else:
        return render(request,'User/Homepage.html')

def Myprofile(request):
    if 'uid' not in request.session:
        return redirect("Guest:Login")
    else:
        user=tbl_user.objects.get(id=request.session['uid'])
        return render(request,'User/Myprofile.html',{'user':user})

def EditProfile(request):
    if 'uid' not in request.session:
        return redirect("Guest:Login")
    else:
        editdata=tbl_user.objects.get(id=request.session['uid'])
        if request.method=='POST':
            name=request.POST.get('txt_num1')  
            email=request.POST.get('txt_num2')
            contact=request.POST.get('txt_num3')
            address=request.POST.get('txt_num4')
            editdata.user_name=name
            editdata.user_email=email
            editdata.user_contact=contact
            editdata.user_address=address
            editdata.save()
            return render(request,'User/EditProfile.html',{'msg':'Updated'}) 
        else:
            return render(request,'User/EditProfile.html',{'editdata':editdata}) 

def changepassword(request):
    if 'uid' not in request.session:
        return redirect("Guest:Login")
    else:
        editdata=tbl_user.objects.get(id=request.session['uid'])
        dbpass=editdata.user_password
        if request.method=='POST':
            old=request.POST.get('txt_num1')  
            new=request.POST.get('txt_num2')
            cpass=request.POST.get('txt_num3')
            if dbpass==old:
                if new == cpass:
                    editdata.user_password=new
                    editdata.save()
                    return render(request,'User/Myprofile.html',{'msg':"Password Updated"})
                else:
                    return render(request,'User/changepassword.html',{'msg':"Password Does Not Match"})
            else:
                return render(request,'User/changepassword.html',{'msg':"Incorrect Current Password"})
        else:
            return render(request,'User/changepassword.html')
    
def logout(request):
    del request.session['uid']
    return redirect("Guest:Login")