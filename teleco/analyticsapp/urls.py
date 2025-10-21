from django.urls import path
from . import views

urlpatterns = [
    path('revenue-trend-month/', views.revenue_trend_month, name='revenue-trend-month'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
