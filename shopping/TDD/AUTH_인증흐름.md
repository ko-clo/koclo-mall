# 인증 흐름 (Authentication Flow)

**Version 1.0** | **2025-12-25** | **ko&clo Project**

---

## 목차

1. [개요](#1-개요)
2. [인증 아키텍처](#2-인증-아키텍처)
3. [JWT 토큰 관리](#3-jwt-토큰-관리)
4. [인증 흐름 상세](#4-인증-흐름-상세)
5. [권한 관리](#5-권한-관리)
6. [보안 고려사항](#6-보안-고려사항)

---

## 1. 개요

> **하위 목차**
> - [1.1 인증 방식](#11-인증-방식)
> - [1.2 인증 주체](#12-인증-주체)

### 1.1 인증 방식

| 방식 | 설명 | 우선순위 |
|------|------|----------|
| Supabase Auth | OAuth 및 이메일 인증 통합 | Primary |
| JWT | 토큰 기반 인증 | - |
| HttpOnly Cookie | 토큰 저장 | - |

### 1.2 인증 주체

| 주체 | 역할 | 인증 방식 |
|------|------|-----------|
| Consumer | 일반 고객 | 소셜/이메일 로그인 |
| Admin | 관리자 | 이메일 로그인 + Role 검증 |
| Service | 서버 간 통신 | Service Role Key |

---

## 2. 인증 아키텍처

> **하위 목차**
> - [2.1 전체 인증 흐름](#21-전체-인증-흐름)
> - [2.2 계층별 인증 책임](#22-계층별-인증-책임)

### 2.1 전체 인증 흐름

```mermaid
flowchart TB
    subgraph Client["Client Layer"]
        Browser["Browser"]
        Cookie["HttpOnly Cookie"]
    end

    subgraph Vercel["Vercel (SvelteKit)"]
        Hooks["hooks.server.ts"]
        Layout["layout.server.ts"]
        API["API Routes"]
    end

    subgraph Supabase["Supabase"]
        Auth["Supabase Auth"]
        JWT["JWT Issuer"]
    end

    subgraph Railway["Railway (FastAPI)"]
        Middleware["Auth Middleware"]
        Endpoints["API Endpoints"]
    end

    Browser -->|1. Login| Auth
    Auth -->|2. JWT| Browser
    Browser -->|3. Store| Cookie
    Cookie -->|4. Request| Hooks
    Hooks -->|5. Verify| Auth
    Hooks -->|6. Pass| Layout
    Layout -->|7. User State| Browser
    API -->|8. Forward| Middleware
    Middleware -->|9. Verify| Endpoints
```

### 2.2 계층별 인증 책임

```mermaid
flowchart LR
    subgraph L1["Layer 1: Client"]
        A1["토큰 저장/전송"]
        A2["로그인 UI"]
        A3["상태 관리"]
    end

    subgraph L2["Layer 2: BFF (SvelteKit)"]
        B1["쿠키 파싱"]
        B2["토큰 갱신"]
        B3["세션 검증"]
    end

    subgraph L3["Layer 3: API (FastAPI)"]
        C1["JWT 검증"]
        C2["권한 확인"]
        C3["사용자 컨텍스트"]
    end

    L1 --> L2 --> L3
```

---

## 3. JWT 토큰 관리

> **하위 목차**
> - [3.1 토큰 구조](#31-토큰-구조)
> - [3.2 토큰 종류 및 저장](#32-토큰-종류-및-저장)
> - [3.3 토큰 생명주기 상태](#33-토큰-생명주기-상태)
> - [3.4 토큰 갱신 Flow](#34-토큰-갱신-flow)
> - [3.5 Race Condition 처리](#35-race-condition-처리)

### 3.1 토큰 구조

```mermaid
flowchart TB
    subgraph JWT["JWT Token"]
        Header["Header<br/>alg: HS256<br/>typ: JWT"]
        Payload["Payload<br/>sub: user_id<br/>email: user@...<br/>role: authenticated<br/>exp: timestamp"]
        Signature["Signature<br/>HMAC-SHA256"]
    end

    Header --> Signature
    Payload --> Signature
```

### 3.2 토큰 종류 및 저장

| 토큰 | 저장 위치 | 유효 기간 | 용도 |
|------|-----------|-----------|------|
| access_token | HttpOnly Cookie | 1시간 | API 인증 |
| refresh_token | HttpOnly Cookie | 30일 | 토큰 갱신 |

### 3.3 토큰 생명주기 상태

```mermaid
stateDiagram-v2
    [*] --> Valid: 로그인 성공

    Valid --> Expiring: 만료 5분 전
    Expiring --> Valid: 자동 갱신 성공

    Valid --> Expired: 만료
    Expiring --> Expired: 갱신 실패
    Expired --> Valid: Refresh 토큰으로 갱신

    Expired --> Invalid: Refresh도 만료
    Valid --> Invalid: 로그아웃
    Invalid --> [*]: 재로그인 필요
```

### 3.4 토큰 갱신 Flow

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant SK as SvelteKit
    participant SA as Supabase Auth

    C->>SK: API 요청 (access_token)
    SK->>SK: 토큰 만료 확인

    alt 만료 임박 (< 5분)
        SK->>SA: refreshSession(refresh_token)
        SA-->>SK: 새 access_token + refresh_token
        SK->>SK: Cookie 업데이트
        SK->>SK: 원래 요청 처리
        SK-->>C: 응답 + Set-Cookie
    else 유효
        SK->>SK: 요청 처리
        SK-->>C: 응답
    else 만료됨
        SK->>SA: refreshSession(refresh_token)
        alt 갱신 성공
            SA-->>SK: 새 토큰
            SK-->>C: 응답 + Set-Cookie
        else 갱신 실패
            SA-->>SK: 401
            SK-->>C: 로그인 페이지로 리다이렉트
        end
    end
```

### 3.5 Race Condition 처리

동시에 여러 요청이 토큰 갱신을 시도할 때의 처리:

```mermaid
stateDiagram-v2
    state "Token State" as TS {
        [*] --> Idle

        Idle --> Refreshing: 갱신 요청
        Refreshing --> Idle: 갱신 완료

        state Refreshing {
            [*] --> InProgress
            InProgress --> Waiting: 추가 요청
            Waiting --> Waiting: 추가 요청
            InProgress --> Complete: 갱신 성공
            Complete --> [*]: 대기 요청 처리
        }
    }
```

#### 구현 전략

```typescript
// src/lib/auth/tokenManager.ts
let refreshPromise: Promise<Session> | null = null;

async function refreshToken(): Promise<Session> {
  // 이미 갱신 중이면 기존 Promise 반환 (중복 요청 방지)
  if (refreshPromise) {
    return refreshPromise;
  }

  refreshPromise = supabase.auth.refreshSession()
    .then(({ data }) => {
      refreshPromise = null;
      return data.session;
    })
    .catch((error) => {
      refreshPromise = null;
      throw error;
    });

  return refreshPromise;
}
```

---

## 4. 인증 흐름 상세

> **하위 목차**
> - [4.1 전체 인증 시퀀스](#41-전체-인증-시퀀스)
> - [4.2 hooks.server.ts 처리](#42-hooksserverts-처리)
> - [4.3 보호된 라우트 접근](#43-보호된-라우트-접근)

### 4.1 전체 인증 시퀀스

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant SA as Supabase Auth
    participant SK as SvelteKit BFF
    participant FA as FastAPI

    C->>SA: Login Request
    SA-->>C: JWT Token
    C->>SK: API Request (Bearer JWT)
    SK->>SK: JWT Verification (via Supabase)
    SK->>FA: Internal API Call (JWT Forward)
    FA->>FA: JWT Final Verification
    FA-->>SK: Response Data
    SK-->>C: Processed Response
```

### 4.2 hooks.server.ts 처리

```mermaid
flowchart TB
    A[Request 수신] --> B{Cookie 존재?}
    B -->|No| C[event.locals.user = null]
    B -->|Yes| D[Supabase Client 생성]
    D --> E[getSession 호출]
    E --> F{세션 유효?}
    F -->|No| G{Refresh 가능?}
    G -->|Yes| H[토큰 갱신]
    G -->|No| C
    H --> I{갱신 성공?}
    I -->|Yes| J[event.locals.user = user]
    I -->|No| C
    F -->|Yes| J
    C --> K[다음 핸들러로 전달]
    J --> K
```

### 4.3 보호된 라우트 접근

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant SK as SvelteKit
    participant Guard as Route Guard

    C->>SK: /my/orders 접근
    SK->>Guard: 라우트 보호 확인
    Guard->>Guard: locals.user 확인

    alt 인증됨
        Guard-->>SK: 통과
        SK-->>C: 페이지 렌더링
    else 미인증
        Guard-->>SK: 리다이렉트
        SK-->>C: 302 → /auth/login?redirect=/my/orders
    end
```

---

## 5. 권한 관리

> **하위 목차**
> - [5.1 역할 정의](#51-역할-정의)
> - [5.2 역할별 접근 권한](#52-역할별-접근-권한)
> - [5.3 권한 검증 Flow](#53-권한-검증-flow)
> - [5.4 Admin 인증 상태](#54-admin-인증-상태)

### 5.1 역할 정의

| 역할 | 설명 | 접근 범위 |
|------|------|-----------|
| anon | 비회원 | 공개 API만 |
| authenticated | 일반 회원 | 본인 데이터 + 공개 API |
| admin | 관리자 | 모든 API |
| service_role | 서버 | 제한 없음 |

### 5.2 역할별 접근 권한

```mermaid
flowchart TB
    subgraph Public["Public (anon)"]
        P1[상품 목록]
        P2[상품 상세]
        P3[카테고리]
    end

    subgraph Member["Member (authenticated)"]
        M1[내 정보]
        M2[주문 내역]
        M3[장바구니]
        M4[배송지]
    end

    subgraph Admin["Admin"]
        A1[상품 관리]
        A2[주문 관리]
        A3[회원 관리]
        A4[통계]
    end

    Public --> Member --> Admin
```

### 5.3 권한 검증 Flow

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant SK as SvelteKit
    participant FA as FastAPI
    participant DB as Database

    C->>SK: Admin API 요청
    SK->>SK: JWT에서 user_id 추출
    SK->>FA: 요청 전달
    FA->>DB: SELECT role FROM members WHERE id = ?
    DB-->>FA: role = 'admin'

    alt Admin 역할
        FA->>FA: 요청 처리
        FA-->>SK: 200 OK
        SK-->>C: 응답
    else 일반 회원
        FA-->>SK: 403 Forbidden
        SK-->>C: 권한 없음
    end
```

### 5.4 Admin 인증 상태

```mermaid
stateDiagram-v2
    [*] --> Guest: 사이트 접속

    Guest --> Member: 일반 로그인
    Guest --> AdminPending: Admin 로그인 시도

    AdminPending --> Admin: Role 검증 성공
    AdminPending --> Member: Role 검증 실패

    Member --> Guest: 로그아웃
    Admin --> Guest: 로그아웃

    Admin --> AdminExpired: 세션 만료
    AdminExpired --> AdminPending: 재인증
```

---

## 6. 보안 고려사항

> **하위 목차**
> - [6.1 CSRF 방지](#61-csrf-방지)
> - [6.2 XSS 방지](#62-xss-방지)
> - [6.3 Brute Force 방지](#63-brute-force-방지)
> - [6.4 토큰 보안](#64-토큰-보안)
> - [6.5 Supabase RLS 정책](#65-supabase-rls-정책)

### 6.1 CSRF 방지

```mermaid
flowchart LR
    A[Cookie] -->|SameSite=Lax| B[Same Origin만 전송]
    C[API 요청] -->|Origin 검증| D[허용된 도메인만]
```

| 설정 | 값 | 목적 |
|------|-----|------|
| SameSite | Lax | Cross-site 요청 시 쿠키 미전송 |
| HttpOnly | true | JavaScript 접근 차단 |
| Secure | true | HTTPS만 전송 |

### 6.2 XSS 방지

| 대상 | 방어 수단 |
|------|-----------|
| 토큰 저장 | HttpOnly Cookie (JS 접근 불가) |
| 사용자 입력 | Svelte 자동 이스케이프 |
| API 응답 | Content-Type: application/json |

### 6.3 Brute Force 방지

```mermaid
flowchart TB
    A[로그인 시도] --> B{실패 횟수?}
    B -->|< 5회| C[정상 처리]
    B -->|5~10회| D[CAPTCHA 요구]
    B -->|> 10회| E[15분 잠금]

    C --> F{성공?}
    F -->|Yes| G[실패 횟수 초기화]
    F -->|No| H[실패 횟수 +1]

    D --> F
    E --> I[15분 후 재시도 가능]
```

### 6.4 토큰 보안

| 위협 | 대응 |
|------|------|
| 토큰 탈취 | 짧은 만료 시간 (1시간) |
| Replay 공격 | 토큰 갱신 시 이전 토큰 무효화 |
| 세션 하이재킹 | IP/User-Agent 변경 감지 |

### 6.5 Supabase RLS 정책

```sql
-- 본인 데이터만 조회
CREATE POLICY "Users can view own data"
  ON members FOR SELECT
  USING (auth.uid() = id);

-- 본인 데이터만 수정
CREATE POLICY "Users can update own data"
  ON members FOR UPDATE
  USING (auth.uid() = id);

-- 본인 주문만 조회
CREATE POLICY "Users can view own orders"
  ON orders FOR SELECT
  USING (auth.uid() = member_id);
```

---

## 환경 변수

```bash
# Supabase
PUBLIC_SUPABASE_URL=https://xxx.supabase.co
PUBLIC_SUPABASE_ANON_KEY=eyJxxx...

# JWT (서버 전용)
SUPABASE_JWT_SECRET=your-jwt-secret
```

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0 | 2025-12-25 | TDD v1.6 내용 기반 초기 작성 |
