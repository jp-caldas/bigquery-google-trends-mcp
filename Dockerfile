FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src/ src/

ENV GOOGLE_CLOUD_PROJECT=""
ENV GOOGLE_APPLICATION_CREDENTIALS=""

ENTRYPOINT ["uv", "run", "mcp-google-trends"]
