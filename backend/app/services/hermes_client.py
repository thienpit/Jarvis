import subprocess
import logging
from app.config import HERMES_CLI_PATH, HERMES_CLI_TIMEOUT, HERMES_CLI_WORKING_DIR

logger = logging.getLogger(__name__)

async def process_with_hermes(user_input: str) -> str:
    """
    Gọi Hermes CLI subprocess để xử lý input.
    Trả về response text từ Hermes.
    """
    try:
        cmd = [
            "python3",
            HERMES_CLI_PATH,
            "chat",
            "-q",
            user_input
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=HERMES_CLI_WORKING_DIR,
            timeout=HERMES_CLI_TIMEOUT
        )
        
        # Parse output — Hermes CLI trả hội thoại, lấy phần response
        output = result.stdout + result.stderr
        
        # Lấy dòng response (sau "╰───────────────────────────────────────────────────╯")
        lines = output.split('\n')
        response_lines = []
        capture = False
        for line in lines:
            if '╰' in line and '─' in line:
                capture = True
                continue
            if capture:
                stripped = line.strip()
                if stripped and not stripped.startswith('Resume'):
                    response_lines.append(stripped)
                elif not stripped:
                    break
        
        if response_lines:
            response = '\n'.join(response_lines).strip()
        else:
            # Fallback: lấy 200 ký tự cuối
            response = output[-500:].strip() if len(output) >= 500 else output.strip()
        
        if not response:
            response = "Jarvis chưa thể xử lý yêu cầu của bạn. Vui lòng thử lại."
        
        logger.info(f"Hermes response length: {len(response)}")
        return response
        
    except subprocess.TimeoutExpired:
        logger.warning(f"Hermes CLI timeout after {HERMES_CLI_TIMEOUT}s")
        return "Jarvis đang suy nghĩ lâu quá. Bạn thử lại nhé."
    except Exception as e:
        logger.error(f"Error calling Hermes CLI: {e}")
        return f"Jarvis gặp lỗi kỹ thuật: {str(e)[:100]}"
