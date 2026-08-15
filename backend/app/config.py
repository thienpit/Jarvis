import os

# Hermes CLI configuration
HERMES_CLI_PATH = os.environ.get("HERMES_CLI_PATH", "/app/hermes_agent/hermes_cli/main.py")
HERMES_CLI_TIMEOUT = int(os.environ.get("HERMES_CLI_TIMEOUT", "30"))
HERMES_CLI_WORKING_DIR = os.environ.get("HERMES_CLI_WORKING_DIR", "/app")

# TTS configuration
TTS_VOICE = os.environ.get("TTS_VOICE", "vi-VN-NamMinhNeural")

# Server configuration
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))
