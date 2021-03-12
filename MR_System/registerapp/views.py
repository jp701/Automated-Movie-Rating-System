from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from registerapp.models import User

# Create your views here.
def doreg(request):
    c={}
    c.update(csrf(request))
    return render(request,'register.html',c)

def register(request):
    uname = request.POST.get('username','')
    passwd = request.POST.get('password','')
    email = request.POST.get('email','')

    user = User.objects.filter(email= email)
    if user.exists():
        msg= "You are already registered.."
        c={}
        return render(request,'register.html',{'c':c.update(csrf(request)),'msg':msg})
    else:
        user= User(name=uname, password=passwd, email=email)
        user.save()
        #msg= "You are now registered.."
        return HttpResponseRedirect("/login/")
    