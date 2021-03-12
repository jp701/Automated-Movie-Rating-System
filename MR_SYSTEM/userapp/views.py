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
""" movies = {0:{'Movie':"Genius",'Review':"-",'Rating':0}, 1:{'Movie':"Mission Mangal", 'Review':"-",'Rating':0}, 
2:{'Movie':"3 idiots",'Review':"-",'Rating':0}, 3:{'Movie':"URI",'Review':"-",'Rating':0}}
tfidf= []
clf= []

def display_movies(request):
    c={}
    c.update(csrf(request))
    df = pd.read_excel('../Templates/AmazonSDPDataset_try.ods', engine='odf', usecols= ['reviewText','overall'])
    df['reviewText']= df['reviewText'].apply(lambda x: get_clean(x))

    global tfidf
    tfidf = TfidfVectorizer(analyzer='word') # append ngram_range=(1,5), analyzer='char'
    X = df['reviewText']
    y = df['overall']
    X = tfidf.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

    global clf
    clf = LinearSVC(C = 0.1, class_weight= 'balanced') #append C = 10, class_weight= 'balanced'
    clf.fit(X_train, y_train)
    return render(request,'display_movies.html',{'c':c,'movies':movies})

def get_clean(x):
    x = str(x).lower().replace('\\','').replace('_',' ').replace(',',' ')
    x = ps.cont_exp(x)
    x = ps.remove_emails(x)
    x = ps.remove_urls(x)
    x = ps.remove_html_tags(x)
    x = ps.remove_accented_chars(x)
    x = ps.remove_special_chars(x)
    x = re.sub("(.)\\1{2,}", "\\1", x)
    return x

def calculate_rating(request):
    review_text = request.POST.get('review','')
    key =  int(request.POST.get('key',''))
    movies[key]['Review']= review_text

    global clf
    global tfidf
    review = tfidf.transform([get_clean(review_text)])
    rating = clf.predict(review)

    movies[key]['Rating'] = rating[0]
    c={}
    c.update(csrf(request))
    return render(request,'display_movies.html',{'c':c, 'movies':movies, 'rating':rating[0], 'review':review_text})
"""
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

def user_home(request):
    #c = {}
    #c.update(csrf(request))
    if "user" in request.session:
        cid = request.session["user"]
        user = User.objects.filter(ID=cid)
        if user.exists():
            user = User.objects.get(ID=cid)
            username = user.name
            movies = Movie.objects.all()
            if movies.exists():
                return render(request,'user_home.html',{'movielist':movies,'nomovie':False,'username':username})
            else:
                return render(request,'user_home.html',{'movielist':movies,'nomovie':True,'username':username})
    return HttpResponseRedirect('/login/')

def showmovie(request):
    if "user" in request.session:
        cid = request.session["user"]
        id=request.POST.get('movieid','')
        if id == "":
            id = request.GET.get('movieid','')
        movie = Movie.objects.get(ID=id)
        
        movie.releasedDate = (movie.releasedDate).strftime("%Y-%m-%d")
        movie.duration = (movie.duration).strftime("%H:%M")
        
        reviews = Review.objects.filter(mid=id)
        sortedReviews = sorted(
            reviews,
            key=lambda x: x.dateTime, reverse=True
        )
        return render(request,'showmovie.html',{'movie':movie,'reviews':sortedReviews,'currentuserid':cid})
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
        
        reviews = Review.objects.filter(mid_id= movie) #update average rating of movie
        rating = 0.0
        
        for r in reviews:
            rating += r.rating
        rating /= len(reviews)

        movie.rating = rating
        movie.save()

        movie = Movie.objects.get(ID=id)
        movie.releasedDate = (movie.releasedDate).strftime("%Y-%m-%d")
        movie.duration = (movie.duration).strftime("%H:%M")

        reviews = Review.objects.filter(mid=movie)
        return HttpResponseRedirect('/user/showmovie?movieid='+str(id))
    return HttpResponseRedirect('/login/')

def my_reviews(request):
    c= {}
    c.update(csrf(request))
    if 'user' in request.session:
        userid = request.session["user"]
        getuser = User.objects.get(ID = userid)
        #console.log(user.email)
        reviews = Review.objects.filter(uid_id= getuser)
        if reviews.exists():
            return render(request,'myreviews.html',{'reviews':reviews,'c':c})
        else:
            return render(request,'myreviews.html',{'reviews':reviews, 'msg':'No reviews available','c':c})
    return HttpResponseRedirect('/login/')

def update_review(request):
    if 'user' not in request.session:
        return HttpResponseRedirect('/login/')
    rid = request.POST.get('id','')
    if rid:
        review = Review.objects.get(ID= rid)
        review.reviewText = request.POST.get('new-rw','')
        review.dateTime = datetime.now()
        store_rating(review)
    return HttpResponseRedirect('/user/reviews/')

def delete_review(request):
    if 'user' not in request.session:
        return HttpResponseRedirect('/login/')
    
    rid = request.GET.get('id','')
    if rid:
        review= Review.objects.get(ID= rid)
        movie_id = review.mid_id
        review.delete()

        movie =  Movie.objects.get(ID= movie_id)
        reviews = Review.objects.filter(mid_id= movie) #update average rating of movie
        rating = 0.0

        if reviews.exists():
            for r in reviews:
                rating += r.rating
            rating /= len(reviews)

        movie.rating = rating
        movie.save()
    return HttpResponseRedirect('/user/reviews/')

def store_rating(review):
    "function to calculate rating, average rating & to update it in database"
    global clf
    global tfidf
    rw = tfidf.transform([get_clean(review.reviewText)])
    review.rating = clf.predict(rw)
    review.save()

    movie =  Movie.objects.get(ID= review.mid_id)
    reviews = Review.objects.filter(mid_id= movie) #update average rating of movie
    rating = 0.0
        
    for r in reviews:
        rating += r.rating
    rating /= len(reviews)

    movie.rating = rating
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
