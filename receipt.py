import argparse
import json
import subprocess
from pathlib import Path
from multimodal_copy import process_multiple_images
from docs import create_expense_report  # docs.py에 함수가 있어야 합니다.

if __name__ == "__main__":
    # 이미지 경로
    image_paths = [
        r"C:\Users\jjjjj\Desktop\skala_7\a\multimodal\japan_3_1.jpg",
        r"C:\Users\jjjjj\Desktop\skala_7\a\multimodal\japan_3_2.png",
        r"C:\Users\jjjjj\Desktop\skala_7\a\multimodal\japan_3_3.jpg",
        r"C:\Users\jjjjj\Desktop\skala_7\a\multimodal\japan_receipt.jpg",
    ]

    # 경로 설정
    parser = argparse.ArgumentParser(description="이미지 → JSON → 문서 자동화")
    parser.add_argument(
        "--json",
        "-j",
        default="5_receipt_results.json",
        help="중간 저장용 JSON 파일 경로",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="5_자동_출장비_내역서.docx",
        help="최종 생성될 Word 문서 경로",
    )
    args = parser.parse_args()

    # 이미지 처리
    print("[1단계] 이미지 분석 중...")
    results = process_multiple_images(image_paths)
    with open(args.json, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"JSON 저장 완료 → {args.json}")

    # 문서 생성
    print("[2단계] LLM 기반 문서 생성 중...")
    try:
        create_expense_report(args.json, args.output)
        print(f"문서 생성 완료 → {args.output}")
    except Exception as e:
        print(f"문서 생성 중 오류 발생: {e}")
        import traceback

        traceback.print_exc()
