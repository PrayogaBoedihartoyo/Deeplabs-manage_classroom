#!/bin/bash

echo "Setting up Django Project..."

# Clone the Repository
git clone https://github.com/your-username/your-django-project.git
cd your-django-project

# Create Virtual Environment
python -m venv venv

# Activate Virtual Environment
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

# Apply Migrations
python manage.py migrate

# Create Superuser
python manage.py createsuperuser

# Run the Development Server
python manage.py runserver

echo "Django Project setup completed."
echo "Visit http://127.0.0.1:8000/ to access the development server."
