FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directory for SQLite database
RUN mkdir -p /data && chmod 777 /data

EXPOSE 5000

# Create startup script
RUN echo '#!/bin/bash\nflask db upgrade\npython -m flask run --host=0.0.0.0' > /app/start.sh && \
    chmod +x /app/start.sh

CMD ["/app/start.sh"] 