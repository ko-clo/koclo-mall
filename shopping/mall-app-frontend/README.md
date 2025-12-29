# KO&CLO Mall Frontend

SvelteKit 기반 쇼핑몰 프론트엔드

## Tech Stack

- **Framework**: SvelteKit 2 + Svelte 5
- **Styling**: Tailwind CSS 4
- **Auth**: Supabase Auth
- **Deploy**: Cloudflare Pages

## 주요 기능

### Consumer
- `/products` - 상품 목록 (카테고리 필터, 정렬)
- `/products/[slug]` - 상품 상세 (옵션 선택, 장바구니)
- `/auth/login` - 로그인 (소셜: 카카오, 네이버, 구글)
- `/auth/signup` - 회원가입
- `/my` - 마이페이지

### Admin
- `/admin` - 대시보드
- `/admin/products` - 상품 관리
- `/admin/products/new` - 상품 등록

## 개발 환경 설정

```bash
# 의존성 설치
pnpm install

# 개발 서버 실행
pnpm dev

# 빌드
pnpm build
```

## 환경 변수

```env
PUBLIC_SUPABASE_URL=https://xxx.supabase.co
PUBLIC_SUPABASE_ANON_KEY=eyJhbGci...
PUBLIC_SITE_URL=http://localhost:5173
```

## 배포

Cloudflare Pages에서 자동 배포 (main 브랜치 push 시)
