from ninja import NinjaAPI
from .models import Bet

api = NinjaAPI()

@api.get("/under75/")
def get_next_stake(request):
    last_bet = Bet.objects.order_by('-created_at').first()
    if last_bet:
        return {"next_stake": last_bet.next_stake}
    return {"error": "No bets found"}