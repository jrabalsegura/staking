from django.db import models

# Create your models here.

class Bet(models.Model):
    stake = models.FloatField()
    odd = models.FloatField()
    result = models.CharField(max_length=2, choices=[('y', 'Yes'), ('n', 'No'), ('hl', 'Half')])
    balance = models.FloatField()
    next_stake = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    daily_profit = models.FloatField(default=0)
    
    STATE_CHOICES = [
        ("<250", "<250"),
        ("250-500", "250-500"),
        ("500-1000", "500-1000"),
        ("1000-2000", "1000-2000"),
        ("2000-4000", "2000-4000"),
        ("4000-8000", "4000-8000"),
        ("8000-12000", "8000-12000"),
        ("12000-20000", "12000-20000"),
        ("20000-30000", "20000-30000"),
        ("30000-45000", "30000-45000"),
        ("45000-80000", "45000-80000"),
        (">80000", ">80000"),
    ]
    
    nextState = models.CharField(max_length=15, choices=STATE_CHOICES)

    def __str__(self):
        return f"{self.stake} a {self.odd} - {self.result}"
    
class BetPending(models.Model):
    stake = models.FloatField()
    odd = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.stake} a {self.odd}"