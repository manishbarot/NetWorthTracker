# Portfolio Tracker Development Setup Script (PowerShell)

Write-Host "🚀 Setting up Portfolio Tracker development environment..." -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
try {
    $nodeVersion = node -v
    Write-Host "✅ Node.js version: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js is not installed. Please install Node.js 18+ and try again." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Prerequisites check passed" -ForegroundColor Green

# Copy environment files if they don't exist
if (-not (Test-Path ".env")) {
    Write-Host "📄 Copying .env.example to .env" -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
}

if (-not (Test-Path "backend/.env")) {
    Write-Host "📄 Copying backend/.env.example to backend/.env" -ForegroundColor Yellow
    Copy-Item "backend/.env.example" "backend/.env"
}

if (-not (Test-Path "frontend/.env")) {
    Write-Host "📄 Copying frontend/.env.example to frontend/.env" -ForegroundColor Yellow
    Copy-Item "frontend/.env.example" "frontend/.env"
}

Write-Host "✅ Environment files ready" -ForegroundColor Green

# Install dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow
npm install

Write-Host "📦 Installing backend dependencies..." -ForegroundColor Yellow
Set-Location backend
npm install
Set-Location ..

Write-Host "📦 Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location frontend
npm install
Set-Location ..

Write-Host "✅ Dependencies installed" -ForegroundColor Green

# Start Docker services
Write-Host "🐳 Starting Docker services..." -ForegroundColor Yellow
docker-compose up -d postgres redis

# Wait for services to be ready
Write-Host "⏳ Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "🎉 Development environment setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Available commands:" -ForegroundColor Cyan
Write-Host "  npm run dev          - Start both frontend and backend" -ForegroundColor White
Write-Host "  npm run dev:backend  - Start backend only" -ForegroundColor White
Write-Host "  npm run dev:frontend - Start frontend only" -ForegroundColor White
Write-Host "  npm run docker:logs  - View Docker logs" -ForegroundColor White
Write-Host "  npm run test         - Run all tests" -ForegroundColor White
Write-Host ""
Write-Host "URLs:" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  Backend:  http://localhost:3001" -ForegroundColor White
Write-Host "  API:      http://localhost:3001/api" -ForegroundColor White
Write-Host ""
Write-Host "To start development servers, run: npm run dev" -ForegroundColor Green