# Multi-stage production build for Cyber Fraud Shield (Reflex App)
FROM python:3.12-slim as builder

# Install system dependencies, Node.js, and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    unzip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency requirements
COPY requirements.txt .

# Install CPU-optimized PyTorch to minimize image size, then install dependencies
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Initialize and compile production bundle
ENV REFLEX_ENV_MODE=prod
RUN reflex init
RUN reflex export --frontend-only --no-zip

# Production Runner Image
FROM python:3.12-slim

WORKDIR /app

# Install runtime curl for health checks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages & application artifacts from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

# Expose standard production port
ENV PORT=8000
EXPOSE 8000

# Start Reflex in production single-port mode
CMD ["sh", "-c", "reflex run --env prod --single-port --frontend-port $PORT --backend-port $PORT"]
