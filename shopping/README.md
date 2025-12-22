# ko&clo 쇼핑몰 기술 문서

**Version 1.0** | **2025-12-22**

---

## 📁 폴더 구조

```
docs_markdown/
├── README.md                    # 이 파일
├── TDD/
│   └── Shopping_Mall_TDD_v8.md  # Technical Design Document
├── PRD/
│   ├── PRD_비즈니스의사결정.md   # 핵심 의사결정 정리
│   ├── PRD-001_상품목록조회.md   # 상품 목록/검색 조회
│   ├── PRD-002_상품상세조회.md   # 상품 상세 (PDP)
│   ├── PRD-003_상품등록.md       # 상품 등록 (Admin)
│   ├── PRD-004_상품수정.md       # 상품 수정 (Admin)
│   ├── PRD-005_상품삭제.md       # 상품 삭제 (Admin)
│   ├── PRD-006_재고관리.md       # 재고 관리 (Admin)
│   └── PRD-007_카테고리관리.md   # 카테고리 관리 (Admin)
└── diagrams/
    ├── prd001_sequence_v2.png    # 상품 목록 조회 시퀀스
    ├── prd001_flow.png           # 상품 목록 플로우
    ├── prd002_sequence.png       # 상품 상세 조회 시퀀스
    ├── prd003_sequence.png       # 상품 등록 시퀀스
    └── prd004_sequence.png       # 상품 수정 시퀀스
```

---

## 📄 문서 목록

### TDD (Technical Design Document)

| 문서 | 설명 | 버전 |
|------|------|------|
| [Shopping_Mall_TDD_v8.md](TDD/Shopping_Mall_TDD_v8.md) | 전체 기술 설계 문서 | v1.8 |

### PRD (Product Requirements Document)

| 문서 | 설명 | 사용자 |
|------|------|--------|
| [PRD_비즈니스의사결정.md](PRD/PRD_비즈니스의사결정.md) | 8개 핵심 의사결정 | - |
| [PRD-001_상품목록조회.md](PRD/PRD-001_상품목록조회.md) | PLP/SRP 통합 조회 | Consumer |
| [PRD-002_상품상세조회.md](PRD/PRD-002_상품상세조회.md) | PDP 상세 페이지 | Consumer |
| [PRD-003_상품등록.md](PRD/PRD-003_상품등록.md) | 상품 등록 | Admin |
| [PRD-004_상품수정.md](PRD/PRD-004_상품수정.md) | 상품 수정 | Admin |
| [PRD-005_상품삭제.md](PRD/PRD-005_상품삭제.md) | 상품 삭제 (Soft Delete) | Admin |
| [PRD-006_재고관리.md](PRD/PRD-006_재고관리.md) | 재고 관리/동기화 | Admin |
| [PRD-007_카테고리관리.md](PRD/PRD-007_카테고리관리.md) | 카테고리 CRUD | Admin |

---

## 🔗 핵심 비즈니스 의사결정

| # | 의사결정 | 최종 결정 |
|---|----------|-----------|
| 1 | PLP/SRP 통합 | MVP 통합, Post-MVP 분리 검토 |
| 2 | 검색 MVP 범위 | PostgreSQL ILIKE만 |
| 3 | URL 구조 | 단일 라우트 /products/[...slug] |
| 4 | SKU 변경 정책 | 변경 가능 (Midas 동기화 주의) |
| 5 | 재고 흐름 | Midas → 쇼핑몰 (단방향) |
| 6 | 에디터 범위 | TipTap 기본 서식만 |
| 7 | 할인가 입력 | 직접 + 할인율 모두 지원 |
| 8 | 상품 구조 | 옵션 방식 (ProductGroup 불필요) |

---

## 🛠 기술 스택

| 구분 | 기술 |
|------|------|
| Frontend | SvelteKit, TypeScript, Tailwind CSS |
| Backend | FastAPI, Python 3.11+, SQLAlchemy 2.0 |
| Database | Supabase (PostgreSQL) |
| Storage | Cloudflare R2 |
| Payment | PortOne |
| Hosting | Vercel (FE), Railway (BE) |

---

## 📅 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2025-12-20 | 초기 버전 |
| 1.6 | 2025-12-21 | 회원 관리 상세 추가 |
| 1.8 | 2025-12-22 | 상품 관리 PRD 상세 추가 |

---

## 📞 문의

- 프로젝트: ko&clo 쇼핑몰
- 담당: ko&clo 개발팀
