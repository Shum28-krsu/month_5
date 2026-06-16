from django.urls import path
from views import *

urlpatterns = [
    path( 'register/', RegisterAPIView.as_view()),

    path('confirm/', ConfirmAPIView.as_view()),

    path('login/', LoginAPIView.as_view()),
]