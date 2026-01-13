FROM python:3.13-slim
WORKDIR /app
# Install system dependencies (needed for cryptography/argon2 build)
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn strictly for prod
RUN pip install gunicorn

COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Use Gunicorn entrypoint
CMD ["gunicorn", "--workers=4", "--threads=2", "--timeout=120", "--bind=0.0.0.0:5000", "run:app"]
