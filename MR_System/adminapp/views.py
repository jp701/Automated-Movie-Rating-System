from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect , HttpResponse
from registerapp.models import Movie
# Create your views here.
import datetime
import requests
import json

def admin_home(request):
    #c = {}
    #c.update(csrf(request))
    l1=[60,60,60,60,60]
    l2=[100,50,150,20,200]
    l3=[10,20,30,40,50]
    l=[l1,l2,l3]
    l=json.dumps(l)
    movielist = ['Overall','Movie1' , 'Movie2']
    movielist = json.dumps(movielist)
    #mlist = ["overall"]
    return render(request,'admin_home.html',{'chartData':l,"movielist":movielist})

def addmovie(request):
    name=request.POST.get('name','')
    releasedDate=request.POST.get('releaseddate','')
    production=request.POST.get('production','')
    duration=request.POST.get('duration','')
    plot=request.POST.get('plot')
    imagefile=request.FILES['image']

    new_movie = Movie(name=name,releasedDate=releasedDate,production=production,duration=duration,plot=plot,image=imagefile,rating=0)
    new_movie.save()
    return render(request,'addmovie.html',{'status':'Movie added'})

def showmovies(request):
    movies = Movie.objects.all()
    if movies.exists():
        return render(request,'showmovies.html',{'movielist':movies,'nomovie':False})
    else:
        return render(request,'showmovies.html',{'movielist':movies,'nomovie':True})

def showmovie(request):
    update = False
    up = request.GET.get('update','')
    if up == "":
        update = False
        id=request.POST.get('movieid','')
        if id == "":
            return HttpResponse("Not found Movieid")
        movie = Movie.objects.get(ID=id)
    else:
        update = True
        movie = Movie.objects.get(ID=up)
    movie.releasedDate = datetime.date.strftime(movie.releasedDate, "%Y-%m-%d")
    movie.duration = datetime.time.strftime(movie.duration,"%H:%M")
    return render(request,'showmovie.html',{'movie':movie,'update':update})

def updatemovie(request):
    id=request.POST.get('updateconfirm','')

    name=request.POST.get('name','')
    releasedDate=request.POST.get('releaseddate','')
    production=request.POST.get('production','')
    duration=request.POST.get('duration','')
    plot=request.POST.get('plot','')    

    #m.update(name=name,releasedDate=releasedDate,production=production,duration=duration,plot=plot,image=imagefile)

    m=Movie.objects.get(ID=id)
    if len(request.FILES) != 0 :
        imagefile=request.FILES['image']
        m.image.delete(save=True)
        m.image = imagefile
    m.name= name
    m.releasedDate = releasedDate
    m.production = production
    m.duration=duration
    m.plot = plot
    m.save()

    movie = Movie.objects.get(ID=id)
    movie.releasedDate = datetime.date.strftime(movie.releasedDate, "%Y-%m-%d")
    movie.duration = datetime.time.strftime(movie.duration,"%H:%M")
    
    return render(request,'showmovie.html',{'movie':movie,'update':False})

def deletemovie(request):
    id = request.POST.get('movieid','')
    m= Movie.objects.filter(ID=id)
    if m.exists():
        m.delete()
    return HttpResponseRedirect('/administrator/showmovies/')

