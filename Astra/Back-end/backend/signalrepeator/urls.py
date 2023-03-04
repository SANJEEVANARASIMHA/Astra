from django.urls import path

from . import views

app_name = 'signalrepeator'
urlpatterns = [
    # URL for SignalRepeatorAPI (get/post/delete)
    path('signalrepeator', views.SignalRepeatorAPI.as_view()),
]

