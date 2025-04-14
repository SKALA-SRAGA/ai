from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from fastapi import HTTPException
from typing import List
import shutil
import os
from pathlib import Path
import json


from services.receipt_service import process_multiple_images
from services.docs_service import create_expense_report

app = FastAPI()

# 임시 저장소 경로
TEMP_DIR = Path("temp_images")
OUTPUT_DIR = Path("output")
TEMP_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


@app.post("/receipt")
async def process_receipts(
    files: List[UploadFile] = File(...), user_id: str = Form(...)
):
    """영수증 이미지를 처리하고 문서를 생성합니다."""

    # 임시 파일 저장
    image_paths = []
    try:
        # 파일 저장
        for file in files:
            temp_path = TEMP_DIR / file.filename
            with temp_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            image_paths.append(str(temp_path))

        # 이미지 처리 및 JSON 생성
        results = process_multiple_images(image_paths)
        json_path = TEMP_DIR / "receipt_results.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        # 문서 생성
        output_path = OUTPUT_DIR / f"{user_id}_expense_report.docx"
        create_expense_report(str(json_path), str(output_path))

        # 문서 반환
        return FileResponse(
            path=output_path,
            filename=f"{user_id}_expense_report.docx",
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    except Exception as e:
        return {"error": str(e)}
    finally:
        # 임시 파일 정리
        for path in image_paths:
            try:
                os.remove(path)
            except:
                pass
        try:
            if json_path.exists():
                os.remove(json_path)
        except:
            pass


@app.get("/download")
async def download_report(user_id: str = Query(...)):
    """생성된 문서를 다운로드합니다."""
    output_path = Path("output") / f"{user_id}_expense_report.docx"

    if not output_path.exists():
        raise HTTPException(status_code=404, detail="문서가 존재하지 않습니다.")

    return FileResponse(
        path=output_path,
        filename=f"{user_id}_expense_report.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
