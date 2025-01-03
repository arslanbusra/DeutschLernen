from django.urls import path
from . import views

urlpatterns=[

    path('',views.home, name='home'),
    path('back/', views.back, name='back'),
    path('further/', views.further, name='further'),
    path('result/', views.result, name='result'),
    path('result-page/', views.result_view, name='result-page'),
  

]

