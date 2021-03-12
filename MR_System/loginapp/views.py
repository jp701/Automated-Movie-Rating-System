from django.shortcuts import render
from registerapp.models import User
from django.template.context_processors import csrf
from django.http import request
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect,HttpResponse

# Create your views here.
user= None


def dologin(request):
    c={}
    c.update(csrf(request))
    return render(request,'login.html',c)

def login(request):
    c={}
    c.update(csrf(request))
    email = request.POST.get('email','')
    passwd = request.POST.get('pwd','')
    try:
        getuser = User.objects.get(email=email, password=passwd)
        request.session["customer"]=getuser.ID
        
        return HttpResponseRedirect('/user/user_home_initial/')
    except ObjectDoesNotExist:
        msg= "Incorrect email or password"
        return render(request,'login.html',{'c':c, 'msg':msg})

def forgotpass(request):
    c={}
    c.update(csrf(request))
    return render(request,'forgotpassword.html',c)
    
def testit(request):
    email=request.POST.get('email','')
    global user
    user=User.objects.filter(email=email)
    if user.exists():
        user=user[:1].get()
        subject='Please reset your password'
        email_from=settings.EMAIL_HOST_USER
        email_to=user.email
        content='Click below link to reset your password\n'+'http://127.0.0.1:8000/login/gotoresetlink/'
        list=[]
        list.append(email_to)
        send_mail(subject,content,email_from,list)
        return render(request,'forgotpassword.html',{'check':'We have mailed you password reset link, check your email.'})
    else:
        return render(request,'forgotpassword.html',{'msg':'Sorry! Account doesn\'t exists, try another email address'})


def gotoresetlink(request):
    c={}
    c.update(csrf(request))
    global user
    return render(request,'resetpassword.html',{'c':c,'user':user})

def resetpassword(request):
    c={}
    c.update(csrf(request))
    Id= request.POST.get('uid','')
    email=request.POST.get('email','')
    password=request.POST.get('password','')
    cpasswd=request.POST.get('cpassword','')
    if password==cpasswd:
        getuser= User.objects.get(ID= int(Id))
        getuser.password = password
        getuser.save()
        #getuser.update(email=email,password=password)
        user1= User.objects.filter(email=email,password=password)
        return render(request,'resetpassword.html',{'c':c,'user1':user1[:1].get()})
    else:
        global user
        return render(request,'resetpassword.html',{'c':c,'msg':'Password does not match, Try again','user':user})