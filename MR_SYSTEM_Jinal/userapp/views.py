from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .models import Review,Movie,User
from datetime import datetime
import numpy as np
import pandas as pd 
import preprocess_kgptalkie as ps
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

# Create your views here.

tfidf=[]
clf =[]
review=""

def get_clean(x):
    x = str(x).lower().replace('\\', '').replace('_', ' ').replace(',','')
    x = ps.cont_exp(x)
    x = ps.remove_emails(x)
    x = ps.remove_urls(x)
    x = ps.remove_html_tags(x)
    x = ps.remove_accented_chars(x)
    x = ps.remove_special_chars(x)
    x = re.sub("(.)\\1{2,}", "\\1", x)
    return x

def readExcel(request):

    df = pd.read_excel('~/SDP_Project/MR_SYSTEM/userapp/templates/AmazonSDPDataset_original.ods', engine='odf', usecols= ['reviewText','overall'])
    df['reviewText'] = df['reviewText'].apply(lambda x: get_clean(x))

    global tfidf
    tfidf = TfidfVectorizer(analyzer='word')
    X = tfidf.fit_transform(df['reviewText'])
    Y = df['overall']
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.25, random_state=0)
    global clf
    clf = LinearSVC(C=0.1, class_weight='balanced')
    clf.fit(X_train,Y_train)
    return HttpResponseRedirect('/user/user_home/')



def user_home(request):
    if "user" in request.session:
        cid = request.session["user"]
        star = request.GET.get('star','')
        filter = False
        user = User.objects.filter(ID=cid)
        if user.exists():
            user = User.objects.get(ID=cid)
            username = user.name
            movies = Movie.objects.all()
            if star != "":
                movies = Movie.objects.filter(rating__range=(float(star)-0.9,float(star))).order_by('-rating')
                filter = True
            if movies.exists():
                return render(request,'user_home.html',{'movielist':movies,'nomovie':False,'filter':filter,'username':username})
            else:
                return render(request,'user_home.html',{'movielist':movies,'nomovie':True,'filter':filter,'username':username})
    return HttpResponseRedirect('/login/')

def calculateRating(request):
    if "user" in request.session:
        id=request.POST.get('movieid','')
        reviewText=request.POST.get('reviewText','')
        global review
        review = reviewText
        reviewText = get_clean(reviewText)
    
        global clf
        global tfidf
        reviewText = tfidf.transform([reviewText])
        rating = clf.predict(reviewText)
        return HttpResponseRedirect('/user/addReview?rating='+str(rating[0])+'&movieid='+str(id))
    return HttpResponseRedirect('/login/')

def addReview(request):
    if "user" in request.session:
        rating = request.GET.get('rating','')
        id = request.GET.get('movieid','')
        global review
        reviewText = review
        Rating = rating
        DateTime = datetime.now()
        uid = request.session["user"]
        user = User.objects.get(ID=uid)
        movie = Movie.objects.get(ID=id)

        new_review = Review(reviewText=reviewText,rating=Rating,dateTime=DateTime,mid=movie,uid=user)
        new_review.save()

        avg_rating(new_review.mid_id) #update avg movie rating

        movie = Movie.objects.get(ID=id)
        movie.releasedDate = (movie.releasedDate).strftime("%d-%m-%Y")
        movie.duration = (movie.duration).strftime("%H:%M")

        reviews = Review.objects.filter(mid=movie)
        return HttpResponseRedirect('/user/showmovie?movieid='+str(id))
    return HttpResponseRedirect('/login/')

def showmovie(request):
    if "user" in request.session:
        cid = request.session["user"]
        m =request.GET.get('m','')
        if m == "":
            m= False
        sortby= request.GET.get('star','')
        id = request.GET.get('movieid','')

        movie = Movie.objects.get(ID=id)
        user = User.objects.get(ID= cid)
        added = False

        myreviews= Review.objects.filter(mid_id= movie, uid_id=user) #don't allow user to add review if already added
        if myreviews.exists():
            added = True
        movie.releasedDate = (movie.releasedDate).strftime("%Y-%m-%d")
        movie.duration = (movie.duration).strftime("%H:%M")
       
        if sortby != '':
            reviews= Review.objects.filter(mid=id, rating= sortby)
        else:
            reviews = Review.objects.filter(mid=id)
        sortedReviews = sorted(
            reviews,
            key=lambda x: x.dateTime, reverse=True
        )
        return render(request,'showmovie.html',{'movie':movie,'reviews':sortedReviews,'currentuserid':cid, 'added':added,'mr':m})
    return HttpResponseRedirect('/login/')

def my_reviews(request):
    c= {}
    c.update(csrf(request))
    if 'user' in request.session:
        userid = request.session["user"]
        getuser = User.objects.get(ID = userid)

        reviews = Review.objects.filter(uid_id= getuser).order_by('-dateTime')
        if reviews.exists():
            return render(request,'myreviews.html',{'reviews':reviews,'c':c})
        else:
            return render(request,'myreviews.html',{'reviews':reviews, 'msg':'You have not added any reviews yet..!!','c':c})
    return HttpResponseRedirect('/login/')

def update_review(request):
    if 'user' not in request.session:
        return HttpResponseRedirect('/login/')
    rid = request.POST.get('id','')
    if rid:
        review = Review.objects.get(ID= rid)
        review.reviewText = request.POST.get('new-rw','')
        review.dateTime = datetime.now()

        global clf
        global tfidf
        rw = tfidf.transform([get_clean(review.reviewText)])
        review.rating = clf.predict(rw)
        review.save()
        avg_rating(review.mid_id)
    return HttpResponseRedirect('/user/reviews/')

def delete_review(request):
    if 'user' not in request.session:
        return HttpResponseRedirect('/login/')
    
    rid = request.GET.get('id','')
    if rid:
        review= Review.objects.get(ID= rid)
        movie_id = review.mid_id
        review.delete()
        avg_rating(movie_id)
    return HttpResponseRedirect('/user/reviews/')

def avg_rating(movie_id):
    "function to calculate average rating & to update it in database"

    movie =  Movie.objects.get(ID= movie_id)
    reviews = Review.objects.filter(mid_id= movie) #update average rating of movie
    rating = 0.0
        
    if reviews.exists():
        for r in reviews:
            rating += r.rating
        rating /= len(reviews)

    movie.rating = round(rating,1) #store rating in y.x format- 1 decimal point
    movie.save()
    return 

def profile(request):
    id= request.GET.get('update','')
    c = {}
    c.update(csrf(request))
    if 'user' in request.session:
        getuser = User.objects.get(ID= request.session["user"])
        if id=="":
            id=0
        return render(request,'profile.html',{'c':c, 'user':getuser, 'id':id})
    else:
        return HttpResponseRedirect('/login/')
    
def update_profile(request):
    c= {}
    c.update(csrf(request))
    uid = request.session["user"]
    name = request.POST.get('name','')
    bio= request.POST.get('bio','')
    try:
        getuser= User.objects.get(ID= uid)
        getuser.name = name
        getuser.bio = bio
        filepath=request.FILES.get('image',False)
        if filepath:
            getuser.image = request.FILES["image"]
        getuser.save()
        user= User.objects.get(ID= uid)
        return render(request,'profile.html',{'c':c,'user':user,'id':0})
    except ObjectDoesNotExist:
        alert= "Profile Not Updated.."
        return render(request,'profile.html',{'c':c,'msg':alert})
