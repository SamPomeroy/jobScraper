FROM node:18-alpine

WORKDIR /app

# Install deps
COPY package*.json ./
RUN npm install

# Copy all source files
COPY . .

# Build and expose
RUN npm run build
EXPOSE 3000

CMD ["npm", "start"]