from django.urls import path
from .views import stake_view, update_bet_pending, update_bet

app_name = 'stakes'

urlpatterns = [
    path('', stake_view, name='stake'),
    path('update/<int:id>/', update_bet_pending, name='update_bet_pending'),
    path('update_bet/<int:id>/', update_bet, name='update_bet'),
]