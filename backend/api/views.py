from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Trade, TradeAnalytics, PerformanceToken, UserAccount
from .serializers import TradeSerializer, TradeAnalyticsSerializer, PerformanceTokenSerializer, UserAccountSerializer
from .utils import TradeParser, HashAnchor, AnalyticsCalculator
from .stellar_client import StellarClient
from datetime import timedelta

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
            pnl = (trade.exit_price - trade.entry_price) * 100000
            trade.pnl = pnl
            trade.rr_ratio = AnalyticsCalculator.calculate_rr_ratio(
                trade.entry_price, trade.exit_price, trade.stop_loss, trade.take_profit
            )
            trade.save()
        
        return Response({'updated': trades.count()})

    @action(detail=False, methods=['get'])
    def by_session(self, request):
        """Get trades grouped by session"""
        user_id = request.query_params.get('user_id')
        trades = Trade.objects.filter(user_id=user_id)
        
        sessions = {}
        for session in ['asian', 'european', 'us']:
            session_trades = trades.filter(session=session)
            sessions[session] = {
                'count': session_trades.count(),
                'win_rate': AnalyticsCalculator.calculate_win_rate(session_trades),
            }
        return Response(sessions)


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
        analytics.consecutive_wins = AnalyticsCalculator.calculate_consecutive_wins(trades)
        analytics.consecutive_losses = AnalyticsCalculator.calculate_consecutive_losses(trades)
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
                'profit_factor': AnalyticsCalculator.calculate_profit_factor(setup_trades),
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


class PerformanceTokenViewSet(viewsets.ModelViewSet):
    serializer_class = PerformanceTokenSerializer
    queryset = PerformanceToken.objects.all()

    @action(detail=False, methods=['post'])
    def mint_token(self, request):
        """Mint performance token for user"""
        user_id = request.data.get('user_id')
        win_rate_threshold = request.data.get('win_rate_threshold', 55)
        
        analytics = TradeAnalytics.objects.get(user_id=user_id)
        if analytics.win_rate < win_rate_threshold:
            return Response(
                {'error': f'Win rate {analytics.win_rate}% below threshold {win_rate_threshold}%'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_account = UserAccount.objects.get(user_id=user_id)
            stellar_client = StellarClient()
            from stellar_sdk import Keypair
            keypair = Keypair.from_secret(user_account.stellar_secret_key)
            
            tx_hash = stellar_client.mint_performance_token(keypair, analytics.win_rate)
            
            token, created = PerformanceToken.objects.get_or_create(
                user_id=user_id,
                defaults={
                    'win_rate_threshold': win_rate_threshold,
                    'stellar_tx_hash': tx_hash,
                    'stellar_public_key': user_account.stellar_public_key,
                }
            )
            
            serializer = PerformanceTokenSerializer(token)
            return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        except UserAccount.DoesNotExist:
            return Response({'error': 'User account not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserAccountViewSet(viewsets.ModelViewSet):
    serializer_class = UserAccountSerializer
    queryset = UserAccount.objects.all()

    @action(detail=False, methods=['post'])
    def create_account(self, request):
        """Create Stellar account for user"""
        user_id = request.data.get('user_id')
        
        if UserAccount.objects.filter(user_id=user_id).exists():
            return Response({'error': 'Account already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        stellar_client = StellarClient()
        keys = stellar_client.create_account()
        
        account = UserAccount.objects.create(
            user_id=user_id,
            stellar_public_key=keys['public_key'],
            stellar_secret_key=keys['secret_key'],
        )
        
        serializer = UserAccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
