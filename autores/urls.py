from django.urls import path
from . import views


app_name = 'autores'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/validate/', views.register_validate, name='register_validate'),
    path('login/', views.login_view, name='login'),
    path('login/validate/', views.login_validate, name='login_validate'),
    path('logout/', views.logout_view, name="logout"),
]
