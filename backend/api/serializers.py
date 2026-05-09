from rest_framework import serializers
from .models import Trade, TradeAnalytics

class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = [
            'id', 'user_id', 'asset_pair', 'entry_price', 'exit_price',
            'stop_loss', 'take_profit', 'setup_id', 'session', 'timestamp', 'pnl'
        ]
        read_only_fields = ['id', 'timestamp', 'pnl']

class TradeAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeAnalytics
        fields = [
            'user_id', 'total_trades', 'win_rate', 'profit_factor',
            'expectancy', 'max_drawdown', 'updated_at'
        ]
        read_only_fields = ['updated_at']
