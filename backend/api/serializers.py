from rest_framework import serializers
from .models import Trade, TradeAnalytics, PerformanceToken

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = [
            'id', 'user_id', 'asset_pair', 'entry_price', 'exit_price',
            'stop_loss', 'take_profit', 'setup_id', 'session', 'timestamp', 'pnl',
            'rr_ratio', 'duration_minutes'
        ]
        read_only_fields = ['id', 'timestamp', 'pnl', 'rr_ratio', 'duration_minutes']

class TradeAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeAnalytics
        fields = [
            'user_id', 'total_trades', 'win_rate', 'profit_factor',
            'expectancy', 'max_drawdown', 'consecutive_wins', 'consecutive_losses', 'updated_at'
        ]
        read_only_fields = ['updated_at']

class PerformanceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceToken
        fields = '__all__'
        read_only_fields = ['minted_at']
