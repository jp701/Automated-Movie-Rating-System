from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect , HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from userapp.models import Movie,Review,User
# Create your views here.
import datetime
import requests
import json

#MAX_USER = 10

def admin_home(request):
    datalist = []
    movies = Movie.objects.all()
    movielist=[]
    for movie in movies:
        movielist.append(movie.name)
        review_1 = Review.objects.filter(rating=1,mid=movie).count()
        review_2 = Review.objects.filter(rating=2,mid=movie).count()
        review_3 = Review.objects.filter(rating=3,mid=movie).count()
        review_4 = Review.objects.filter(rating=4,mid=movie).count()
        review_5 = Review.objects.filter(rating=5,mid=movie).count()
        ratinglist = []
        ratinglist.append(review_1)
        ratinglist.append(review_2)
        ratinglist.append(review_3)
        ratinglist.append(review_4)
        ratinglist.append(review_5)
        datalist.append(ratinglist)

    movielist = json.dumps(movielist)
    datalist=json.dumps(datalist)

    overallData = []
    nreview = []
    avrating = []
    mname = []
    movies = Movie.objects.filter()
    MAX_USER = User.objects.all().count()
    for each in movies:
        no_of_reviews = Review.objects.filter(mid=each).count()
        no_of_reviews = (no_of_reviews*100)/MAX_USER
        movie_name = each.name
        avg_rating = each.rating
        nreview.append(no_of_reviews)
        avrating.append(avg_rating)
        mname.append(movie_name)

    nreview = json.dumps(nreview)
    avrating = json.dumps(avrating)
    mname = json.dumps(mname)
    overallData.append(nreview)
    overallData.append(avrating)
    overallData.append(mname)
    overallData = json.dumps(overallData)


    movie = Movie.objects.all().order_by("ID")
    review_1 = Review.objects.filter(rating=1,mid=movie[:1]).count()
    review_2 = Review.objects.filter(rating=2,mid=movie[:1]).count()
    review_3 = Review.objects.filter(rating=3,mid=movie[:1]).count()
    review_4 = Review.objects.filter(rating=4,mid=movie[:1]).count()
    review_5 = Review.objects.filter(rating=5,mid=movie[:1]).count()
    firstratinglist = []
    firstdatalist = []
    firstratinglist.append(review_1)
    firstratinglist.append(review_2)
    firstratinglist.append(review_3)
    firstratinglist.append(review_4)
    firstratinglist.append(review_5)
    firstdatalist.append(firstratinglist)

    firstmoviename = movie[:1].get().name
    firstmoviename = json.dumps(firstmoviename)
    firstdatalist = json.dumps(firstdatalist)
    #mlist = ["overall"]
    return render(request,'admin_home.html',{'chartData':datalist,"movielist":movielist,"firstmoviename":firstmoviename,"firstdatalist":firstdatalist,'overallData':overallData})

def alogout(request):
    try:
        del request.session["admin"]
    except KeyError:
        pass
    return HttpResponseRedirect('/login')

def addmovie(request):
    if 'admin' in request.session:
        name=request.POST.get('name','')
        releasedDate=request.POST.get('releaseddate','')
        production=request.POST.get('production','')
        duration=request.POST.get('duration','')
        plot=request.POST.get('plot')
        imagefile=request.FILES['image']

        new_movie = Movie(name=name,releasedDate=releasedDate,production=production,duration=duration,plot=plot,image=imagefile,rating=0)
        new_movie.save()
        movie = Movie.objects.all().last()
        return render(request,'addmovie.html',{'status':'Movie added','mid':movie.ID}) #to retrieve the latest movie added
    else:
        return HttpResponseRedirect('/login')

def showmovies(request):
    if 'admin' in request.session:
        star= request.GET.get('star','') 
        movies = Movie.objects.all().order_by('-ID')
        if star != "":
                movies = Movie.objects.filter(rating__range=(float(star)-0.9,float(star))).order_by('-rating')
        if movies.exists():
            return render(request,'showmovies.html',{'movielist':movies,'nomovie':False})
        else:
            return render(request,'showmovies.html',{'movielist':movies,'nomovie':True})
    else:
        return HttpResponseRedirect('/login')

def showmovie(request):
    if 'admin' in request.session:
        update = False
        up = request.GET.get('update','')
        sortby = request.GET.get('star','')
        sortedReviews = None

        if up == "":
            update = False
            id=request.GET.get('movieid','')
            if id == "":
                return HttpResponse("Not Found Movieid")
            try:
                movie = Movie.objects.get(ID=id)
            except ObjectDoesNotExist:
                return HttpResponse("Not Found Movieid")
            if sortby != '':
                reviews= Review.objects.filter(mid=id, rating= sortby)
            else:
                reviews = Review.objects.filter(mid=id)
            sortedReviews = sorted(
                reviews,
                key=lambda x: x.dateTime, reverse=True
            )
        else:
            update = True
            movie = Movie.objects.get(ID=up)
        movie.releasedDate = datetime.date.strftime(movie.releasedDate, "%Y-%m-%d")
        movie.duration = datetime.time.strftime(movie.duration,"%H:%M")
        return render(request,'ashowmovie.html',{'movie':movie,'update':update,'reviews':sortedReviews})
    else:
        return HttpResponseRedirect('/login')

def updatemovie(request):
    if 'admin' in request.session:
        id=request.POST.get('updateconfirm','')

        name=request.POST.get('name','')
        releasedDate=request.POST.get('releaseddate','')
        production=request.POST.get('production','')
        duration=request.POST.get('duration','')
        plot=request.POST.get('plot','')    

        #m.update(name=name,releasedDate=releasedDate,production=production,duration=duration,plot=plot,image=imagefile)

        m= Movie.objects.get(ID=id)
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
        
        return render(request,'ashowmovie.html',{'movie':movie,'update':False})
    else:
        return HttpResponseRedirect('/login')

def deletemovie(request):
    if 'admin' in request.session:
        id = request.POST.get('movieid','')
        m= Movie.objects.filter(ID=id)
        if m.exists():
            m.delete()
        return HttpResponseRedirect('/administrator/showmovies/')
    else:
        return HttpResponseRedirect('/login/')
