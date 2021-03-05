from django.shortcuts import render
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect,HttpResponse

import pandas as pd
import numpy as np
import preprocess_kgptalkie as ps
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

# Create your views here.

movie_list={ 0:'Rambo', 1:'Dayalu' , 2:'Dil bechara' , 3:'Dhoom3' }
movie_review={0:'-', 1:'-' , 2:'-' , 3:'-' , 4:'-'}
movie_ratting={0:'0', 1:'0' , 2:'0' , 3:'0'}

tfidf = ""
clf = ""

def user_home(request):
    #c = {}
    #c.update(csrf(request))
    global tfidf
    global clf

    df = pd.read_csv('https://raw.githubusercontent.com/laxmimerit/Amazon-Musical-Reviews-Rating-Dataset/master/Musical_instruments_reviews.csv', usecols=['reviewText','overall'])
    df['reviewText'] = df['reviewText'].apply(lambda x: get_clean(x))

    #instantiate the vectorizer object
    #It is used to convert a collection of raw documents to a matrix of TF-IDF features.
    tfidf = TfidfVectorizer(max_features=20000, ngram_range=(1,5) , analyzer='char')

    #convert the documents into a matrix
    #Return a matrix of the format ( (document_id,feature_id) , tfidf_value )
    #This entry is there in matrix if document of id=document_id is having feature of id=feature_id, for all document in df['reviewText'].
    #We just only need to pass List[] as the parameter to the fit_transform() method.
    X = tfidf.fit_transform(df['reviewText'])

    #Array mapping from feature integer indices to feature name.
    #print(tfidf.get_feature_names())

    #To print matrix
    #for x in X:
    #    for y in x:
    #        print(y)
    #print(X)

    Y = df['overall']

    #Splitting your dataset is essential for an unbiased evaluation of prediction performance.
    #With train_test_split() , You’ll split inputs and outputs at the same time, with a single function call.
    X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2, random_state=0)
    clf = LinearSVC(C=20)
    clf.fit(X_train,Y_train)

    return render(request,'user_home.html',{'movies':movie_list,'movie_review':movie_review,'movie_ratting':movie_ratting})

def add_review(request):
    review_Text = request.POST.get('reviewtext','')
    submitid = request.POST.get('submitid','')

    global tfidf
    global clf
    review_Text = get_clean(review_Text)
    vec = tfidf.transform( [ review_Text ] )
    temp = clf.predict(vec)

    t = {int(submitid) : review_Text}
    movie_review.update(t)
    t = {int(submitid) : temp[0]}
    movie_ratting.update(t)

    return render(request,'user_home.html',{'movies':movie_list,'movie_review':movie_review,'movie_ratting':movie_ratting,'review':review_Text,'ratting':temp,'id':submitid})
    #return HttpResponse("hello ")

def get_clean(x):
    x = str(x).lower().replace('\\', '').replace('_', ' ')
    x = ps.cont_exp(x)
    x = ps.remove_emails(x)
    x = ps.remove_urls(x)
    x = ps.remove_html_tags(x)
    x = ps.remove_accented_chars(x)
    x = ps.remove_special_chars(x)
    x = re.sub("(.)\\1{2,}", "\\1", x)
    return x