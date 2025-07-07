from django.urls import path
from .views import acceder, homePage, salir

urlpatterns = [
    path('', acceder, name="login"),
    path('home/', homePage, name="home"),
    path('logout/', salir, name="logout"),
]
