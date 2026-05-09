from django.db.models import Sum, Avg, Count, Q
from .models import Trade, TradeAnalytics

class PortfolioAnalyzer:
    @staticmethod
    def get_multi_account_stats(user_ids):
        """Aggregate stats across multiple accounts"""
        trades = Trade.objects.filter(user_id__in=user_ids)
        
        total_trades = trades.count()
        total_pnl = trades.aggregate(Sum('pnl'))['pnl__sum'] or 0
        wins = trades.filter(pnl__gt=0).count()
        
        return {
            'total_trades': total_trades,
            'total_pnl': total_pnl,
            'win_rate': (wins / total_trades * 100) if total_trades > 0 else 0,
            'accounts': len(user_ids),
        }

    @staticmethod
    def get_account_comparison(user_ids):
        """Compare performance across accounts"""
        comparison = []
        
        for user_id in user_ids:
            analytics = TradeAnalytics.objects.filter(user_id=user_id).first()
            if analytics:
                comparison.append({
                    'user_id': user_id,
                    'total_trades': analytics.total_trades,
                    'win_rate': analytics.win_rate,
                    'profit_factor': analytics.profit_factor,
                    'expectancy': analytics.expectancy,
                })
        
        return sorted(comparison, key=lambda x: x['win_rate'], reverse=True)

    @staticmethod
    def get_portfolio_allocation(user_ids):
        """Get asset allocation across accounts"""
        trades = Trade.objects.filter(user_id__in=user_ids)
        
        allocation = {}
        for trade in trades:
            asset = trade.asset_pair
            if asset not in allocation:
                allocation[asset] = {'count': 0, 'pnl': 0}
            
            allocation[asset]['count'] += 1
            allocation[asset]['pnl'] += trade.pnl or 0
        
        return allocation

    @staticmethod
    def get_correlation_matrix(user_ids):
        """Calculate correlation between account performances"""
        analytics_list = TradeAnalytics.objects.filter(user_id__in=user_ids)
        
        correlations = {}
        for i, a1 in enumerate(analytics_list):
            for a2 in analytics_list[i+1:]:
                key = f"{a1.user_id}-{a2.user_id}"
                correlation = abs(a1.win_rate - a2.win_rate) / 100
                correlations[key] = correlation
        
        return correlations
