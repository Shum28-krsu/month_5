from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/users/register/',views.register_api_view),
    path('api/v1/users/login/',views.login_api_view),
    path('api/v1/users/confirm/',views.confirm_api_view),
]