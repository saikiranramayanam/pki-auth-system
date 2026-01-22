FROM python:3.10-slim

ENV TZ=UTC
WORKDIR /app

# Install only required system packages
RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
    && ln -fs /usr/share/zoneinfo/UTC /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app/ app/
COPY scripts/ scripts/
COPY cron/ cron/
COPY student_private.pem .
COPY student_public.pem .
COPY instructor_public.pem .

# Create required directories
RUN mkdir -p /data /cron

# Setup cron job
RUN chmod 0644 cron/2fa-cron && crontab cron/2fa-cron

EXPOSE 8080

CMD service cron start && uvicorn app.main:app --host 0.0.0.0 --port 8080
