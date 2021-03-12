from django.shortcuts import render
from userapp.models import User
from django.template.context_processors import csrf
from django.http import request,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.core.mail import send_mail
import random,string

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
        request.session['user'] = getuser.ID
        msg = "Login successful.."
        return HttpResponseRedirect('/user/')
    except ObjectDoesNotExist:
        if email=="admin@gmail.com" and passwd=='admin':
            request.session["admin"] = "admin"
            return HttpResponseRedirect('/administrator/admin_home')
        msg= "Incorrect email or password"
    return render(request,'login.html',{'c':c, 'msg':msg})

def logout(request):
    if 'user' in request.session:
        del request.session['user']
        request.session.modified=True
        c={}
        c.update(csrf(request))
        msg='You are logged out, Please login again...'
        return render(request,'login.html',{'c':c,'msg':msg})
    else:
        return HttpResponseRedirect('/login/')

def forgotpass(request):
    c={}
    c.update(csrf(request))
    return render(request,'forgotpassword.html',c)

#import random,string to generate random character sequence
def randomSequence(len):
    seq =string.ascii_letters+ string.digits
    return ''.join(random.choice(seq) for i in range(len))

def testit(request):
    email=request.POST.get('email','')
    global user
    user=User.objects.filter(email=email)
    if user.exists():
        user=user[:1].get()
        subject='Please reset your password'
        email_from=settings.EMAIL_HOST_USER
        email_to=user.email
        randStr = randomSequence(10)
        content='Click below link to reset your password\n'+'http://127.0.0.1:8000/login/gotoresetlink?seq='+randStr
        list=[]
        list.append(email_to)
        send_mail(subject,content,email_from,list)
        return render(request,'forgotpassword.html',{'check':'We have mailed you password reset link, check your email.'})
    else:
        return render(request,'forgotpassword.html',{'msg':'Sorry! Account doesn\'t exists, try another email address'})

# Redirect back to login page if querystring parameter seq doesn't exist
def gotoresetlink(request):
    seq = request.GET.get('seq','')
    if seq:
        c={}
        c.update(csrf(request))
        global user
        return render(request,'resetpassword.html',{'c':c,'user':user})
    else:
        return HttpResponseRedirect("/login/")

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