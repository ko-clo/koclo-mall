# 배포 전략 및 인프라 (Infrastructure & Deployment)

**Version 1.0** | **2025-12-25** | **ko&clo Project**

---

## 목차

1. [개요](#1-개요)
2. [인프라 구성](#2-인프라-구성)
3. [CI/CD 파이프라인](#3-cicd-파이프라인)
4. [환경 구성](#4-환경-구성)
5. [비용 분석](#5-비용-분석)
6. [모니터링](#6-모니터링)

---

## 1. 개요

> **하위 목차**
> - [1.1 인프라 목표](#11-인프라-목표)
> - [1.2 기술 스택 요약](#12-기술-스택-요약)

### 1.1 인프라 목표

| 목표 | 내용 |
|------|------|
| 저비용 | 월 $0~10 운영 비용 |
| 확장성 | 트래픽 증가에 따른 자동 스케일링 |
| 안정성 | 99.9% 가용성 목표 |
| 보안 | HTTPS, 데이터 암호화 |

### 1.2 기술 스택 요약

| 구분 | 서비스 | 용도 |
|------|--------|------|
| FE Hosting | Vercel | SvelteKit 배포 |
| BE Hosting | Railway | FastAPI 컨테이너 |
| Database | Supabase | PostgreSQL + Auth |
| Storage | Cloudflare R2 | 이미지 저장소 |
| Payment | PortOne | PG 통합 결제 |
| DNS | Cloudflare | 도메인 관리 |

---

## 2. 인프라 구성

> **하위 목차**
> - [2.1 전체 아키텍처](#21-전체-아키텍처)
> - [2.2 서비스별 역할](#22-서비스별-역할)

### 2.1 전체 아키텍처

```mermaid
flowchart TB
    subgraph Users["Users"]
        Browser["Browser"]
        Mobile["Mobile"]
    end

    subgraph CDN["Cloudflare"]
        DNS["DNS"]
        Cache["Edge Cache"]
    end

    subgraph Vercel["Vercel"]
        Edge["Edge Functions"]
        SSR["SSR (SvelteKit)"]
        Static["Static Assets"]
    end

    subgraph Railway["Railway"]
        API["FastAPI Container"]
    end

    subgraph Supabase["Supabase"]
        Auth["Auth Service"]
        DB[("PostgreSQL")]
        Realtime["Realtime"]
    end

    subgraph Cloudflare_R2["Cloudflare R2"]
        Images["Product Images"]
        Uploads["User Uploads"]
    end

    subgraph External["External"]
        PortOne["PortOne (PG)"]
    end

    Users --> CDN
    CDN --> Vercel
    Vercel --> Railway
    Railway --> Supabase
    Railway --> PortOne
    Vercel --> Supabase
    Vercel --> Cloudflare_R2
    Railway --> Cloudflare_R2
```

### 2.2 서비스별 역할

```mermaid
flowchart LR
    subgraph Frontend["Frontend Layer"]
        V1["정적 파일 서빙"]
        V2["SSR 렌더링"]
        V3["BFF API Routes"]
        V4["Edge Functions"]
    end

    subgraph Backend["Backend Layer"]
        R1["비즈니스 로직"]
        R2["DB 트랜잭션"]
        R3["외부 API 연동"]
    end

    subgraph Data["Data Layer"]
        S1["PostgreSQL"]
        S2["인증/세션"]
        S3["Realtime 구독"]
    end

    subgraph Storage["Storage Layer"]
        C1["이미지 저장"]
        C2["CDN 배포"]
    end

    Frontend --> Backend --> Data
    Backend --> Storage
```

---

## 3. CI/CD 파이프라인

> **하위 목차**
> - [3.1 배포 흐름](#31-배포-흐름)
> - [3.2 브랜치 전략](#32-브랜치-전략)
> - [3.3 GitHub Actions 워크플로우](#33-github-actions-워크플로우)
> - [3.4 배포 상태 흐름](#34-배포-상태-흐름)

### 3.1 배포 흐름

```mermaid
flowchart LR
    subgraph Trigger["Trigger"]
        Push["Push to main"]
        PR["Pull Request"]
    end

    subgraph CI["CI (GitHub Actions)"]
        Lint["Lint"]
        Test["Test"]
        Build["Build"]
    end

    subgraph CD["CD (Auto Deploy)"]
        Vercel["Vercel"]
        Railway["Railway"]
        Supabase["Supabase Migrations"]
    end

    Push --> Lint --> Test --> Build
    Build --> Vercel & Railway & Supabase
    PR --> Lint --> Test
    Test --> Preview["Preview Deploy"]
```

### 3.2 브랜치 전략

```mermaid
gitgraph
    commit id: "init"
    branch develop
    checkout develop
    commit id: "feature-1"
    commit id: "feature-2"
    checkout main
    merge develop id: "release-1.0"
    checkout develop
    commit id: "feature-3"
    branch feature/auth
    commit id: "auth-1"
    commit id: "auth-2"
    checkout develop
    merge feature/auth id: "merge-auth"
    checkout main
    merge develop id: "release-1.1"
```

| 브랜치 | 용도 | 배포 환경 |
|--------|------|-----------|
| main | 프로덕션 릴리즈 | Production |
| develop | 개발 통합 | Staging |
| feature/* | 기능 개발 | Preview |
| hotfix/* | 긴급 수정 | Production |

### 3.3 GitHub Actions 워크플로우

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run lint

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm run test

  deploy-frontend:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

### 3.4 배포 상태 흐름

```mermaid
stateDiagram-v2
    [*] --> Pending: Push/PR

    Pending --> Running: CI 시작
    Running --> Lint: Lint 검사
    Lint --> Test: 테스트 실행

    Test --> Build: 빌드
    Test --> Failed: 테스트 실패

    Build --> Deploying: 배포 시작
    Build --> Failed: 빌드 실패

    Deploying --> Success: 배포 완료
    Deploying --> Failed: 배포 실패

    Failed --> [*]: 알림 발송
    Success --> [*]: 완료
```

---

## 4. 환경 구성

> **하위 목차**
> - [4.1 환경 분리](#41-환경-분리)
> - [4.2 환경 변수](#42-환경-변수)
> - [4.3 시크릿 관리](#43-시크릿-관리)

### 4.1 환경 분리

| 환경 | 도메인 | 용도 |
|------|--------|------|
| Production | koclo.kr | 실서비스 |
| Staging | staging.koclo.kr | QA/테스트 |
| Preview | *.vercel.app | PR 미리보기 |
| Local | localhost:3000 | 개발 |

### 4.2 환경 변수

#### Frontend (.env)

```bash
# Supabase
PUBLIC_SUPABASE_URL=https://xxx.supabase.co
PUBLIC_SUPABASE_ANON_KEY=eyJxxx...

# API
PUBLIC_API_URL=https://api.koclo.kr

# PortOne
PUBLIC_PORTONE_IMP_CODE=imp12345678

# R2
PUBLIC_R2_URL=https://images.koclo.kr
```

#### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=eyJxxx...
SUPABASE_JWT_SECRET=your-jwt-secret

# PortOne
PORTONE_API_KEY=your-api-key
PORTONE_API_SECRET=your-api-secret

# R2
R2_ACCOUNT_ID=xxx
R2_ACCESS_KEY_ID=xxx
R2_SECRET_ACCESS_KEY=xxx
R2_BUCKET_NAME=koclo-images
```

### 4.3 시크릿 관리

```mermaid
flowchart TB
    subgraph Sources["Secret Sources"]
        GH["GitHub Secrets"]
        Vercel_Env["Vercel Env"]
        Railway_Env["Railway Variables"]
    end

    subgraph Deploy["Deployment"]
        CI["CI/CD"]
        FE["Frontend"]
        BE["Backend"]
    end

    GH --> CI
    Vercel_Env --> FE
    Railway_Env --> BE
```

---

## 5. 비용 분석

> **하위 목차**
> - [5.1 월 예상 비용](#51-월-예상-비용)
> - [5.2 스케일업 비용 (성장 시)](#52-스케일업-비용-성장-시)
> - [5.3 비용 최적화 전략](#53-비용-최적화-전략)

### 5.1 월 예상 비용

| 서비스 | 무료 한도 | 예상 사용량 | 예상 비용 |
|--------|-----------|-------------|-----------|
| Vercel | 100GB 대역폭/월 | ~10GB | $0 |
| Railway | $5 크레딧/월 | ~$3 | $0 |
| Supabase | 500MB DB, 50K MAU | ~100MB, ~1K | $0 |
| Cloudflare R2 | 10GB 저장 | ~5GB | $0 |
| PortOne | 무제한 | - | $0 |
| **합계** | - | - | **$0~5/월** |

### 5.2 스케일업 비용 (성장 시)

| 서비스 | 유료 플랜 | 가격 | 트리거 |
|--------|-----------|------|--------|
| Vercel | Pro | $20/월 | 100GB 초과 |
| Railway | Usage Based | $0.01/GB | $5 초과 |
| Supabase | Pro | $25/월 | 500MB 초과 |
| Cloudflare R2 | Pay as you go | $0.015/GB | 10GB 초과 |

### 5.3 비용 최적화 전략

```mermaid
flowchart TB
    subgraph Strategy["비용 최적화"]
        S1["이미지 최적화<br/>WebP 변환, 리사이즈"]
        S2["캐싱 활용<br/>Vercel Edge Cache"]
        S3["DB 쿼리 최적화<br/>인덱스, N+1 방지"]
        S4["정적 생성<br/>SSG for SEO pages"]
    end

    S1 --> R1["R2 저장 비용 감소"]
    S2 --> R2["Origin 요청 감소"]
    S3 --> R3["DB 부하 감소"]
    S4 --> R4["서버리스 비용 감소"]
```

---

## 6. 모니터링

> **하위 목차**
> - [6.1 모니터링 스택](#61-모니터링-스택)
> - [6.2 알림 설정](#62-알림-설정)
> - [6.3 핵심 메트릭](#63-핵심-메트릭)
> - [6.4 로그 레벨](#64-로그-레벨)

### 6.1 모니터링 스택

| 영역 | 도구 | 용도 |
|------|------|------|
| APM | Vercel Analytics | 프론트엔드 성능 |
| Error | Sentry | 에러 추적 |
| Logs | Railway Logs | 백엔드 로그 |
| Uptime | Better Uptime | 가용성 모니터링 |
| Database | Supabase Dashboard | DB 모니터링 |

### 6.2 알림 설정

```mermaid
flowchart LR
    subgraph Events["Events"]
        E1["Error Rate > 1%"]
        E2["Response Time > 3s"]
        E3["Downtime"]
        E4["Deploy Failed"]
    end

    subgraph Channels["Channels"]
        Slack["Slack"]
        Email["Email"]
    end

    Events --> Slack
    Events --> Email
```

### 6.3 핵심 메트릭

| 메트릭 | 목표 | 알림 임계값 |
|--------|------|-------------|
| Uptime | 99.9% | < 99% |
| Response Time (P95) | < 500ms | > 2s |
| Error Rate | < 0.1% | > 1% |
| Apdex Score | > 0.9 | < 0.7 |

### 6.4 로그 레벨

| 레벨 | 용도 | 보관 기간 |
|------|------|-----------|
| ERROR | 에러 발생 | 30일 |
| WARN | 경고 상황 | 14일 |
| INFO | 정상 이벤트 | 7일 |
| DEBUG | 디버깅 (개발만) | 1일 |

---

## 외부 시스템 링크

| 서비스 | 대시보드 |
|--------|----------|
| Vercel | https://vercel.com/dashboard |
| Railway | https://railway.app/dashboard |
| Supabase | https://supabase.com/dashboard |
| Cloudflare | https://dash.cloudflare.com |
| PortOne | https://admin.portone.io |

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2025-12-25 | TDD v1.6 내용 기반 초기 작성 |
