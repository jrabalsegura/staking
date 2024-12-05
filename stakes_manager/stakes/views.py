from datetime import datetime

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import BetForm
from .models import Bet, BetPending
from .services import (
    check_if_same_day,
    create_bet_pending,
    delete_bet_service,
    get_last_10_bets,
    get_last_bet,
    get_pending_bets,
    process_bet,
    update_bet_service,
)

# Create your views here.


@require_http_methods(["GET", "POST"])
def stake_view(request):
    if request.method == "POST":
        stake = float(request.POST.get("stake", 0))
        odd = float(request.POST.get("odd", 0))
        choice = request.POST.get("choice")
        method = request.POST.get("method")
        if choice in ["y", "n", "hl"]:
            process_bet(stake, odd, choice, method)
        else:
            # Create a new BetPending
            create_bet_pending(stake, odd, method)

        return redirect(
            "stakes:stake"
        )  # Redirect back to the same page after processing

    # Seguro que esto se podría refactorizar más para quitar toda la lógica de negocio de la vista
    # pero bueno, funciona.
    # Get the last bet for stake and multiplier
    last_bet = get_last_bet()
    current_stake = last_bet.next_stake if last_bet else 0

    # Get daily profit and check if it's same day that last_bet was created
    if check_if_same_day(last_bet.get_local_created_at(), timezone.localtime()):
        daily_profit = last_bet.daily_profit
        number_of_bets_day = last_bet.number_of_bets_day
    else:
        daily_profit = 0
        number_of_bets_day = 0

    # Get pending bets
    pending_bets = get_pending_bets()

    # Get last 10 days of bets in reverse order
    last_bets = get_last_10_bets()

    context = {
        "current_stake": current_stake,
        "pending_bets": pending_bets,
        "last_bets": last_bets,
        "daily_profit": daily_profit,
        "number_of_bets_day": number_of_bets_day,
        "nextState": last_bet.nextState if last_bet else "",
        "current_date": timezone.localtime().date(),
    }

    return render(request, "stakes/stake.html", context)


@require_http_methods(["POST"])
def update_bet_pending(request, id):
    bet_pending = get_object_or_404(BetPending, id=id)
    choice = request.POST.get("choice")

    if choice in ["y", "n", "hl"]:
        process_bet(bet_pending.stake, bet_pending.odd, choice, bet_pending.method)

        # Delete the BetPending object as it's no longer needed
        bet_pending.delete()

        # Redirect to stake view with POST data
        return redirect(reverse("stakes:stake"))
    else:
        # If no valid choice is provided, redirect back to the same page
        return redirect(request.META.get("HTTP_REFERER", reverse("stakes:stake")))


@require_http_methods(["GET", "POST"])
def update_bet(request, id):
    # Get the existing bet
    bet = get_object_or_404(Bet, id=id)

    if request.method == "POST":
        form = BetForm(request.POST)
        if form.is_valid():
            update_bet_service(
                id,
                form.cleaned_data["stake"],
                form.cleaned_data["odd"],
                form.cleaned_data["result"],
                form.cleaned_data["balance"],
                form.cleaned_data["next_stake"],
                form.cleaned_data["daily_profit"],
                form.cleaned_data["method"],
                form.cleaned_data["number_of_bets_day"],
            )
            return redirect(reverse("stakes:stake"))
        else:
            return render(request, "stakes/stake.html", {"form": form})
    else:
        # Prepopulate the form with existing bet data
        initial_data = {
            "stake": bet.stake,
            "odd": bet.odd,
            "result": bet.result,
            "balance": bet.balance,
            "next_stake": bet.next_stake,
            "daily_profit": bet.daily_profit,
            "nextState": bet.nextState,
            "method": bet.method,
            "number_of_bets_day": bet.number_of_bets_day,
        }
        form = BetForm(initial=initial_data)
        return render(request, "stakes/betform.html", {"form": form, "id": id})


@require_http_methods(["POST"])
def delete_bet(request, id):
    delete_bet_service(id)
    return redirect(reverse("stakes:stake"))
