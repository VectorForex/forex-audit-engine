from django.contrib import admin
from .models import Trade, TradeAnalytics

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'asset_pair', 'setup_id', 'entry_price', 'exit_price', 'pnl', 'timestamp']
    list_filter = ['setup_id', 'asset_pair', 'timestamp']
    search_fields = ['user_id', 'asset_pair']

@admin.register(TradeAnalytics)
class TradeAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'total_trades', 'win_rate', 'profit_factor', 'expectancy', 'max_drawdown']
    readonly_fields = ['updated_at']
