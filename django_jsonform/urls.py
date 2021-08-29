from django.urls import path
from . import views


app_name = 'django_jsonform'

urlpatterns = [
    path('upload/', views.upload_handler, name='upload'),
]