from django.db import models
from django.utils import timezone

class Trade(models.Model):
    SETUP_CHOICES = [
        ('breakout', 'Breakout'),
        ('mean_reversion', 'Mean Reversion'),
        ('trend_follow', 'Trend Following'),
        ('scalp', 'Scalping'),
    ]
    
    SESSION_CHOICES = [
        ('asian', 'Asian'),
        ('european', 'European'),
        ('us', 'US'),
    ]

    user_id = models.CharField(max_length=255)
    asset_pair = models.CharField(max_length=10)
    entry_price = models.DecimalField(max_digits=10, decimal_places=5)
    exit_price = models.DecimalField(max_digits=10, decimal_places=5)
    stop_loss = models.DecimalField(max_digits=10, decimal_places=5)
    take_profit = models.DecimalField(max_digits=10, decimal_places=5)
    setup_id = models.CharField(max_length=50, choices=SETUP_CHOICES)
    session = models.CharField(max_length=20, choices=SESSION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    pnl = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    on_chain_hash = models.CharField(max_length=255, null=True, blank=True)
    rr_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    duration_minutes = models.IntegerField(null=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user_id', '-timestamp']),
            models.Index(fields=['setup_id']),
        ]

    def __str__(self):
        return f"{self.asset_pair} {self.setup_id} @ {self.timestamp}"


class TradeAnalytics(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    total_trades = models.IntegerField(default=0)
    win_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    profit_factor = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    expectancy = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_drawdown = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    consecutive_wins = models.IntegerField(default=0)
    consecutive_losses = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analytics for {self.user_id}"


class PerformanceToken(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    token_id = models.CharField(max_length=255, null=True)
    win_rate_threshold = models.DecimalField(max_digits=5, decimal_places=2)
    minted_at = models.DateTimeField(auto_now_add=True)
    on_chain_address = models.CharField(max_length=255, null=True)
    stellar_tx_hash = models.CharField(max_length=255, null=True)
    stellar_public_key = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"Token for {self.user_id}"


class UserAccount(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    stellar_public_key = models.CharField(max_length=255, unique=True)
    stellar_secret_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Account for {self.user_id}"
