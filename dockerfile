FROM python:3.14-slim

# System dependencies
RUN apt-get update && \
    apt-get install -y \
        curl \
        ca-certificates \
        ffmpeg \
        unzip && \
    rm -rf /var/lib/apt/lists/*

COPY cookies.txt /app/cookies.txt
ENV YOUTUBE_COOKIES_FILE=/app/cookies.txt

# Install Azure CLI
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash



# Install Deno
RUN curl -fsSL https://deno.land/install.sh | sh

ENV DENO_INSTALL=/root/.deno
ENV PATH="${DENO_INSTALL}/bin:${PATH}"

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install project dependencies
RUN uv sync --frozen --no-dev

# Copy application source
COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "backend.src.api.server:app", "--host", "0.0.0.0", "--port", "8000"]