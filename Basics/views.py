from django.shortcuts import render

# Create your views here.
def Sum(request):
    if request.method=='POST':
        num1=int(request.POST.get('txt_num1'))
        num2=int(request.POST.get('txt_num2'))
        sum=num1+num2
        return render(request,'Basics/Sum.html',{'res':sum})
    else:
        return render(request,'Basics/Sum.html')

def Data(request):
    return render(request,'Basics/Data.html')

def Sub(request):
    if request.method=='POST':
        num1=int(request.POST.get('txt_num1'))
        num2=int(request.POST.get('txt_num2'))
        substract=num1-num2 
        return render(request,'Basics/substract.html',{'res':substract})  
    else:
        return render(request,'Basics/substract.html')  

def large(request):
    if request.method=='POST':
        num1=int(request.POST.get('txt_num1'))
        num2=int(request.POST.get('txt_num2'))
        if num1>num2:
            largest=num1
        else:
            largest=num2
        return render(request,'Basics/largest.html',{'res':largest})
    else:
        return render(request,'Basics/largest.html') 

def Calculator(request):
    if request.method=='POST':
        num1=int(request.POST.get('txt_num1'))
        num2=int(request.POST.get('txt_num2'))
        op=request.POST.get('btn')
        if op == '+':
            result=num1+num2
        elif op == '-':
            result=num1-num2
        elif op== '*':
            result=num1*num2
        elif op== '/':
            result=num1/num2 
        return render(request,'Basics/Calculator.html',{'res':result})
        
    else:        
        return render(request,'Basics/Calculator.html') 


         
