# ShuviAI

ShuviAI는 마이크 입력을 인식하여 Google Gemini 모델을 통해 텍스트 응답을 생성하고, 필요에 따라 응답을 음성으로 출력할 수 있는 로컬 Python 애플리케이션입니다. 코드 구조는 **입력**, **AI 처리**, **음성 출력**, **설정** 모듈로 분리되어 있어 나중에 디스코드 봇으로 쉽게 이식할 수 있도록 설계되었습니다.

## 설치 방법

1. 이 저장소를 원하는 위치에 준비합니다.
2. Python 3.9 이상이 설치되어 있는지 확인하세요.
3. 의존성 설치:

       pip install -r requirements.txt

4. 환경 설정 파일 준비:
   - `.env.example` 파일을 복사하여 `.env`로 이름을 바꿉니다.
   - `GEMINI_API_KEY`에 Google AI Studio에서 발급한 키를 입력하세요.
   - 음성 출력(TTS)을 사용하려면 `USE_TTS=true`로 변경하세요.

## 실행 방법

콘솔에서 다음과 같이 실행하세요:

       python main.py

프로그램을 실행하면 마이크를 통해 음성 입력을 받을 준비가 됩니다. 말을 하면 Google Speech Recognition을 통해 텍스트로 변환되고, 변환된 텍스트를 Gemini 모델에 전달하여 응답을 생성한 뒤 콘솔에 출력합니다. `USE_TTS=true`로 설정되어 있으면 응답을 음성으로도 들을 수 있습니다.

## 폴더 구조
