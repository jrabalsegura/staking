from .models import Bet, BetPending
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone


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
            return "4000-7000"
        elif balance < 1000:
            return "1000-2000"
    elif state == "4000-7000":
        if balance >= 7000:
            return "7000-12000"
        elif balance < 2000:
            return "2000-4000"
    elif state == "7000-12000":
        if balance >= 12000:
            return "12000-20000"
        elif balance < 4000:
            return "4000-8000"
    elif state == "12000-20000":
        if balance >= 20000:
            return "20000-30000"
        elif balance < 7000:
            return "7000-12000"
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


def process_bet(stake, odd, choice, method):
    last_bet = Bet.objects.last()
    
    # Get the current time in the Europe/Madrid timezone
    current_time = timezone.localtime()
    
    balance = last_bet.balance
    last_bet_date = last_bet.created_at
    last_daily_profit = last_bet.daily_profit
    last_state = last_bet.nextState
    last_number_of_bets_day = last_bet.number_of_bets_day
    same_day = check_if_same_day(last_bet_date, current_time)
    
    if same_day:
        number_of_bets_day = last_number_of_bets_day + 1
    else:
        number_of_bets_day = 1
    
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
        nextState=next_state,
        method=method,
        number_of_bets_day=number_of_bets_day
    )
    
def get_last_bet():
    return Bet.objects.last()

def get_last_5_bets():
    two_days_ago = datetime.now() - timedelta(days=5)
    return Bet.objects.filter(created_at__gte=two_days_ago).order_by('-created_at')

def get_pending_bets():
    return BetPending.objects.all()

def create_bet_pending(stake, odd, method):
    BetPending.objects.create(
        stake=stake,
        odd=odd,
        method=method
    )
    

def update_bet_service(bet_id, stake, odd, result, balance, next_stake, daily_profit, method, number_of_bets_day):
    bet = get_object_or_404(Bet, id=bet_id)
    bet.stake = stake
    bet.odd = odd
    bet.result = result
    bet.balance = balance
    bet.next_stake = next_stake
    bet.daily_profit = daily_profit
    bet.method = method
    bet.number_of_bets_day = number_of_bets_day
    bet.save()
    
def delete_bet_service(bet_id):
    bet = get_object_or_404(Bet, id=bet_id)
    bet.delete()
    
def get_last_stake():
    last_bet = get_last_bet()
    return last_bet.next_stake if last_bet else 0


