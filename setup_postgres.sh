

set -e

echo "=== PostgreSQL Setup for Parallel Diary ==="
echo

if ! command -v psql &> /dev/null; then
    echo "PostgreSQL is not installed. Please install PostgreSQL first."
    echo "On Ubuntu: sudo apt-get update && sudo apt-get install -y postgresql postgresql-contrib"
    exit 1
fi

if ! pg_isready &> /dev/null; then
    echo "PostgreSQL service is not running. Please start it first."
    echo "On Ubuntu: sudo service postgresql start"
    exit 1
fi

DB_NAME="parallel_diary"
DB_USER="postgres"
DB_PASSWORD=""
DB_HOST="localhost"

read -p "Database name [$DB_NAME]: " input
DB_NAME=${input:-$DB_NAME}

read -p "Database user [$DB_USER]: " input
DB_USER=${input:-$DB_USER}

read -p "Database password: " DB_PASSWORD

read -p "Database host [$DB_HOST]: " input
DB_HOST=${input:-$DB_HOST}

echo
echo "Creating database $DB_NAME..."

if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "Database $DB_NAME already exists."
else
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
    echo "Database $DB_NAME created successfully."
fi

if [ "$DB_USER" != "postgres" ]; then
    if sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
        echo "User $DB_USER already exists."
    else
        sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
        echo "User $DB_USER created successfully."
    fi
    
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
    echo "Privileges granted to $DB_USER on $DB_NAME."
fi

ENV_FILE="$(pwd)/.env"
if [ -f "$ENV_FILE" ]; then
    if grep -q "DATABASE_URL" "$ENV_FILE"; then
        sed -i "s|DATABASE_URL=.*|DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST/$DB_NAME|" "$ENV_FILE"
    else
        echo "DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST/$DB_NAME" >> "$ENV_FILE"
    fi
    echo "Updated DATABASE_URL in .env file."
else
    echo "DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@$DB_HOST/$DB_NAME" > "$ENV_FILE"
    echo "Created .env file with DATABASE_URL."
fi

echo
echo "=== PostgreSQL Setup Complete ==="
echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo "Host: $DB_HOST"
echo
echo "To start the application:"
echo "1. Backend: cd backend && poetry install && poetry run uvicorn app.main:app --reload"
echo "2. Frontend: cd frontend && npm install && npm run dev"
echo
echo "The application will automatically create all necessary tables on startup."
