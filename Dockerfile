# Stage 1: Prepare frontend static files
FROM node:20-slim AS frontend

WORKDIR /app
COPY package.json .
RUN npm install

RUN mkdir -p /app/public && cp -r ./node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/. /app/public/

# Stage 2: Application image
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Install nginx and gettext-base (for envsubst)
RUN apt-get update && apt-get install -y nginx gettext-base && rm -rf /var/lib/apt/lists/*

# Copy dependency files and install Python dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Copy built frontend static files
COPY --from=frontend /app/public /app/public

# Copy nginx config template and start script
COPY nginx.conf.template /etc/nginx/nginx.conf.template
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Port exposed by the container (Render sets PORT env var to 80)
EXPOSE 80

CMD ["/start.sh"]
