from django.contrib import admin
from .models import Bet, BetPending
# Register your models here.

class BetAdmin(admin.ModelAdmin):
    list_display = ('stake', 'odd', 'result', 'balance', 'next_stake', 'created_at', 'nextState', 'method')
    list_filter = ('result', 'created_at', 'odd')

class BetPendingAdmin(admin.ModelAdmin):
    list_display = ('stake', 'odd', 'created_at')

admin.site.register(Bet, BetAdmin)
admin.site.register(BetPending, BetPendingAdmin)
