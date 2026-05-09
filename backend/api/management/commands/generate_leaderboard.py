from django.core.management.base import BaseCommand
from api.models import TradeAnalytics

class Command(BaseCommand):
    help = 'Generate leaderboard rankings'

    def handle(self, *args, **options):
        analytics = TradeAnalytics.objects.all().order_by('-win_rate')[:100]
        
        self.stdout.write(self.style.SUCCESS('Top 10 Traders by Win Rate:'))
        for idx, entry in enumerate(analytics[:10], 1):
            self.stdout.write(
                f"{idx}. {entry.user_id}: {entry.win_rate:.2f}% WR | "
                f"PF: {entry.profit_factor:.2f} | E: ${entry.expectancy:.2f}"
            )
