FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directory for SQLite database
RUN mkdir -p /data && chmod 777 /data

EXPOSE 5000

# Use shell form of CMD to run multiple commands
CMD flask db upgrade && python -m flask run --host=0.0.0.0 