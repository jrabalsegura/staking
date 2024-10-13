from ninja import NinjaAPI
from .models import Bet
from datetime import datetime
api = NinjaAPI()

min_stake = 0.01
max_stake = 0.07
multiplier_y = 0.002
multiplier_n = 0.002544
#OJO cambiar también en views!!!! 

@api.get("/under75/")
def get_next_stake(request):
    last_bet = Bet.objects.order_by('-created_at').first()
    if last_bet:
        return {"next_stake": last_bet.next_stake}
    return {"error": "No bets found"}

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

@api.post("/bet/")
def create_bet(request):
    try:
        data = request.json()
        stake = float(data.get('stake'))
        odd = float(data.get('odd'))
        choice = data.get('choice')

        if not all([stake, odd, choice]):
            return {"error": "Missing required fields"}, 400

        if choice not in ['y', 'n', 'hl']:
            return {"error": "Invalid choice"}, 400

        process_bet(stake, odd, choice)
        return {"message": "Bet created successfully"}, 201
    except ValueError:
        return {"error": "Invalid data types"}, 400
    except Exception as e:
        return {"error": str(e)}, 500
