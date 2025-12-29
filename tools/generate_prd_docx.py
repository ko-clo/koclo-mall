#!/usr/bin/env python3
"""
PRD 마크다운 파일들을 하나의 DOCX 파일로 변환하는 스크립트

사용법:
    python tools/generate_prd_docx.py

필수 요구사항:
    - pandoc: brew install pandoc
    - mermaid-cli: npm install -g @mermaid-js/mermaid-cli

출력:
    docs/shopping/PRD/Shopping_Mall_PRD.docx
"""

import subprocess
import sys
import tempfile
import re
import shutil
from pathlib import Path
from datetime import datetime


# PRD 파일 순서 정의
PRD_FILES = [
    "Shopping_Mall_PRD.md",    # 1. 개요/목차
    "MBR_회원관리.md",          # 2. 회원관리
    "PRD_상품관리.md",          # 3. 상품관리
    "CART_장바구니.md",         # 4. 장바구니
    "ORD_주문결제.md",          # 5. 주문결제
    "ADDR_배송지관리.md",       # 6. 배송지관리
    "SHP_배송.md",             # 7. 배송
    "PROMO_프로모션.md",        # 8. 프로모션
    "CS_고객센터.md",           # 9. 고객센터
]


def check_dependencies():
    """필수 도구 설치 여부 확인"""
    missing = []

    # pandoc 확인
    try:
        result = subprocess.run(["pandoc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"  ✓ {version}")
    except FileNotFoundError:
        missing.append("pandoc (brew install pandoc)")

    # mmdc 확인
    try:
        result = subprocess.run(["mmdc", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"  ✓ mermaid-cli {result.stdout.strip()}")
    except FileNotFoundError:
        missing.append("mermaid-cli (npm install -g @mermaid-js/mermaid-cli)")

    if missing:
        print("\n✗ 다음 도구가 필요합니다:")
        for tool in missing:
            print(f"    - {tool}")
        return False

    return True


def render_mermaid_to_png(mermaid_code: str, output_path: Path) -> bool:
    """Mermaid 코드를 PNG 이미지로 렌더링"""
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.mmd',
        encoding='utf-8',
        delete=False
    ) as f:
        f.write(mermaid_code)
        temp_mmd = f.name

    try:
        result = subprocess.run(
            [
                "mmdc",
                "-i", temp_mmd,
                "-o", str(output_path),
                "-b", "white",           # 흰색 배경
                "-t", "default",         # 기본 테마
                "-s", "2",               # 스케일 2x (고해상도)
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0 and output_path.exists()
    except Exception as e:
        print(f"    ⚠ Mermaid 렌더링 실패: {e}")
        return False
    finally:
        Path(temp_mmd).unlink(missing_ok=True)


def process_mermaid_blocks(content: str, images_dir: Path, file_prefix: str) -> str:
    """Mermaid 블록을 이미지로 변환하고 마크다운 참조로 대체"""
    pattern = r'```mermaid\n(.*?)```'
    diagram_count = 0

    def replace_with_image(match):
        nonlocal diagram_count
        diagram_count += 1
        mermaid_code = match.group(1)

        # 이미지 파일명
        image_name = f"{file_prefix}_diagram_{diagram_count}.png"
        image_path = images_dir / image_name

        # Mermaid를 PNG로 렌더링
        if render_mermaid_to_png(mermaid_code, image_path):
            # 마크다운 이미지 참조로 대체
            return f"\n![다이어그램 {diagram_count}]({image_path})\n"
        else:
            # 렌더링 실패 시 플레이스홀더
            return "\n*[다이어그램 렌더링 실패 - 원본 마크다운 참조]*\n"

    return re.sub(pattern, replace_with_image, content, flags=re.DOTALL)


def add_page_break() -> str:
    """페이지 구분을 위한 마크다운 추가"""
    return "\n\n---\n\n\\newpage\n\n"


def merge_prd_files(prd_dir: Path, images_dir: Path) -> str:
    """PRD 파일들을 하나의 마크다운으로 병합"""
    merged_content = []

    # 헤더 추가
    merged_content.append(f"""---
title: "Ko & Clo 쇼핑몰 PRD (Product Requirements Document)"
author: "ko&clo Project"
date: "{datetime.now().strftime('%Y-%m-%d')}"
---

""")

    for i, filename in enumerate(PRD_FILES):
        filepath = prd_dir / filename

        if not filepath.exists():
            print(f"  ⚠ 파일 없음: {filename}")
            continue

        print(f"  ✓ {filename}", end="", flush=True)

        content = filepath.read_text(encoding='utf-8')

        # 파일명에서 prefix 추출 (확장자 제외)
        file_prefix = filepath.stem

        # Mermaid 블록을 이미지로 변환
        original_content = content
        content = process_mermaid_blocks(content, images_dir, file_prefix)

        # 다이어그램 개수 표시
        diagram_count = original_content.count("```mermaid")
        if diagram_count > 0:
            print(f" ({diagram_count} diagrams)")
        else:
            print()

        merged_content.append(content)

        # 마지막 파일이 아니면 페이지 구분 추가
        if i < len(PRD_FILES) - 1:
            merged_content.append(add_page_break())

    return "\n".join(merged_content)


def generate_docx(merged_md: str, output_path: Path, images_dir: Path):
    """pandoc을 사용해 DOCX 생성"""

    # 임시 마크다운 파일 생성
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.md',
        encoding='utf-8',
        delete=False
    ) as f:
        f.write(merged_md)
        temp_md_path = f.name

    try:
        # pandoc 실행
        cmd = [
            "pandoc",
            temp_md_path,
            "-o", str(output_path),
            "--from", "markdown",
            "--to", "docx",
            "--standalone",
            "--resource-path", str(images_dir),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"✗ pandoc 오류: {result.stderr}")
            return False

        return True

    finally:
        Path(temp_md_path).unlink(missing_ok=True)


def main():
    print("=" * 50)
    print("PRD → DOCX 변환 스크립트 (with Mermaid diagrams)")
    print("=" * 50)
    print()

    # 1. 의존성 확인
    print("[1/4] 의존성 확인...")
    if not check_dependencies():
        sys.exit(1)
    print()

    # 2. 경로 설정
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    prd_dir = project_root / "docs" / "shopping" / "PRD"
    output_path = prd_dir / "Shopping_Mall_PRD.docx"

    # 임시 이미지 디렉토리
    images_dir = prd_dir / ".diagrams"
    images_dir.mkdir(exist_ok=True)

    if not prd_dir.exists():
        print(f"✗ PRD 디렉토리를 찾을 수 없습니다: {prd_dir}")
        sys.exit(1)

    # 3. 파일 병합 (Mermaid → PNG 변환 포함)
    print("[2/4] PRD 파일 병합 및 다이어그램 렌더링...")
    merged_md = merge_prd_files(prd_dir, images_dir)
    print()

    # 4. DOCX 생성
    print("[3/4] DOCX 생성...")
    if generate_docx(merged_md, output_path, images_dir):
        print(f"✓ 생성 완료: {output_path}")
        print()
        print(f"파일 크기: {output_path.stat().st_size / 1024:.1f} KB")
    else:
        print("✗ DOCX 생성 실패")
        sys.exit(1)

    # 5. 임시 이미지 정리
    print()
    print("[4/4] 임시 파일 정리...")
    shutil.rmtree(images_dir, ignore_errors=True)
    print("✓ 완료")


if __name__ == "__main__":
    main()
