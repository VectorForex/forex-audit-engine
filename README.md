# 🏗️ Forex Ledger Protocol
A decentralized Forex audit engine built on Stellar/Soroban that uses on-chain data analysis to calculate trade expectancy, identify high-risk setups, and help traders improve their win rate through verifiable performance metrics.

## 🎯 Core Problem
Forex traders lack a transparent, tamper-proof way to track performance and identify patterns that hurt profitability. Manual journaling is error-prone, and centralized platforms don't provide privacy or verifiable proof of trading skill.

## 🏛️ Three-Layer Architecture

### 1. Data Ingestion Layer (Off-Chain/Oracle)
**Purpose:** Bring Forex trade data from MT4/MT5/cTrader onto the Stellar ledger.

**Implementation:**
- CLI/web interface for uploading trade history (.csv/.json)
- Hash anchoring: Each trade log's hash is stored on-chain, proving data integrity
- Prevents tampering and creates an immutable audit trail

**Key Features:**
- Support for multiple broker formats
- Automatic data validation and normalization
- Cryptographic proof of data authenticity

---

### 2. Analytical Engine (Soroban Smart Contracts)
**Purpose:** Core pattern analysis and risk detection using Rust-based contracts.

**Pattern Attribution:**
- Categorizes trades by "Setup ID" (Breakout, Mean Reversion, etc.)
- Calculates Profit Factor and Trade Expectancy per setup
- Identifies correlations between trade outcomes and market conditions

**Red Flag Detection:**
- **Time-of-Day Risk:** Detects win rate drops during specific sessions (Asian, European, US)
- **Asset Correlation:** Identifies "double-dipping" (e.g., Long EUR/USD + Short USD/CHF)
- **Revenge Trading:** Flags trades opened within 5 minutes of a loss
- **Maximum Drawdown (MDD):** Alerts when daily loss threshold is exceeded

**Key Metrics Calculated:**
- Trade Expectancy: `E = (Win% × Avg Win) - (Loss% × Avg Loss)`
- Risk-to-Reward (R:R) Efficiency
- Win Rate by Setup, Session, and Asset
- Consecutive Win/Loss Streaks

---

### 3. Insights Dashboard (Win Rate Booster)
**Purpose:** Translate on-chain analytics into actionable trader insights.

**Features:**
- **Heat Maps:** Visualize win rates across days and trading sessions
- **Anti-Journal:** Blacklisted setups based on historical underperformance
- **Performance Tokens:** View minted SBTs proving trading skill to investors
- **Setup Recommendations:** High-probability vs. low-probability trade patterns
- **Risk Alerts:** Real-time warnings for dangerous trading behaviors

---

## 🛠️ Stellar Integration Features

| Feature | Stellar Implementation | Hackathon Value |
|---------|------------------------|-----------------|
| **Proof of Performance** | NFT/Soulbound Token (SBT) | Traders mint verifiable performance credentials without revealing strategy |
| **Data Privacy** | Zero-Knowledge Proofs (Optional) | Privacy-preserving analysis aligns with Stellar's innovation goals |
| **Trading Credits** | Custom "JOURNAL" Token | Gamify consistent logging; reward disciplined traders |
| **Immutable Audit Trail** | Ledger Hash Anchoring | Cryptographic proof of data integrity |

---

## 📊 Key Analysis Metrics

### Trade Expectancy
Calculates expected profit per trade:
```
E = (Win% × Avg Win) - (Loss% × Avg Loss)
```

### Risk-to-Reward Efficiency
Identifies if traders close winners early and let losers run.

### Maximum Drawdown Protection
Contract-based alerts trigger when daily loss threshold is exceeded.

### Setup Performance
Win rate, profit factor, and expectancy broken down by:
- Trade setup type
- Trading session (Asian, European, US)
- Asset pair
- Time of day

---

## 🚀 Implementation Roadmap

### Phase 1: Smart Contract (Rust/Soroban)
- [ ] Contract accepting entry, exit, stop_loss, take_profit inputs
- [ ] Calculate R:R ratio and trade expectancy
- [ ] Implement red flag detection logic
- [ ] Store trade metadata on-chain

### Phase 2: Data Ingestion (Python/Django CLI)
- [ ] Parse MT4/MT5/cTrader CSV exports
- [ ] Validate and normalize trade data
- [ ] Hash anchoring to Stellar ledger
- [ ] Push trade data to Soroban contracts via Stellar SDK

### Phase 3: Dashboard (Frontend)
- [ ] Heat map visualization (Chart.js)
- [ ] Setup performance rankings
- [ ] Anti-journal (blacklisted setups)
- [ ] Performance token minting interface
- [ ] Real-time risk alerts

### Phase 4: Advanced Features
- [ ] Zero-knowledge proof integration
- [ ] Multi-account portfolio analysis
- [ ] Predictive setup recommendations
- [ ] Leaderboard and social features

---

## 🔧 Tech Stack

- **Smart Contracts:** Rust + Soroban
- **Blockchain:** Stellar Network
- **Backend:** Python/Django
- **Frontend:** React/Vue + Chart.js
- **Data Format:** CSV/JSON
- **Cryptography:** SHA-256 hashing, ZK-proofs (optional)

---

## 📦 Getting Started

### Prerequisites
- Rust toolchain
- Stellar SDK
- Python 3.8+
- Node.js 16+

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/forex-ledger-protocol.git
cd forex-ledger-protocol

# Install dependencies
npm install
pip install -r requirements.txt
cargo build

# Deploy contracts to Stellar testnet
soroban contract deploy --network testnet
```

---

## 🎓 Why This Matters for Traders

1. **Transparency:** Verifiable proof of trading performance
2. **Accountability:** Immutable audit trail prevents data manipulation
3. **Improvement:** Data-driven insights identify profitable patterns
4. **Credibility:** Mint performance tokens to attract investors
5. **Discipline:** Gamified logging encourages consistent journaling

---

## 🏆 Hackathon Innovation Points

✅ **Decentralized Data Integrity:** Hash anchoring proves journal authenticity  
✅ **Advanced Analytics:** Pattern attribution and red flag detection  
✅ **Token Economics:** SBTs for performance proof, JOURNAL tokens for gamification  
✅ **Privacy-First:** Optional ZK-proof integration for sensitive data  
✅ **Real-World Impact:** Solves actual trader pain point  

---

## 📄 License
MIT

## 🤝 Contributing
Contributions welcome! Please open an issue or submit a pull request.

---

**Built for the Stellar Wave Drip Hackathon**
