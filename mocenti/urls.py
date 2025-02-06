from django.contrib import admin
from django.urls import path
from mocenti import views

urlpatterns = [
    path('',views.index,name='index'),
    #path('main',views.main,name='main'),
    path('login',views.login,name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup',views.signup_view,name='signup'),
    #path('analysis',views.analysis,name='analysis'),
    #path('feedback',views.feedback,name='feedback'),
    #path('about',views.about,name='about'),
    path('url',views.url,name='url'),
    

]