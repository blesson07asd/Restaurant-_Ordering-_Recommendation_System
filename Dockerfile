# Use a Python 3.9 base image
FROM python:3.9-alpine

# Set environment variables for pip timeout
ENV PIP_DEFAULT_TIMEOUT=600

# Install build dependencies
RUN apk update && apk add --no-cache \
    build-base \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev \
    py3-pip \
    bash \
    make \
    libc-dev

# Set working directory
WORKDIR /app

# Copy application code
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --timeout=600 --index-url https://pypi.org/simple

# Set default command
CMD ["python", "v1.py"]