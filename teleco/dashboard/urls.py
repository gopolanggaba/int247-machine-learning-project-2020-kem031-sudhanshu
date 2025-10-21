from django.urls import path
from . import views
from . import views_hvc

urlpatterns = [
    path('', views.home, name='home'),
    path('hvc/', views_hvc.hvc_lists, name='hvc-lists'),
]
