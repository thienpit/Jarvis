FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements và install
# Build context là backend/, nên COPY path là relative đến backend/
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ứng dụng
COPY app ./app
COPY run.sh .
RUN chmod +x run.sh

# Tạo thư mục audio tạm
RUN mkdir -p /tmp/audio

# Export env vars mặc định
ENV HERMES_CLI_PATH=/app/hermes_agent/hermes_cli/main.py
ENV HERMES_CLI_TIMEOUT=30
ENV HERMES_CLI_WORKING_DIR=/app
ENV AUDIO_OUTPUT_DIR=/tmp/audio
ENV PORT=8000

EXPOSE 8000

CMD ["./run.sh"]
