-- Initialize Portfolio Tracker Database
-- This script sets up the basic database structure and extensions

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "timescaledb";

-- Create database user if not exists (for production)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'portfolio_user') THEN
        CREATE ROLE portfolio_user WITH LOGIN PASSWORD 'portfolio_password';
    END IF;
END
$$;

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON DATABASE portfolio_tracker TO portfolio_user;
GRANT ALL ON SCHEMA public TO portfolio_user;

-- Set timezone
SET timezone = 'UTC';

-- Create initial tables will be handled by migration scripts
-- This file just ensures the database is properly initialized