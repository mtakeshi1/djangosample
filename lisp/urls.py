from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.evaluateRequest, name='index_lisp'),

]