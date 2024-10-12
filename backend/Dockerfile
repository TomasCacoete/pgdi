# Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Copy project
COPY . .

EXPOSE 8000

# Run server
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000