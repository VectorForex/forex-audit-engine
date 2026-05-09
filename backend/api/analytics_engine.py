from decimal import Decimal
from datetime import timedelta

class AdvancedAnalytics:
    @staticmethod
    def calculate_sharpe_ratio(trades, risk_free_rate=0.02):
        """Calculate Sharpe ratio"""
        if not trades or len(trades) < 2:
            return 0
        
        returns = [t.pnl for t in trades]
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        std_dev = variance ** 0.5
        
        if std_dev == 0:
            return 0
        
        return (mean_return - risk_free_rate) / std_dev

    @staticmethod
    def calculate_recovery_factor(trades):
        """Calculate recovery factor (net profit / max drawdown)"""
        if not trades:
            return 0
        
        net_profit = sum(t.pnl for t in trades)
        max_dd = AdvancedAnalytics.calculate_mdd(trades)
        
        if max_dd == 0:
            return 0
        
        return net_profit / max_dd

    @staticmethod
    def calculate_mdd(trades):
        """Calculate maximum drawdown"""
        if not trades:
            return 0
        
        cumulative = 0
        peak = 0
        max_dd = 0
        
        for trade in trades:
            cumulative += trade.pnl
            if cumulative > peak:
                peak = cumulative
            dd = peak - cumulative
            if dd > max_dd:
                max_dd = dd
        
        return max_dd

    @staticmethod
    def detect_double_dipping(trades):
        """Detect correlated asset pairs traded simultaneously"""
        correlations = {
            'EUR': ['USD', 'GBP', 'CHF'],
            'USD': ['EUR', 'JPY', 'CHF'],
            'GBP': ['EUR', 'USD'],
            'JPY': ['USD'],
            'CHF': ['EUR', 'USD'],
        }
        
        flags = []
        for i, trade1 in enumerate(trades):
            for trade2 in trades[i+1:]:
                pair1_base = trade1.asset_pair[:3]
                pair1_quote = trade1.asset_pair[4:7]
                pair2_base = trade2.asset_pair[:3]
                pair2_quote = trade2.asset_pair[4:7]
                
                if (pair1_base in correlations.get(pair2_base, []) or
                    pair1_quote in correlations.get(pair2_quote, [])):
                    flags.append({
                        'trade1_id': trade1.id,
                        'trade2_id': trade2.id,
                        'pair1': trade1.asset_pair,
                        'pair2': trade2.asset_pair,
                    })
        
        return flags

    @staticmethod
    def calculate_time_of_day_stats(trades):
        """Analyze performance by time of day"""
        stats = {
            'asian': {'wins': 0, 'losses': 0, 'total': 0},
            'european': {'wins': 0, 'losses': 0, 'total': 0},
            'us': {'wins': 0, 'losses': 0, 'total': 0},
        }
        
        for trade in trades:
            session = trade.session.lower()
            if session in stats:
                stats[session]['total'] += 1
                if trade.pnl > 0:
                    stats[session]['wins'] += 1
                else:
                    stats[session]['losses'] += 1
        
        for session in stats:
            total = stats[session]['total']
            if total > 0:
                stats[session]['win_rate'] = (stats[session]['wins'] / total) * 100
            else:
                stats[session]['win_rate'] = 0
        
        return stats

    @staticmethod
    def identify_best_setups(trades, min_trades=5):
        """Identify most profitable setups"""
        setup_stats = {}
        
        for trade in trades:
            setup = trade.setup_id
            if setup not in setup_stats:
                setup_stats[setup] = {'trades': [], 'count': 0}
            
            setup_stats[setup]['trades'].append(trade)
            setup_stats[setup]['count'] += 1
        
        best_setups = []
        for setup, data in setup_stats.items():
            if data['count'] >= min_trades:
                wins = sum(1 for t in data['trades'] if t.pnl > 0)
                win_rate = (wins / data['count']) * 100
                avg_win = sum(t.pnl for t in data['trades'] if t.pnl > 0) / max(1, wins)
                
                best_setups.append({
                    'setup': setup,
                    'count': data['count'],
                    'win_rate': win_rate,
                    'avg_win': avg_win,
                })
        
        return sorted(best_setups, key=lambda x: x['win_rate'], reverse=True)
