from .models import Bet, BetPending
from datetime import datetime
from django.shortcuts import get_object_or_404

min_stake = 0.01
max_stake = 0.07
multiplier_y = 0.002
multiplier_n = 0.002544
#OJO cambiar también en api!!!! 

def round_to_5_decimals(number):
    return round(number, 5)

def check_if_same_day(date1, date2):
    return date1.day == date2.day and date1.month == date2.month and date1.year == date2.year

def process_bet(stake, odd, choice):
    last_bet = Bet.objects.last()
            
    multiplier = last_bet.next_multiplier
    balance = last_bet.balance
    last_bet_date = last_bet.created_at
    last_daily_profit = last_bet.daily_profit
    same_day = check_if_same_day(last_bet_date, datetime.now())
    
    if choice == 'y':
        balance = round_to_5_decimals(balance + stake * odd - stake)
        next_multiplier = round_to_5_decimals(max(multiplier - multiplier_y, min_stake))
        next_stake = round_to_5_decimals(next_multiplier * balance)
        if same_day:
            daily_profit = round_to_5_decimals(last_daily_profit + stake * odd - stake)
        else:
            daily_profit = round_to_5_decimals(stake * odd - stake)
        
    elif choice == 'n':
        balance = round_to_5_decimals(balance - stake)
        next_multiplier = round_to_5_decimals(min(multiplier + multiplier_n, max_stake))
        next_stake = round_to_5_decimals(next_multiplier * balance)
        if same_day:
            daily_profit = round_to_5_decimals(last_daily_profit - stake)
        else:
            daily_profit = round_to_5_decimals(-stake)
    elif choice == 'hl':
        balance = round_to_5_decimals(balance - stake / 2)
        next_multiplier = round_to_5_decimals(min(multiplier + multiplier_n, max_stake))
        next_stake = round_to_5_decimals(next_multiplier * balance)
        if same_day:
            daily_profit = round_to_5_decimals(last_daily_profit - stake / 2)
        else:
            daily_profit = round_to_5_decimals(-stake / 2)
    elif choice == 'hw':
        balance = round_to_5_decimals(balance + stake * odd / 2 - stake)
        next_multiplier = round_to_5_decimals(max(multiplier - multiplier_y, min_stake))
        next_stake = round_to_5_decimals(next_multiplier * balance)
        if same_day:
            daily_profit = round_to_5_decimals(last_daily_profit + stake * odd / 2 - stake)
        else:
            daily_profit = round_to_5_decimals(stake * odd / 2 - stake)
            
    
    # Create a new Bet
    Bet.objects.create(
        stake=stake,
        odd=odd,
        result=choice,
        next_multiplier=next_multiplier,
        balance=balance,  # You may want to calculate this based on your logic
        next_stake=next_stake,
        daily_profit=daily_profit
    )
    
def get_last_bet():
    return Bet.objects.last()

def get_last_10_bets():
    return Bet.objects.order_by('-created_at')[:10]

def get_pending_bets():
    return BetPending.objects.all()

def create_bet_pending(stake, odd):
    BetPending.objects.create(
        stake=stake,
        odd=odd
    )
    
def update_bet_service(bet_id, stake, odd, result, next_multiplier, balance, next_stake, daily_profit):
    bet = get_object_or_404(Bet, id=bet_id)
    bet.stake = stake
    bet.odd = odd
    bet.result = result
    bet.next_multiplier = next_multiplier
    bet.balance = balance
    bet.next_stake = next_stake
    bet.daily_profit = daily_profit
    bet.save()
    
def delete_bet_service(bet_id):
    bet = get_object_or_404(Bet, id=bet_id)
    bet.delete()
    
def get_last_stake():
    last_bet = get_last_bet()
    return last_bet.next_stake if last_bet else 0


