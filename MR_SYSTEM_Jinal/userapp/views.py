from django.shortcuts import render
from django.template.context_processors import csrf
import numpy as np
import pandas as pd 
import preprocess_kgptalkie as ps
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

# Create your views here.
movies = {0:{'Movie':"Genius",'Review':"-",'Rating':0}, 1:{'Movie':"Mission Mangal", 'Review':"-",'Rating':0}, 
2:{'Movie':"3 idiots",'Review':"-",'Rating':0}, 3:{'Movie':"URI",'Review':"-",'Rating':0}}
tfidf= []
clf= []

def display_movies(request):
    c={}
    df = pd.read_excel('../Templates/AmazonSDPDataset_try.ods', engine='odf', usecols= ['reviewText','overall'])
    df['reviewText']= df['reviewText'].apply(lambda x: get_clean(x))

    global tfidf
    tfidf = TfidfVectorizer(max_features=2500,ngram_range=(1,5), analyzer='char') # append ngram_range=(1,5), analyzer='char'
    X = df['reviewText']
    y = df['overall']
    X = tfidf.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

    global clf
    clf = LinearSVC(C = 5.0, class_weight= 'balanced') #append C = 10, class_weight= 'balanced'
    clf.fit(X_train, y_train)
    c.update(csrf(request))
    return render(request,'display_movies.html',{'c':c,'movies':movies})

def get_clean(x):
    x = str(x).lower().replace('\\','').replace('_',' ')
    x = ps.cont_exp(x)
    x = ps.remove_emails(x)
    x = ps.remove_urls(x)
    x = ps.remove_html_tags(x)
    x = ps.remove_accented_chars(x)
    x = ps.remove_special_chars(x)
    x = re.sub("(.)\1{2,}", "\1", x)
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
