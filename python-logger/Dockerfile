FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create logs directory and set permissions
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

COPY logger.py .

# Create a non-root user for better security
RUN useradd -m appuser
USER appuser

# Volume for persistent logs
VOLUME /app/logs

CMD ["python", "logger.py"]