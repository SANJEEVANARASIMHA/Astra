from django.urls import path

from . import views

app_name = 'zones'
urlpatterns = [
    # URL for Zones (get/post/delete)
    path('zones', views.ZoneAPI.as_view()),

    # URL for ZoneTrackingAPI (post)
    path('zones/tracking', views.ZoneTrackingAPI.as_view()),

    # URL for WeeklyZoneTrackingAPI (get)
    path('zones/weekly/tracking', views.WeeklyZoneTrackingAPI.as_view()),

    # # URL for MonthlyZoneTrackingAPI (get)
    path('zones/monthly/tracking', views.MonthlyZoneTrackingAPI.as_view()),
]


