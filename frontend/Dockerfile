# Build Stage
FROM node:20-alpine AS build

WORKDIR /app

# Copy package manifests and install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code and build for production
COPY . .
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# Serve Stage using Nginx
FROM nginx:alpine

# Copy built dist files to Nginx web root
COPY --from=build /app/dist /usr/share/nginx/html

# Copy default nginx configuration if needed
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
