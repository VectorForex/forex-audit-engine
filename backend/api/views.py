from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Trade, TradeAnalytics
from .serializers import TradeSerializer, TradeAnalyticsSerializer
from .utils import TradeParser, HashAnchor, AnalyticsCalculator

class TradeViewSet(viewsets.ModelViewSet):
    serializer_class = TradeSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Trade.objects.filter(user_id=user_id)
        return Trade.objects.all()

    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        """Upload and parse CSV trade history"""
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        user_id = request.data.get('user_id')
        
        try:
            trades_data = TradeParser.parse_csv(file)
            trades = []
            for trade_data in trades_data:
                trade = Trade.objects.create(
                    user_id=user_id,
                    **trade_data
                )
                trades.append(trade)
            
            # Hash and anchor
            trade_hash = HashAnchor.hash_trade_log(trades_data)
            
            return Response({
                'message': 'Trades uploaded successfully',
                'count': len(trades),
                'hash': trade_hash
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def calculate_pnl(self, request):
        """Calculate PnL for trades"""
        user_id = request.data.get('user_id')
        trades = Trade.objects.filter(user_id=user_id, pnl__isnull=True)
        
        for trade in trades:
            pnl = (trade.exit_price - trade.entry_price) * 100000  # Simplified
            trade.pnl = pnl
            trade.save()
        
        return Response({'updated': trades.count()})


class AnalyticsViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def user_stats(self, request):
        """Get analytics for a user"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        trades = Trade.objects.filter(user_id=user_id)
        
        analytics, _ = TradeAnalytics.objects.get_or_create(user_id=user_id)
        analytics.total_trades = trades.count()
        analytics.win_rate = AnalyticsCalculator.calculate_win_rate(trades)
        analytics.profit_factor = AnalyticsCalculator.calculate_profit_factor(trades)
        analytics.expectancy = AnalyticsCalculator.calculate_expectancy(trades)
        analytics.max_drawdown = AnalyticsCalculator.calculate_mdd(trades)
        analytics.save()
        
        serializer = TradeAnalyticsSerializer(analytics)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def setup_performance(self, request):
        """Get performance by setup type"""
        user_id = request.query_params.get('user_id')
        trades = Trade.objects.filter(user_id=user_id)
        
        setups = {}
        for setup in trades.values_list('setup_id', flat=True).distinct():
            setup_trades = trades.filter(setup_id=setup)
            setups[setup] = {
                'count': setup_trades.count(),
                'win_rate': AnalyticsCalculator.calculate_win_rate(setup_trades),
                'expectancy': AnalyticsCalculator.calculate_expectancy(setup_trades),
            }
        
        return Response(setups)

    @action(detail=False, methods=['get'])
    def red_flags(self, request):
        """Detect red flags in trading"""
        user_id = request.query_params.get('user_id')
        trades = Trade.objects.filter(user_id=user_id).order_by('timestamp')
        
        flags = {
            'revenge_trading': [],
            'high_drawdown': [],
            'low_win_rate_sessions': {},
        }
        
        for i, trade in enumerate(trades):
            if i > 0:
                prev_trade = trades[i - 1]
                if prev_trade.pnl < 0 and (trade.timestamp - prev_trade.timestamp).total_seconds() < 300:
                    flags['revenge_trading'].append(trade.id)
        
        mdd = AnalyticsCalculator.calculate_mdd(trades)
        if mdd > 1000:
            flags['high_drawdown'].append(mdd)
        
        return Response(flags)
