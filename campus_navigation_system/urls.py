
from django.contrib import admin
from django.urls import path
from navigation import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing),
    path('index/', views.index),
    path("api/buildings/", views.get_buildings),
    path("api/path/", views.get_path),

]
