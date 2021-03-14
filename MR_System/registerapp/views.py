from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from userapp.models import User,Movie

# Create your views here.
def index(request):
    c={}
    c.update(csrf(request))
    movie = Movie.objects.all().order_by('-ID')[:5]
    if movie.exists():
        counts = movie.count()
        count = []
        for i in range(counts):
            count.append(i)
        return render(request,'index.html',{'c':c,'movie':movie,'count':count,'countlen':counts})
    return render(request,'index.html',{'c':c})

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
    