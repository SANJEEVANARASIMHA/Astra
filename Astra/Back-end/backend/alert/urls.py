from django.urls import path
from . import views


app_name = 'alert'
urlpatterns = [
    path('alerts', views.Alerts.as_view()),
    path('alert/panic', views.AlertPanicApi.as_view())

]