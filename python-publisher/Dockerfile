FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY publisher.py .

# Create a non-root user for better security
RUN useradd -m appuser
USER appuser

CMD ["python", "publisher.py"]