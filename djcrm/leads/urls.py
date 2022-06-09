from django.urls import path
from . import views

app_name = 'leads'

urlpatterns = [
    path('all/', views.home, name='home'),
    path('<int:pk>', views.home, name='lead-single'),
]
