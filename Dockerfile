# Base image: using the official Python image
FROM python:3.12

# Set environment variables to avoid Python buffering outputs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies for Apache and WSGI
RUN apt-get update && apt-get install -y \
    apache2 \
    apache2-dev \
    libapache2-mod-wsgi-py3 \
    && apt-get clean

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files to the container
COPY . /app/

# Collect static files (optional, for production)
RUN python manage.py collectstatic --noinput

# Copy Apache configuration file
COPY ./apache/apache-django.conf /etc/apache2/sites-available/000-default.conf

# Enable WSGI module
RUN a2enmod wsgi

# Expose port 80
EXPOSE 80

# Start Apache service
CMD ["apachectl", "-D", "FOREGROUND"]
