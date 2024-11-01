from django.forms import ModelForm
from .models import Bet

class BetForm(ModelForm):
    class Meta:
        model = Bet
        fields = ['stake', 'odd', 'result', 'next_multiplier', 'balance', 'next_stake', 'daily_profit']