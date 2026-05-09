#!/bin/bash

echo "🚀 Setting up Forex Ledger Protocol..."

# Backend setup
echo "📦 Installing backend dependencies..."
cd backend
pip install -r ../requirements.txt
python manage.py migrate
cd ..

# Frontend setup
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Contracts setup
echo "🦀 Building Soroban contracts..."
cd contracts
cargo build --release
cd ..

echo "✅ Setup complete!"
echo ""
echo "To start development:"
echo "  Backend:  cd backend && python manage.py runserver"
echo "  Frontend: cd frontend && npm start"
