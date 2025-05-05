FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

# Configure Vite to listen on all interfaces
ENV VITE_HOST=0.0.0.0
ENV VITE_PORT=5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"] 