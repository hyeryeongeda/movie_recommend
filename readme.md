# 🎬 MYFLIX – Movie Recommendation & Review Platform

사용자가 영화를 검색하고, 별점을 주고, 리뷰를 남기며, 보고 싶은 영화/본 영화를 관리할 수 있는 **영화 커뮤니티 서비스**입니다.
TMDB API 기반으로 데이터를 가져오고 Django REST + Vue3 프론트엔드로 구성되었습니다.

---

## 🚀 주요 기능

### 🔐 인증 (JWT)

- 회원가입 / 로그인 / 로그아웃
- JWT 토큰 기반 자동 로그인 유지
- 마이페이지에서 내 활동 조회 예정

### 🎞 영화

- TMDB API 기반 인기 영화 데이터 수집 (커스텀 management command)
- 영화 리스트 / 상세페이지
- 관련된 비슷한 영화 추천
- 감독 및 출연 배우 정보 표시

### ⭐ 평점

- 사용자가 영화에 직접 별점 부여
- 별점 클릭 즉시 서버에 저장 및 평균 점수 동기화
- 로그인한 사용자만 가능

### 📝 리뷰

- 영화별 리뷰 작성 / 삭제 / 조회
- 리뷰 좋아요 기능
- 리뷰 목록 실시간 새로고침

### ✔️ 워치리스트(보고싶어요 / 봤어요)

- 토글 방식으로 상태 변경 (WANT / DONE)
- 영화 상세 페이지에서 바로 관리 가능

---

## 🏗 기술 스택

### Backend

- **Django 5**
- **Django REST Framework**
- **SimpleJWT** (JWT 인증)
- **SQLite3**
- **TMDB API**

### Frontend

- **Vue 3 (Composition API)**
- **Vite**
- **Axios**
- **Pinia 방식의 Custom Store 구조 (useAuth)**

---

## 📁 프로젝트 구조

```
my_movies/
 ┣ backend/
 ┃ ┣ movies/
 ┃ ┣ accounts/
 ┃ ┣ config/
 ┃ ┗ manage.py
 ┗ frontend/
    ┣ src/
    ┃ ┣ api/
    ┃ ┣ components/
    ┃ ┣ stores/
    ┃ ┣ views/
    ┃ ┣ router/
    ┃ ┗ main.js
```

---

## ⚙️ 설치 및 실행 방법

### 1) Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows에서는 venv/Scripts/activate
pip install -r requirements.txt
```

### `.env 설정`

```
SECRET_KEY=django-secret-key
TMDB_API_KEY=YOUR_TMDB_API_KEY
DEBUG=True
```

### DB 마이그레이션 및 TMDB 데이터 넣기

```bash
python manage.py migrate
python manage.py import_tmdb --pages 3
```

### 서버 실행

```bash
python manage.py runserver
```

---

### 2) Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🖼 주요 화면

### 🎞 홈 화면

- 인기 영화 슬라이드
- TMDB 포스터/제목 자동 반영

### 📄 영화 상세

- 포스터, 개요, 장르
- 감독/출연자 정보
- ⭐ 별점 입력
- 📝 리뷰 목록/작성
- ✔️ 보고싶어요 / 봤어요 토글
- 비슷한 영화 추천

### 👤 로그인 / 회원가입

- JWT 기반 로그인
- 자동 로그인 유지
- 네비바에 사용자명 표시

---

## 🔮 앞으로 추가될 기능 (계획)

- 마이페이지 (내 리뷰, 내 평점, 워치리스트)
- 검색 기능
- 영화 필터링 (장르/국가/평점)
- 소셜 로그인
- 반응형 UI 개선

---

## 🧑‍💻 개발 포인트

- TMDB API의 원본 포스터 URL과 Django Media 경로를 정리해 **통일된 포스터 처리 로직** 구현
- JWT 토큰 자동 저장/갱신 로직 직접 설계
- 영화 상세 페이지의 성능을 위해 **fetchMovie() 하나로 데이터 구조 정리**
- 컴포넌트 기반 구조로 Rating, WatchButtons, ReviewForm 재사용성 향상

---

## 📬 연락

만약 이 프로젝트에 대해 궁금한 것 있으면 언제든 연락 주세요!
