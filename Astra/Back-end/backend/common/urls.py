from django.urls import path

from . import views

app_name = 'common'

urlpatterns = [
    # URL to login to application (post)
    path('login', views.loginAPI.as_view(), name='login'),
    
    # URL to logout from application
    path('logout', views.logoutAPI.as_view() , name='logout'),
    
    # URL for UploadMapAPI (get/post)
    path('uploadmap', views.FloorMapAPI.as_view(),name='uploadmap'),
]

