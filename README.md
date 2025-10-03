# Portfolio Tracker

A comprehensive portfolio tracking web application for managing investment portfolios across multiple asset classes, currencies, and exchanges with advanced dividend tracking and forecasting capabilities.

## Features

- Multi-currency portfolio management
- Real-time market data integration
- Advanced dividend tracking and forecasting
- Corporate actions handling
- Bulk transaction import
- Comprehensive analytics and reporting
- Mobile-responsive design
- Social features and community insights

## Tech Stack

### Frontend
- React 18 with TypeScript
- Vite for build tooling
- Tailwind CSS for styling
- Chart.js for visualizations
- React Query for state management
- React Router for navigation

### Backend
- Node.js with Express
- TypeScript
- PostgreSQL with TimescaleDB
- Redis for caching
- JWT authentication
- Docker for containerization

## Getting Started

### Prerequisites

- Node.js 18+ and npm 9+
- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/portfolio-tracker.git
cd portfolio-tracker
```

2. Copy environment files:
```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

3. Install dependencies and start development environment:
```bash
npm run setup
```

This will:
- Install all dependencies for frontend and backend
- Start PostgreSQL and Redis containers
- Start both frontend and backend development servers

### Development Commands

```bash
# Start all services
npm run dev

# Start only database services
npm run db:up

# Start backend only
npm run dev:backend

# Start frontend only
npm run dev:frontend

# Run tests
npm run test

# Build for production
npm run build

# Lint code
npm run lint

# Docker commands
npm run docker:up    # Start all containers
npm run docker:down  # Stop all containers
npm run docker:logs  # View logs
```

### Project Structure

```
portfolio-tracker/
├── frontend/          # React TypeScript frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
├── backend/           # Node.js Express backend
│   ├── src/
│   ├── package.json
│   └── tsconfig.json
├── docker/            # Docker configuration
│   └── postgres/
├── docker-compose.yml # Development environment
└── package.json       # Root package.json
```

## Development

### Database

The application uses PostgreSQL with TimescaleDB extension for time-series data. The database is automatically initialized when you run `npm run setup`.

### API Documentation

API documentation will be available at `http://localhost:3001/api/docs` when the backend is running.

### Testing

Run tests with:
```bash
npm run test           # Run all tests
npm run test:backend   # Backend tests only
npm run test:frontend  # Frontend tests only
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run linting and tests
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.