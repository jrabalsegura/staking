from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from .models import Bet, BetPending
import math

min_stake = 0.01
max_stake = 0.07
multiplier_y = 0.002
multiplier_n = 0.002526

def round_to_hundred(number):
    return math.ceil(number / 100) * 100

def round_to_5_decimals(number):
    return round(number, 5)

def process_bet(stake, odd, choice):
    last_bet = Bet.objects.last()
            
    multiplier = last_bet.next_multiplier
    balance = last_bet.balance   
    
    if choice == 'y':
        balance = round_to_5_decimals(balance + stake * odd - stake)
        next_multiplier = round_to_5_decimals(max(multiplier - multiplier_y, min_stake))
        next_stake = round_to_5_decimals(next_multiplier * round_to_hundred(balance))
    elif choice == 'n':
        balance = round_to_5_decimals(balance - stake)
        next_multiplier = round_to_5_decimals(min(multiplier + multiplier_n, max_stake))
        next_stake = round_to_5_decimals(next_multiplier * round_to_hundred(balance))
        print(balance, next_multiplier, next_stake, round_to_5_decimals(balance - stake))
    elif choice == 'hl':
        balance = round_to_5_decimals(balance - stake / 2)
        next_multiplier = round_to_5_decimals(min(multiplier + multiplier_n, max_stake))
        next_stake = round_to_5_decimals(next_multiplier * round_to_hundred(balance))
    
    # Create a new Bet
    Bet.objects.create(
        stake=stake,
        odd=odd,
        result=choice,
        next_multiplier=next_multiplier,
        balance=balance,  # You may want to calculate this based on your logic
        next_stake=next_stake
    )

# Create your views here.
@require_http_methods(["GET", "POST"])
def stake_view(request):
    if request.method == 'POST':
        stake = float(request.POST.get('stake', 0))
        odd = float(request.POST.get('odd', 0))
        choice = request.POST.get('choice')
        
        if choice in ['y', 'n', 'hl']:
            process_bet(stake, odd, choice)
        else:
            # Create a new BetPending
            BetPending.objects.create(
                stake=stake,
                odd=odd,
            )
        
        return redirect('stakes:stake')  # Redirect back to the same page after processing

    # Get the last bet for stake and multiplier
    last_bet = Bet.objects.last()
    current_stake = last_bet.next_stake if last_bet else 0
    current_multiplier = last_bet.next_multiplier if last_bet else 0

    # Get pending bets
    pending_bets = BetPending.objects.all()

    # Get last 10 bets in reverse order
    last_bets = Bet.objects.order_by('-created_at')[:10]

    context = {
        'current_stake': current_stake,
        'current_multiplier': current_multiplier,
        'pending_bets': pending_bets,
        'last_bets': last_bets,
    }

    return render(request, 'stakes/stake.html', context)

@require_http_methods(["POST"])
def update_bet_pending(request, id):
    bet_pending = get_object_or_404(BetPending, id=id)
    choice = request.POST.get('choice')
    
    if choice in ['y', 'n', 'hl']:
        process_bet(bet_pending.stake, bet_pending.odd, choice)
        
        # Delete the BetPending object as it's no longer needed
        bet_pending.delete()
        
        # Redirect to stake view with POST data
        return redirect(reverse('stakes:stake'))
    else:
        # If no valid choice is provided, redirect back to the same page
        return redirect(request.META.get('HTTP_REFERER', reverse('stakes:stake')))