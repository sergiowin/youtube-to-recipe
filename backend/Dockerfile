FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create database directory and set permissions
RUN mkdir -p /app/instance && \
    chown -R nobody:nogroup /app/instance && \
    chmod -R 777 /app/instance

EXPOSE 5000

# Run as non-root user
USER nobody

CMD flask db upgrade && python -m flask run --host=0.0.0.0 