# Use Python 3.9 slim image (lightweight Python version)
FROM python:3.9-slim

# Install system packages needed for MySQL and Python packages
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev pkg-config gcc \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Set working directory inside container
WORKDIR /app

# Copy Python dependencies and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files to container
COPY . .

# Collect Django static files (for CSS, JS, etc.)
RUN python manage.py collectstatic --noinput

# Start Django app using Gunicorn on port 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
