# Use a lightweight official Python base image
FROM python:3.12.5-alpine3.20

# Set environment variables for improved output and compatibility
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.local/bin:$PATH"

# Metadata for the image
LABEL maintainer="Nur Amin Sifat"

# Set the working directory
WORKDIR /app

# Install system dependencies needed for builds and runtime
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    libcurl \
    curl-dev \
    openssl

# Copy and install Python dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copy application source code
COPY . .

# Prepare for static files collection
RUN mkdir -p /staticfiles

# Remove unnecessary build tools to reduce image size
RUN apk del gcc musl-dev libffi-dev curl-dev

# Set the default command to run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
