# PostgreSQL Setup for Parallel Diary

This document explains how to set up PostgreSQL for the Parallel Diary application.

## Prerequisites

- PostgreSQL installed on your system
- Basic knowledge of PostgreSQL administration

## Database Setup

1. Create a PostgreSQL database:

```sql
CREATE DATABASE parallel_diary;
```

2. Create a user (optional):

```sql
CREATE USER parallel_diary_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE parallel_diary TO parallel_diary_user;
```

## Environment Configuration

Add the following to your `.env` file (do not commit this file):

```
DATABASE_URL=postgresql://username:password@localhost/parallel_diary
```

Replace `username`, `password`, and `parallel_diary` with your actual PostgreSQL credentials and database name.

## Database Initialization

The application will automatically create all necessary tables on startup. No manual schema creation is required.

## Data Model

The application uses the following data model:

- **Users**: Stores user account information
- **DiaryEntries**: Stores diary entries with Japanese and translated English content
- **FavoriteExpressions**: Stores favorite expressions selected from diary entries

Each diary entry and favorite expression is associated with a specific user account.
