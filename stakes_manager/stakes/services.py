from .models import Bet, BetPending
from datetime import datetime
from django.shortcuts import get_object_or_404

#OJO cambiar también en api!!!! 

def round_to_5_decimals(number):
    return round(number, 5)

def check_if_same_day(date1, date2):
    return date1.day == date2.day and date1.month == date2.month and date1.year == date2.year

def calculate_next_state(state, balance):
    if state == "<250":
        if balance >= 250:
            return "250-500"
    elif state == "250-500":
        if balance >= 500:
            return "500-1000"
        elif balance < 100:
            return "<250"
    elif state == "500-1000":
        if balance >= 1000:
            return "1000-2000"
        elif balance < 250:
            return "250-500"
    elif state == "1000-2000":
        if balance >= 2000:
            return "2000-4000"
        elif balance < 500:
            return "500-1000"
    elif state == "2000-4000":
        if balance >= 4000:
            return "4000-8000"
        elif balance < 1000:
            return "1000-2000"
    elif state == "4000-8000":
        if balance >= 8000:
            return "8000-12000"
        elif balance < 2000:
            return "2000-4000"
    elif state == "8000-12000":
        if balance >= 12000:
            return "12000-20000"
        elif balance < 4000:
            return "4000-8000"
    elif state == "12000-20000":
        if balance >= 20000:
            return "20000-30000"
        elif balance < 8000:
            return "8000-12000"
    elif state == "20000-30000":
        if balance >= 30000:
            return "30000-45000"
        elif balance < 12000:
            return "12000-20000"
    elif state == "30000-45000":
        if balance >= 45000:
            return "45000-80000"
        elif balance < 20000:
            return "20000-30000"
    elif state == "45000-80000":
        if balance >= 80000:
            return ">80000"
        elif balance < 30000:
            return "30000-45000"
    elif state == ">80000":
        if balance < 45000:
            return "45000-80000"
    return state

def calculate_next_stake(state, balance):
    if state == "<250":
        return round(max(0.04 * balance, 1), 2)
    elif state == "250-500":
        return round(0.03 * balance, 2)
    elif state == "500-1000":
        return round(0.02 * balance, 2)
    elif state == "1000-2000":
        return 20
    elif state == "2000-4000":
        return 40
    elif state == "4000-8000":
        return 60
    elif state == "8000-12000":
        return 75
    elif state == "12000-20000":
        return 100
    elif state == "20000-30000":
        return 140
    elif state == "30000-45000":
        return 200
    elif state == "45000-80000":
        return 250
    elif state == ">80000":
        return 300


def process_bet(stake, odd, choice):
    last_bet = Bet.objects.last()
            
    balance = last_bet.balance
    last_bet_date = last_bet.created_at
    last_daily_profit = last_bet.daily_profit
    last_state = last_bet.nextState
    same_day = check_if_same_day(last_bet_date, datetime.now())
    
    if choice == 'y':
        balance = round_to_5_decimals(balance + stake * odd - stake)
        if same_day:
            daily_profit = round_to_5_decimals(last_daily_profit + stake * odd - stake)
        else:
            daily_profit = round_to_5_decimals(stake * odd - stake)
        
    elif choice == 'n':
        balance = round_to_5_decimals(balance - stake)
        if same_day:
            daily_profit = round_to_5_decimals(last_daily_profit - stake)
        else:
            daily_profit = round_to_5_decimals(-stake)
    elif choice == 'hl':
        balance = round_to_5_decimals(balance - stake / 2)
        if same_day:
            daily_profit = round_to_5_decimals(last_daily_profit - stake / 2)
        else:
            daily_profit = round_to_5_decimals(-stake / 2)
    elif choice == 'hw':
        balance = round_to_5_decimals(balance + stake * odd / 2 - stake)
        if same_day:
            daily_profit = round_to_5_decimals(last_daily_profit + stake * odd / 2 - stake)
        else:
            daily_profit = round_to_5_decimals(stake * odd / 2 - stake)
            
    next_state = calculate_next_state(last_state, balance)
    next_stake = calculate_next_stake(next_state, balance)
            
    
    # Create a new Bet
    Bet.objects.create(
        stake=stake,
        odd=odd,
        result=choice,
        balance=balance,  # You may want to calculate this based on your logic
        next_stake=next_stake,
        daily_profit=daily_profit,
        nextState=next_state
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
    
def update_bet_service(bet_id, stake, odd, result, balance, next_stake, daily_profit):
    bet = get_object_or_404(Bet, id=bet_id)
    bet.stake = stake
    bet.odd = odd
    bet.result = result
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


