"""
PostgreSQL Setup Script for Parallel Diary
This script sets up a PostgreSQL database for the Parallel Diary application
"""

import os
import sys
import argparse
import getpass
from dotenv import load_dotenv, set_key

try:
    import psycopg
except ImportError:
    print("Error: psycopg package not found. Please install it with:")
    print("  pip install psycopg[binary]")
    sys.exit(1)

def check_postgres_connection(host, user, password, dbname=None):
    """Check if PostgreSQL connection is possible"""
    try:
        conn_string = f"host={host} user={user}"
        if password:
            conn_string += f" password={password}"
        if dbname:
            conn_string += f" dbname={dbname}"
        
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()[0]
                print(f"Connected to PostgreSQL: {version}")
        return True
    except Exception as e:
        if dbname:
            print(f"Error connecting to database {dbname}: {e}")
        else:
            print(f"Error connecting to PostgreSQL: {e}")
        return False

def create_database(host, user, password, dbname):
    """Create PostgreSQL database if it doesn't exist"""
    try:
        conn_string = f"host={host} user={user}"
        if password:
            conn_string += f" password={password}"
        
        with psycopg.connect(conn_string) as conn:
            conn.autocommit = True
            
            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
                exists = cur.fetchone()
                
                if not exists:
                    print(f"Creating database {dbname}...")
                    cur.execute(f"CREATE DATABASE {dbname};")
                    print(f"Database {dbname} created successfully.")
                else:
                    print(f"Database {dbname} already exists.")
                
                if user != "postgres":
                    cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {dbname} TO {user};")
                    print(f"Privileges granted to {user} on {dbname}.")
        
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def update_env_file(host, user, password, dbname):
    """Update .env file with database connection string"""
    env_path = os.path.join(os.getcwd(), ".env")
    
    if not os.path.exists(env_path):
        with open(env_path, "w") as f:
            f.write("# Environment variables for Parallel Diary\n")
    
    load_dotenv(env_path)
    
    database_url = f"postgresql://{user}:{password}@{host}/{dbname}"
    
    set_key(env_path, "DATABASE_URL", database_url)
    print(f"Updated DATABASE_URL in .env file.")

def main():
    """Main function to set up PostgreSQL database"""
    parser = argparse.ArgumentParser(description="Set up PostgreSQL database for Parallel Diary")
    parser.add_argument("--host", default="localhost", help="PostgreSQL host (default: localhost)")
    parser.add_argument("--user", default="postgres", help="PostgreSQL user (default: postgres)")
    parser.add_argument("--dbname", default="parallel_diary", help="Database name (default: parallel_diary)")
    
    args = parser.parse_args()
    
    print("=== PostgreSQL Setup for Parallel Diary ===")
    print()
    
    password = getpass.getpass(f"Password for PostgreSQL user {args.user}: ")
    
    if not check_postgres_connection(args.host, args.user, password):
        print("Failed to connect to PostgreSQL. Please check your credentials and try again.")
        sys.exit(1)
    
    if not create_database(args.host, args.user, password, args.dbname):
        print("Failed to create database. Please check your credentials and try again.")
        sys.exit(1)
    
    if not check_postgres_connection(args.host, args.user, password, args.dbname):
        print("Failed to connect to the new database. Please check your credentials and try again.")
        sys.exit(1)
    
    update_env_file(args.host, args.user, password, args.dbname)
    
    print()
    print("=== PostgreSQL Setup Complete ===")
    print(f"Database: {args.dbname}")
    print(f"User: {args.user}")
    print(f"Host: {args.host}")
    print()
    print("To start the application:")
    print("1. Backend: cd backend && poetry install && poetry run uvicorn app.main:app --reload")
    print("2. Frontend: cd frontend && npm install && npm run dev")
    print()
    print("The application will automatically create all necessary tables on startup.")

if __name__ == "__main__":
    main()
