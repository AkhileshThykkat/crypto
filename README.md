# Crypto Project

This project fetches and stores cryptocurrency prices using Django, Celery, and Redis.

## Setup Instructions

### 1. Set Up Environment Variables
Create a `.env` file and add the following variables:

```ini
DATABASE_URL=postgresql://your_database_url
CELERY_URL=rediss://your_redis_url
```

### 2. Install Dependencies
Ensure you have Python installed, then run:

```sh
pip install -r requirements.txt
```

### 3. Apply Database Migrations
Run the following commands to set up the database:

```sh
python manage.py makemigrations
python manage.py migrate
```

### 4. Start the Django Server
Run the Django development server with:

```sh
python manage.py runserver
```

### 5. Start Celery Workers
Run the following commands in separate terminals:

```sh
celery -A crypto_project worker --loglevel=info
celery -A crypto_project beat --loglevel=info
```

