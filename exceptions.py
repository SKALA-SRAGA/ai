from fastapi import HTTPException
from typing import Any


class ReceiptProcessingError(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(
            status_code=400, detail=detail or "영수증 처리 중 오류가 발생했습니다."
        )


class DocumentGenerationError(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(
            status_code=400, detail=detail or "문서 생성 중 오류가 발생했습니다."
        )


class FileUploadError(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(
            status_code=400, detail=detail or "파일 업로드 중 오류가 발생했습니다."
        )


class InvalidFileTypeError(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(
            status_code=400, detail=detail or "지원하지 않는 파일 형식입니다."
        )
