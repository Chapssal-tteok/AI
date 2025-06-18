# PreView AI Repository

> 이 레포지토리는 **AI 기반 자기소개서 분석 및 면접 준비 서비스 PreView**의 AI 서버를 위한 FastAPI 기반 프로젝트입니다.

## 👥 팀 소개

**Team 30 - 찹쌀떡**

| 항목 | 신정화 (2271035) | 차현주 (2276321) |
|-----|-----------------|-----------------|
| GitHub | [@jungh150](https://github.com/jungh150) | [@chacha091](https://github.com/chacha091) |
| 역할  | 팀장 / 백엔드 개발자 | 팀원 / 프론트엔드 개발자 |
| 담당 업무 | 백엔드 개발, 서버 배포, AI 기능 구현 | 프론트엔드 개발, UI/UX 디자인, AI 기능 구현 |

## 🔍 프로젝트 개요

**PreView**는 GPT-4o와 RAG 기반 기술을 활용하여 자기소개서 분석과 맞춤형 면접 연습을 지원하는 **AI 기반 자기소개서 분석 및 면접 준비 서비스 PreView**입니다.  
취업 준비자가 보다 효율적으로 자기소개서를 개선하고, 실제 면접처럼 연습할 수 있도록 돕는 것이 핵심 목표입니다.

### 🎯 주요 목표
- 객관적이고 세밀한 자기소개서 분석 및 피드백 제공
- 자기소개서 및 기업·직무 맞춤형 면접 예상 질문 생성
- 음성 기반 인터뷰 시뮬레이션을 통한 실전 감각 향상

### 🧠 기술적 특성
- **GPT-4o** 기반 프롬프트 엔지니어링을 통한 정밀한 자소서 피드백
- **Perplexity AI + ChromaDB** 기반 RAG 시스템으로 기업 및 직무 맞춤형 질문 생성
- **Google TTS/STT** 기술을 활용한 음성 기반 면접 연습 기능 제공
- **Spring Boot + FastAPI** 구조로 백엔드 서버와 AI 서버 분리 구성

> 💡 **참고:** 본 레포지토리는 GPT-4o 분석 및 Perplexity 기반 질문 생성을 담당하는 **FastAPI 기반 AI 서버**입니다.  
> 👉 Spring Boot 기반 백엔드 서버와 연동되어, AI 기능을 외부 API 형태로 제공합니다.

### 🛠 제공 기능
1. **자기소개서 피드백**  
   → 질문 충실도, 논리 흐름, 구체성 등 6가지 항목 분석 + 개선 예문 제시  
2. **맞춤형 면접 질문 생성**  
   → 자기소개서 핵심 키워드 기반, RAG로 도출된 예상 질문 제공  
3. **음성 면접 시뮬레이션**  
   → TTS/STT로 실제 면접처럼 연습, 답변 분석 및 후속 질문 피드백 제공

PreView는 누구나 **혼자서도 실전 면접을 준비할 수 있는 AI 면접 파트너**입니다.

## 🛠 기술 스택 및 주요 라이브러리

### 🧩 사용 기술

| 항목 | 내용 |
|------|------|
| Language | Python 3.10 |
| Framework | FastAPI |
| AI 모델 | GPT-4o (OpenAI), Sonar (Perplexity API) |
| 벡터 검색 | ChromaDB + SentenceTransformer |
| 프롬프트 관리 | Python 기반 Prompt Template 구조 |
| 외부 연동 | OpenAI API, Perplexity API |
| 데이터 크롤링 | Selenium |
| 실행 환경 관리 | uvicorn, dotenv, requirements.txt 기반 |

## 📁 디렉토리 구조

```
AI/
├── app/                             # 애플리케이션 주요 모듈
│   ├── api/                         # FastAPI 라우팅 관련 파일
│   │   ├── interview/               # 면접 관련 API 라우터
│   │   │   └── route.py
│   │   ├── chroma.py                # ChromaDB 관련 API 라우터
│   │   ├── perplexity.py            # Perplexity 관련 API 라우터
│   │   └── __init__.py
│   ├── core/                        # 핵심 설정 및 유틸
│   │   ├── config.py                # 환경 변수 로딩 등 설정 파일
│   │   ├── init_chroma.py           # ChromaDB 초기화용 스크립트
│   │   └── vector_utils.py          # 벡터 처리 유틸 함수들
│   ├── models/                      # 검색 관련 모델 정의
│   │   └── search_model.py
│   ├── prompts/                     # 프롬프트 모음
│   │   ├── analyze_answer_prompts.py
│   │   ├── follow_up_prompts.py
│   │   ├── interview_qas_prompts.py
│   │   └── resume_analyze_prompts.py
│   ├── services/                    # 기능별 서비스 모듈
│   │   ├── chroma_service.py        # 벡터 검색 관련 로직
│   │   ├── gpt_service.py           # GPT-4o API 호출 관련
│   │   └── perplexity_service.py    # Perplexity 호출 관련
│   └── __init__.py
│
├── db/                              # ChromaDB 데이터 저장 폴더
│
├── .env                             # 환경 변수 파일 (.env)
├── crolling_question.py             # 면접 질문 크롤링 코드
├── dataset_question.csv             # 크롤링을 통해 얻은 기업, 직무 별 면접 질문 데이터
├── main.py                          # FastAPI 앱 진입점
├── requirements.txt                 # Python 의존성 명세
└── README.md
```

## 🚀 주요 API 기능

| 엔드포인트 | 설명 |
|------------|------|
| `POST /analyze-resume` | 자기소개서 문항과 답변을 기반으로 GPT가 피드백을 생성합니다. |
| `POST /analyze-answer` | 면접 답변에 대해 강점과 개선점을 분석합니다. |
| `POST /follow-up` | 면접 답변을 기반으로 추가 질문을 생성합니다. |
| `POST /generate-qas` | 자기소개서, 기업 및 직무 정보를 기반으로 예상 면접 질문을 생성합니다. |

> **예시 요청 및 응답은 각 API 내부에 Swagger-style Docstring으로 포함되어 있습니다.**

## 🔧 사전 준비사항

AI 서버를 실행하기 위해 아래의 환경 및 자원들이 필요합니다:

- Python 3.10 이상
- `pip` 또는 `virtualenv` 사용 가능 환경
- 아래 서비스의 API 키 발급
  - 🔑 OpenAI API Key: https://platform.openai.com/account/api-keys
  - 🔑 Perplexity API Key: https://www.perplexity.ai/
- 크롤링용 ChromeDriver 설치 (`crolling_question.py` 실행 시 필요)
  - 사용 중인 Chrome 브라우저 버전에 맞는 ChromeDriver 다운로드
  - 📎 다운로드: [Chrome for Testing (ChromeDriver)](https://googlechromelabs.github.io/chrome-for-testing/)

## 🚀 시작하기

### 1️⃣ 레포지토리 클론

```bash
git clone https://github.com/Chapssal-tteok/preview-ai.git
cd preview-ai
```

### 2️⃣ 의존성 설치

```bash
pip install -r requirements.txt
```

또는 가상환경을 사용하는 경우:

```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3️⃣ `.env` 파일 작성

루트 디렉토리에 `.env` 파일을 생성하고 다음 내용을 입력합니다:

```ini
CHROMEDRIVER_PATH=YOUR_CHROME_DRIVER_PATH
OPENAI_API_KEY=your-openai-api-key
PPLX_API_KEY=your-perplexity-api-key
```

### 4️⃣ 면접 질문 데이터 크롤링 (선택)

> 💡 이미 dataset_question.csv가 준비되어 있다면 이 단계는 생략 가능합니다.

```bash
python crolling_question.py
```

- 잡코리아 웹사이트에서 기업명, 경력 구분, 직무, 면접 질문 데이터를 크롤링하여
CSV 파일 `dataset_question.csv`에 저장합니다.

- 해당 파일이 이미 존재할 경우, 이전에 저장된 데이터를 보존한 채 새로운 질문이 이어서 추가됩니다.

- 크롤링 결과는 이후 ChromaDB 초기화 시 임베딩 데이터로 사용됩니다.

### 5️⃣ 벡터 DB 초기화

```bash
python app/core/init_chroma.py
```

- `dataset_question.csv`에 저장된 면접 질문 데이터를 기반으로 ChromaDB 벡터 데이터베이스를 초기화합니다.

- 각 질문은 SentenceTransformer로 임베딩되어 저장되며, 추후 `/generate-qas` API에서 유사 질문 검색에 사용됩니다.

- 초기화 시 기존 ChromaDB 폴더(`db/`)는 삭제되고 새롭게 생성되며,
초기화가 완료되면 `✅ DB 초기화 완료. 총 문서 수: N` 형태로 완료 메시지가 출력됩니다.

### 6️⃣ 서버 실행

```bash
uvicorn main:app --reload --port 8000
```

- 기본 실행 주소: http://localhost:8000
- Swagger 문서 확인: http://localhost:8000/docs