import hashlib
import pandas as pd
from decimal import Decimal
from stellar_sdk import Server, Keypair, TransactionBuilder, Network
from django.conf import settings

class TradeParser:
    @staticmethod
    def parse_csv(file_path):
        """Parse MT4/MT5 CSV export"""
        df = pd.read_csv(file_path)
        trades = []
        for _, row in df.iterrows():
            trades.append({
                'asset_pair': row.get('Symbol', ''),
                'entry_price': Decimal(str(row.get('Open', 0))),
                'exit_price': Decimal(str(row.get('Close', 0))),
                'stop_loss': Decimal(str(row.get('StopLoss', 0))),
                'take_profit': Decimal(str(row.get('TakeProfit', 0))),
                'setup_id': row.get('Setup', 'unknown'),
                'timestamp': row.get('OpenTime', ''),
            })
        return trades

class HashAnchor:
    @staticmethod
    def hash_trade_log(trades):
        """Generate SHA-256 hash of trade log"""
        trade_str = str(sorted([(t['asset_pair'], t['entry_price']) for t in trades]))
        return hashlib.sha256(trade_str.encode()).hexdigest()

    @staticmethod
    def anchor_to_stellar(trade_hash, user_keypair):
        """Store hash on Stellar ledger"""
        server = Server(settings.STELLAR_SERVER)
        source_account = server.load_account(user_keypair.public_key)
        
        transaction = (
            TransactionBuilder(
                source_account=source_account,
                base_fee=100,
                network_passphrase=settings.STELLAR_NETWORK,
            )
            .add_text_memo(trade_hash[:28])
            .set_timeout(300)
            .build()
        )
        
        return transaction

class AnalyticsCalculator:
    @staticmethod
    def calculate_win_rate(trades):
        """Calculate win rate percentage"""
        if not trades:
            return 0
        wins = sum(1 for t in trades if t.pnl > 0)
        return (wins / len(trades)) * 100

    @staticmethod
    def calculate_profit_factor(trades):
        """Calculate profit factor"""
        gross_profit = sum(t.pnl for t in trades if t.pnl > 0)
        gross_loss = abs(sum(t.pnl for t in trades if t.pnl < 0))
        if gross_loss == 0:
            return 0
        return gross_profit / gross_loss

    @staticmethod
    def calculate_expectancy(trades):
        """Calculate trade expectancy"""
        if not trades:
            return 0
        avg_win = sum(t.pnl for t in trades if t.pnl > 0) / max(1, sum(1 for t in trades if t.pnl > 0))
        avg_loss = sum(t.pnl for t in trades if t.pnl < 0) / max(1, sum(1 for t in trades if t.pnl < 0))
        win_rate = AnalyticsCalculator.calculate_win_rate(trades)
        return (win_rate / 100 * avg_win) + ((1 - win_rate / 100) * avg_loss)

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
    def calculate_consecutive_wins(trades):
        """Calculate max consecutive wins"""
        if not trades:
            return 0
        max_streak = 0
        current_streak = 0
        for trade in trades:
            if trade.pnl > 0:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        return max_streak

    @staticmethod
    def calculate_consecutive_losses(trades):
        """Calculate max consecutive losses"""
        if not trades:
            return 0
        max_streak = 0
        current_streak = 0
        for trade in trades:
            if trade.pnl < 0:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
        return max_streak

    @staticmethod
    def calculate_rr_ratio(entry, exit_price, stop_loss, take_profit):
        """Calculate risk-to-reward ratio"""
        risk = abs(entry - stop_loss)
        reward = abs(take_profit - entry)
        if risk == 0:
            return 0
        return reward / risk
