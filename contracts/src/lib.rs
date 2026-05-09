use soroban_sdk::{contract, contractimpl, Env, Symbol, Vec, Map};

#[derive(Clone)]
pub struct Trade {
    pub entry_price: i128,
    pub exit_price: i128,
    pub stop_loss: i128,
    pub take_profit: i128,
    pub setup_id: u32,
    pub timestamp: u64,
    pub asset_pair: Symbol,
    pub session: Symbol,
}

#[contract]
pub struct ForexAnalytics;

#[contractimpl]
impl ForexAnalytics {
    pub fn calculate_rr(entry: i128, exit: i128, stop_loss: i128, take_profit: i128) -> i128 {
        let risk = (entry - stop_loss).abs();
        let reward = (take_profit - entry).abs();
        if risk == 0 {
            return 0;
        }
        reward / risk
    }

    pub fn calculate_expectancy(
        win_rate: i128,
        avg_win: i128,
        avg_loss: i128,
    ) -> i128 {
        (win_rate * avg_win) / 100 - ((100 - win_rate) * avg_loss) / 100
    }

    pub fn detect_revenge_trading(
        last_trade_timestamp: u64,
        current_timestamp: u64,
        last_trade_profitable: bool,
    ) -> bool {
        !last_trade_profitable && (current_timestamp - last_trade_timestamp) < 300
    }

    pub fn detect_double_dipping(
        asset_pair_1: Symbol,
        asset_pair_2: Symbol,
    ) -> bool {
        // Simplified: check if both pairs share a common currency
        // EUR/USD and USD/CHF share USD
        false // Placeholder
    }

    pub fn calculate_mdd(trades: Vec<i128>) -> i128 {
        let mut peak = 0i128;
        let mut max_drawdown = 0i128;
        let mut cumulative = 0i128;

        for trade_pnl in trades.iter() {
            cumulative += trade_pnl;
            if cumulative > peak {
                peak = cumulative;
            }
            let drawdown = peak - cumulative;
            if drawdown > max_drawdown {
                max_drawdown = drawdown;
            }
        }
        max_drawdown
    }
}
