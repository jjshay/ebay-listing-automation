# eBay Listing Automation Docker Image
FROM python:3.11-slim

LABEL maintainer="John (JJ) Shay"
LABEL description="Automated eBay listing creation with AI"

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default command
CMD ["python", "demo.py"]
