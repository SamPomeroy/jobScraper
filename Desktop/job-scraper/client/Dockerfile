# Stage 1: Build the Next.js app
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Install dependencies
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

# Copy the rest of the source code
COPY frontend .

# Build the app
RUN npm run build

# Stage 2: Run the app
FROM node:20-alpine AS runner

WORKDIR /app

# Copy build output and necessary files
COPY --from=builder /app/.next .next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./

# Install only production dependencies
RUN npm install --omit=dev

# Set environment variables and expose port
ENV NODE_ENV=production
EXPOSE 3000

# Start the app
CMD ["npm", "start"]
