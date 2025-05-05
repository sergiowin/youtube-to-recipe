FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create instance directory for SQLite database
RUN mkdir -p /app/instance && chmod 777 /app/instance

EXPOSE 5000

CMD flask db upgrade && python -m flask run --host=0.0.0.0 