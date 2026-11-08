FROM python:3.11.18-slim-trixie

WORKDIR /app/

COPY src/ ./src/
COPY pyproject.toml uv.lock README.md .

RUN apt-get update \
&& apt-get install -y curl ca-certificates \
&& curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

RUN uv sync
