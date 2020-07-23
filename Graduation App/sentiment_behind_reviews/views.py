from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from sentiment_behind_reviews.forms import SignUpForm
import pymongo
# from .souq_configs import *
from .models import Products, Review, Contact_us
from sentiment_behind_reviews.ml_work.cleaning_data import *
import json
import sys
import os
import pickle
import io
import urllib, base64
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from sklearn.model_selection import train_test_split
from django.contrib.auth.models import User
# Features Extraction
from sklearn.feature_extraction.text import TfidfVectorizer

# Evaluation
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

# models
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC

from decimal import Decimal

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


# load model and features extraction weights

tfidf_vectorizer = pickle.load(open("sentiment_behind_reviews/ml_work/tfidf_vectorizer.pickle", "rb"))
logistic_model = pickle.load(open("sentiment_behind_reviews/ml_work/logistic_model.sav", "rb"))



def load_data(products):
    '''
    Argument:
    Products: the products we have in database
    return:
    List of all of these dictionary that will be displayed in template
    '''
    products_info = []
    for i, product in enumerate(products):
        product_title               = product.product_title
        image_src                   = product.image_src
        product_id                   = product.id
        product_url                 = product.product_url
        product_new_price           = product.product_new_price
        product_old_price           = product.product_old_price
        product_discount_percentage = product.product_discount_percentage
        product_discount_value      = product.product_discount_value
        one_product = {
            'product_title':               product_title,
            'product_id':                  product_id,
            'image_src':                   image_src,
            'product_url':                 product_url,
            'product_new_price':           product_new_price,
            'product_old_price':           product_old_price,
            'product_discount_percentage': product_discount_percentage,
            'product_discount_value':      product_discount_value,
        }
        products_info.append(one_product)
    return products_info


def products(request):
    # get just 1000 product from all of product we have

    products = list(Products.objects.all())[:1000]
    products_info = {}
    products_info['products_info'] = load_data(products)
    return render(request, 'sentiment_behind_reviews/products.html', products_info)



def product_reviews(request, id):
    try:
        products_reviews = {}
        reviews = Review.objects.filter(review=id)

        all_reviews = []
        for review in reviews:
            one_product_reviews = review.product_review
            if not(one_product_reviews == "لا يوجد" or one_product_reviews == "لا توجد" or one_product_reviews == "لايوجد" or one_product_reviews == "لاتوجد" or len(one_product_reviews) < 3):
                all_reviews.append(one_product_reviews)

        cleaned_reviews = arabic_pip_line(all_reviews)
        transformed_reviews = tfidf_vectorizer.transform(cleaned_reviews)
        transformed_reviews  = transformed_reviews.toarray()
        predicted_reviews = logistic_model.predict(transformed_reviews)

        final_result = []
        one_review = {}
        num_positive = 0
        num_negative = 0
        for i in range(len(predicted_reviews)):
            one_review = {}
            if predicted_reviews[i] & 1:
                num_positive +=1
                one_review = {
                'review': all_reviews[i],
                'preict': "Positive"
                }
            else:
                num_negative +=1
                one_review = {
                    'review': all_reviews[i],
                    'preict': "Negative"
                }
            final_result.append(one_review)
        labels = ['Positive', 'Negative']

        sizes = [num_positive, num_negative]
        explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig = plt.figure(figsize=(8,8))
        plt.pie(sizes, explode=explode, labels=labels, 
        autopct='%1.1f%%', shadow=True, startangle=140)
        plt.savefig('sentiment_behind_reviews/static/images/charts/pie.png')

        products_reviews['products_reviews'] = final_result
        
    except:
        pass
    return render(request, 'sentiment_behind_reviews/reviews.html', products_reviews)





def home_page(request):
    if request.method == "POST":
        data = json.loads(request.body) # get data hat user inout in text area
        review = []
        review.append(data['user_input'])
        cleaned_review = arabic_pip_line(review)
        transformed_review = tfidf_vectorizer.transform(cleaned_review)
        transformed_review  = transformed_review.toarray()
        predicted_review = list(logistic_model.predict(transformed_review))

        if predicted_review[0] == 0:
            data['Polarity'] = "Negative"
        else: data['Polarity'] = "Positive"
        return JsonResponse(data)
    return render(request, 'sentiment_behind_reviews/home_page.html')




################################## Forms


def signup_form(request):
    if request.method == 'POST':
        data = json.loads(request.body) # get data hat user inout in text area
        form = SignUpForm(data)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('username')
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # data['success'] = True
            return JsonResponse(data)
        else:
            form = SignUpForm(request.POST)
            return JsonResponse({'errors': form.errors})
    else:
        form = SignUpForm()
    return render(request, 'sentiment_behind_reviews/signup.html', {'form': form})



def login_form(request):


    if request.method == 'POST':
        data = json.loads(request.body) # get data hat user inout in text area
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse(data)
        else: 
            return render(request, 'sentiment_behind_reviews/login.html')


    return render(request, 'sentiment_behind_reviews/login.html')



def logout_form(request):
    logout(request)
    return redirect('home_page')


def contact_form(request):
    if request.method == "POST":
        data = json.loads(request.body)
        if request.user.is_authenticated:
            data['mail'] = request.user.username
            data['first_name'] = request.user.first_name
        Contact_us.objects.create(
            mail=data['mail'],
            first_name=data['first_name'],
            phonenumber=data['phonenumber'],
            message=data['message']
        )
        return JsonResponse(data)
    else:
        return render(request, 'sentiment_behind_reviews/contact_us.html')
