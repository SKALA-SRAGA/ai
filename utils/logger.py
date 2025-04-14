import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from config import settings

# 로그 디렉토리 생성
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# 로거 생성
logger = logging.getLogger("receipt_processor")
logger.setLevel(logging.INFO)

# 로그 포맷 설정
log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 파일 핸들러 설정 (10MB 크기, 최대 5개 파일 유지)
file_handler = RotatingFileHandler(
    log_dir / "receipt_processor.log",
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5,
    encoding="utf-8",
)
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.INFO)

# 콘솔 핸들러 설정
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
console_handler.setLevel(logging.INFO)

# 핸들러 추가
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# 로깅 함수들
def log_request(endpoint: str, files: list):
    """API 요청 로깅"""
    logger.info(f"Received request at {endpoint} with {len(files)} files")


def log_process_start(process_name: str):
    """프로세스 시작 로깅"""
    logger.info(f"Starting process: {process_name}")


def log_process_complete(process_name: str):
    """프로세스 완료 로깅"""
    logger.info(f"Completed process: {process_name}")


def log_error(error: Exception, context: str = None):
    """에러 로깅"""
    if context:
        logger.error(f"Error in {context}: {str(error)}")
    else:
        logger.error(str(error))


def log_warning(message: str):
    """경고 로깅"""
    logger.warning(message)
