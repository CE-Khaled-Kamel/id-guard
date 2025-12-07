# 1. Start with a lightweight Linux + Python 3.10 image
FROM python:3.10-slim

# 2. Set Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set work directory
WORKDIR /app

# 4. Install System dependencies
# FIX: Replaced 'libgl1-mesa-glx' with 'libgl1' and 'libglib2.0-0'
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-ara \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. Copy project files
COPY . /app/

# This tells Docker: "Start the Production Server on Port 8000"
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]