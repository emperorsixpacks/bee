from django.urls import path
from .views import dashboard, withdraw, deposits, earnings_dashboard


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('withdraw/', withdraw, name='withdraw'),
    path('deposit/', deposits, name='deposits'),
    path('earnings_dashboard/', earnings_dashboard, name='earnings_dashboard'),
]