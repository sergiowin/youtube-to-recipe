FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directory for JSON storage
RUN mkdir -p /app/data && \
    chown -R nobody:nogroup /app/data && \
    chmod -R 777 /app/data

EXPOSE 5000

# Run as non-root user
USER nobody

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"] 