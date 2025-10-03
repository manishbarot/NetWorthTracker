#!/bin/bash

# Portfolio Tracker Development Setup Script

echo "🚀 Setting up Portfolio Tracker development environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ and try again."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version 18+ is required. Current version: $(node -v)"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Copy environment files if they don't exist
if [ ! -f .env ]; then
    echo "📄 Copying .env.example to .env"
    cp .env.example .env
fi

if [ ! -f backend/.env ]; then
    echo "📄 Copying backend/.env.example to backend/.env"
    cp backend/.env.example backend/.env
fi

if [ ! -f frontend/.env ]; then
    echo "📄 Copying frontend/.env.example to frontend/.env"
    cp frontend/.env.example frontend/.env
fi

echo "✅ Environment files ready"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

echo "📦 Installing backend dependencies..."
cd backend && npm install && cd ..

echo "📦 Installing frontend dependencies..."
cd frontend && npm install && cd ..

echo "✅ Dependencies installed"

# Start Docker services
echo "🐳 Starting Docker services..."
docker-compose up -d postgres redis

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are healthy
if docker-compose ps | grep -q "healthy"; then
    echo "✅ Docker services are ready"
else
    echo "⚠️  Services may still be starting up. Check with: docker-compose logs"
fi

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "Available commands:"
echo "  npm run dev          - Start both frontend and backend"
echo "  npm run dev:backend  - Start backend only"
echo "  npm run dev:frontend - Start frontend only"
echo "  npm run docker:logs  - View Docker logs"
echo "  npm run test         - Run all tests"
echo ""
echo "URLs:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:3001"
echo "  API:      http://localhost:3001/api"
echo ""
echo "To start development servers, run: npm run dev"