# 🚀 웹 게시판 프로젝트

## ✨ 프로젝트 소개

이 프로젝트는 사용자들이 여행 기록을 자유롭게 작성하고 공유할 수 있는 간단한 웹 게시판 서비스입니다. Python의 **FastAPI** 웹 프레임워크를 사용하여 백엔드를 구축하고, **SQLAlchemy**로 데이터베이스를 관리합니다. 프론트엔드는 **Jinja2 템플릿**과 직접 작성한 **CSS, JavaScript**를 활용하여 구현되었습니다.

## 🛠️ 주요 기능

우리가 함께 구현한 주요 기능들은 다음과 같습니다:

-   **회원 가입 및 로그인:** 사용자 계정을 생성하고 로그인하여 게시판 기능을 이용할 수 있습니다. (쿠키 기반 인증)
-   **게시글 목록 보기:** 작성된 모든 게시글을 최신순으로 볼 수 있습니다. (제목 한 줄 표시 기능 포함!)
-   **게시글 상세 보기:** 특정 게시글의 상세 내용을 확인하고, 작성자일 경우 수정/삭제 버튼을 볼 수 있습니다.
-   **게시글 작성:** 로그인한 사용자는 새로운 게시글을 작성하여 게시판에 올릴 수 있습니다.
-   **게시글 삭제:** 게시글 작성자 본인만 해당 게시글을 삭제할 수 있습니다. (JavaScript `fetch` API 연동!)
-   **데이터베이스 연동:** MySQL 데이터베이스에 사용자 및 게시글 데이터를 저장하고 관리합니다.
-   **반응형 웹 디자인:** CSS 미디어 쿼리를 활용하여 기본적인 모바일 화면 레이아웃을 지원합니다.
-   **통일된 디자인:** 웹사이트 전체에 걸쳐 일관성 있는 버튼, 레이아웃 스타일을 적용했습니다.

## 📦 사용 기술

이 프로젝트를 구축하는 데 사용된 핵심 기술 스택입니다:

-   **백엔드:** Python, FastAPI, SQLAlchemy(ORM), Uvicorn (ASGI 서버)
-   **데이터베이스:** MySQL
-   **프론트엔드:** HTML (Jinja2), CSS, JavaScript 
-   **패키지 관리:** uv (pip 호환)
## ▶️ 시작하는 방법

프로젝트를 로컬 환경에서 실행하기 위한 단계입니다:

1.  **프로젝트 클론:**
    ```bash
    git clone [깃허브 레포지토리 주소]
    cd [프로젝트 폴더 이름]
    ```
2.  **가상 환경 설정:**
    ```bash
    # uv 사용 시
    uv venv
    uv sync
    ```
    *(uv 또는 pipenv 등 사용하는 가상 환경 툴에 맞게 사용하세요.)*
3.  **데이터베이스 설정:**
    *   MySQL 서버를 설치하고 실행합니다.
    *   `database.py` 파일을 열어 `DATABASE_URL`에 MySQL 연결 정보를 올바르게 설정합니다. (예: `mysql+mysqlconnector://유저명:비밀번호@호스트:포트/DB이름`)
    *   FastAPI 서버 실행 시 `Base.metadata.create_all(bind=engine)` 코드가 자동으로 테이블을 생성합니다. (필요하다면 Alembic 등으로 마이그레이션 관리)
4.  **FastAPI 서버 실행:**
    ```bash
    # uv 가상 환경 활성화 후
    uvicorn main:app --reload
    ```
5.  **접속:**
    웹 브라우저를 열고 `http://127.0.0.1:8000` 또는 서버가 실행된 주소로 접속합니다.

## 📁 프로젝트 구조 (예상)

├── main.py # FastAPI 메인 애플리케이션 및 라우트 정의</br>
├── database.py # DB 연결 설정 (SQLAlchemy engine, SessionLocal 등)</br>
├── models.py # SQLAlchemy DB 모델 정의 (User, Post 등)</br>
├── schemas.py # Pydantic 스키마 정의 (Request/Response 데이터 모델)</br>
├── templates/ # Jinja2 HTML 템플릿 파일들</br>
│ ├── base.html # 기본 레이아웃 템플릿</br>
│ ├── index.html # 인덱스 페이지</br>
│ ├── web_board.html # 게시글 목록 페이지</br>
│ ├── web_board_detail.html # 게시글 상세 페이지</br>
│ ├── web_board_create.html # 게시글 작성 페이지</br>
│ └── ... (로그인, 회원가입 등 다른 페이지)</br>
└── static/ # 정적 파일 (CSS, JS 등)</br>
└── styles.css # 웹사이트 스타일 정의</br>
└── scripts.js # 클라이언트 측 JavaScript (예: 삭제 기능)</br>


## 💡 개선 예정 / 추가 기능

앞으로 다음과 같은 기능들을 추가하거나 개선할 수 있습니다:

-   게시글 수정 기능 구현
-   댓글 기능 추가
-   사용자 프로필 페이지 구현
-   게시글 검색 및 페이징 기능 추가
-   이미지 업로드 기능 추가
-   보안 강화 (비밀번호 해싱, CSRF 방지 등)
-   프론트엔드 프레임워크(React, Vue 등) 도입 검토

<details>
<summary> <b> 이미지 </b></summary>

<br/>
<img src="https://github.com/user-attachments/assets/306bf85b-6c76-47b3-be84-ff6b550475fa" alt="[1]">


<img src="https://github.com/user-attachments/assets/5f63e1e5-a3fd-43da-82f8-3d6ff1b9657d" alt="[3]">

<img src="https://github.com/user-attachments/assets/30e3990d-a7d8-4cfa-855d-0b4c441385fb" alt="[4]">

<img src="https://github.com/user-attachments/assets/8b7c8a3b-096c-4e81-b4c2-e75898d46357" alt="[5]">

<img src="https://github.com/user-attachments/assets/440667cc-dc00-4645-9ad9-333f6bf98ba3" alt="[6]">

<img src="https://github.com/user-attachments/assets/61adb942-57e5-4a2e-935d-187aac570bed" alt="[2]">

<img src="https://github.com/user-attachments/assets/07c75c90-1fd4-4ab9-b706-1203c422bb51" alt="[7]">

<img src="https://github.com/user-attachments/assets/00bc8638-6b8d-4ab9-9893-1eb745ee3d43" alt="[8]">

</details>