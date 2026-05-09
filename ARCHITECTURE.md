# Forex Ledger Protocol - Project Structure

## Directory Layout

```
forex-audit-engine/
├── contracts/                 # Soroban Smart Contracts (Rust)
│   ├── Cargo.toml
│   └── src/
│       └── lib.rs            # Core analytics logic
├── backend/                   # Django REST API
│   ├── config/               # Django settings
│   ├── api/                  # Trade & analytics endpoints
│   │   ├── models.py         # Trade, TradeAnalytics
│   │   ├── views.py          # ViewSets
│   │   ├── serializers.py    # DRF serializers
│   │   ├── utils.py          # Parser, Hash, Calculator
│   │   └── admin.py
│   └── manage.py
├── frontend/                  # React Dashboard
│   ├── src/
│   │   ├── pages/            # Dashboard, Analytics, RedFlags
│   │   ├── components/       # Navigation, Charts
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
├── README.md
├── requirements.txt
├── docker-compose.yml
└── setup.sh
```

## Layer Breakdown

### 1. Data Ingestion (Backend)
- **TradeViewSet**: Upload CSV, parse trades
- **TradeParser**: MT4/MT5/cTrader format support
- **HashAnchor**: SHA-256 hashing + Stellar anchoring

### 2. Analytical Engine (Contracts)
- **ForexAnalytics**: R:R calculation, expectancy, MDD
- **Red Flag Detection**: Revenge trading, double-dipping, drawdown

### 3. Insights Dashboard (Frontend)
- **Dashboard**: CSV upload interface
- **Analytics**: Win rate, profit factor, setup performance
- **RedFlags**: Revenge trading, high drawdown alerts

## API Endpoints

```
POST   /api/trades/upload_csv/          # Upload trade history
POST   /api/trades/calculate_pnl/       # Calculate PnL
GET    /api/analytics/user_stats/       # User statistics
GET    /api/analytics/setup_performance/ # Setup breakdown
GET    /api/analytics/red_flags/        # Red flag detection
```

## Getting Started

1. Copy `.env.example` to `.env`
2. Run `bash setup.sh`
3. Start services:
   - Backend: `cd backend && python manage.py runserver`
   - Frontend: `cd frontend && npm start`
   - Or use Docker: `docker-compose up`

## Next Steps (40% remaining)

- [ ] Stellar SDK integration for hash anchoring
- [ ] Soroban contract deployment
- [ ] Performance token (SBT) minting
- [ ] Advanced heat map visualizations
- [ ] Zero-knowledge proof integration
- [ ] Multi-account portfolio analysis
- [ ] Leaderboard & social features
