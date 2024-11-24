from ninja import NinjaAPI, Schema
from ninja.errors import HttpError

from .models import Bet
from .services import create_bet_pending, process_bet

api = NinjaAPI()


@api.get("/under75/")
def get_next_stake(request):
    last_bet = Bet.objects.order_by("-created_at").first()
    if last_bet:
        return {"next_stake": last_bet.next_stake}
    return {"error": "No bets found"}


class NewBet(Schema):
    stake: float
    odd: float
    choice: str
    method: str


class NewBetPending(Schema):
    stake: float
    odd: float
    method: str


@api.post("/bet/")
def create_bet(request, bet: NewBet):
    try:
        stake = float(bet.stake)
        odd = float(bet.odd)
        choice = bet.choice
        method = bet.method

        print(stake, odd, choice, method)

        if not all([stake, odd, choice, method]):
            raise HttpError(400, "Missing required fields")

        if choice not in ["y", "n", "hl", "hw"]:
            raise HttpError(400, "Invalid choice")

        process_bet(stake, odd, choice, method)
        return {"message": "Bet created successfully"}
    except ValueError as ve:
        raise HttpError(400, f"Invalid data types: {str(ve)}")
    except HttpError as he:
        raise
    except Exception as e:
        raise HttpError(500, f"An unexpected error occurred: {str(e)}")


@api.post("/bet/pending/")
def create_pending(request, bet: NewBetPending):
    try:
        stake = float(bet.stake)
        odd = float(bet.odd)
        method = bet.method

        print(stake, odd, method)

        create_bet_pending(stake, odd, method)

        return {"message": "Bet pending created successfully"}
    except ValueError as ve:
        raise HttpError(400, f"Invalid data types: {str(ve)}")
    except HttpError as he:
        raise
    except Exception as e:
        raise HttpError(500, f"An unexpected error occurred: {str(e)}")
