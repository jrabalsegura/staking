from django.db import models

# Create your models here.

class Bet(models.Model):
    stake = models.FloatField()
    odd = models.FloatField()
    result = models.CharField(max_length=2, choices=[('y', 'Yes'), ('n', 'No'), ('hl', 'Half')])
    next_multiplier = models.FloatField()
    balance = models.FloatField()
    next_stake = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    daily_profit = models.FloatField(default=0)

    def __str__(self):
        return f"{self.stake} a {self.odd} - {self.result}"
    
class BetPending(models.Model):
    stake = models.FloatField()
    odd = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stake} a {self.odd}"