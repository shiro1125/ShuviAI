# ShuviAI

ShuviAI는 마이크 입력을 인식하여 Google Gemini 모델을 통해 텍스트 응답을 생성하고, 필요에 따라 응답을 음성으로 출력할 수 있는 로컬 Python 애플리케이션입니다. 코드 구조는 **입력**, **AI 처리**, **음성 출력**, **설정** 모듈로 분리되어 있어 나중에 디스코드 봇으로 쉽게 이식할 수 있도록 설계되었습니다.

## 설치 방법

1. 이 저장소를 원하는 위치에 준비합니다.
2. Python 3.9 이상이 설치되어 있는지 확인하세요.
3. **필수 의존성 설치:**

   ```bash
   pip install -r requirements.txt
   ```

   이 명령은 Google Gen AI SDK(`google-genai`)와 필수 라이브러리를 한 번에 설치합니다. 일부 라이브러리(`pyaudio` 등)는 Windows에서 컴파일 문제가 발생할 수 있으므로 **PyAudio 설치에 주의**해야 합니다. 다음 명령을 순서대로 실행하면 사전 컴파일된 PyAudio 패키지를 설치할 수 있습니다:

   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

   이 과정을 완료하면 마이크 입력을 정상적으로 사용할 수 있습니다.

4. **환경 설정 파일 준비:**
   - `.env.example` 파일을 복사하여 `.env`로 이름을 바꿉니다.
   - `GEMINI_API_KEY`에 Google AI Studio 또는 Google Cloud Console에서 발급한 키를 입력하세요.
   - 필요하다면 `GEMINI_MODEL` 값을 원하는 모델(`gemini-2.5-flash`, `gemini-2.5-pro` 등)로 지정합니다. 지정하지 않으면 기본값(`gemini-2.5-flash`)이 사용됩니다.
   - 음성 출력(TTS)을 사용하려면 `USE_TTS=true`로 변경하세요.

## 실행 방법

콘솔에서 다음 명령을 실행하면 애플리케이션이 시작됩니다:

```bash
python main.py
```

프로그램이 실행되면 화면에 사용 안내가 표시됩니다. 마이크가 제대로 연결되어 있고 PyAudio가 설치되어 있다면 **말로 질문**을 입력할 수 있으며, 프로그램이 자동으로 음성을 텍스트로 변환합니다. 만약 마이크를 사용하지 못하는 경우(예: PyAudio 미설치, 마이크 부재 등)에는 콘솔에 질문을 **직접 입력**할 수 있도록 안내가 나타납니다. 모델이 생성한 응답은 항상 콘솔에 출력되며, `USE_TTS=true`로 설정되어 있으면 음성으로도 들을 수 있습니다.

## 폴더 구조

```
ShuviAI/
│  .env.example      # 환경 변수 예시
│  .gitignore        # Git에서 추적하지 않을 파일 목록
│  README.md         # 프로젝트 소개 및 실행 방법
│  requirements.txt  # 프로젝트 의존성 목록
│  config.py         # 환경 설정을 불러오는 모듈
│  main.py           # 프로그램의 실행 진입점
├─ai/
│  ├─__init__.py
│  └─gemini.py       # Gemini 모델 호출 로직
├─input/
│  ├─__init__.py
│  └─voice_input.py  # 마이크 입력 처리 및 음성→텍스트 변환
└─tts/
   ├─__init__.py
   └─speech.py       # 텍스트→음성 변환(TTS) 로직
```

## 참고

* `requirements.txt`에 정의된 라이브러리는 Windows 환경을 기준으로 작성되었습니다. 일부 패키지(`pyaudio` 등)는 시스템 환경에 따라 설치 방법이 다를 수 있으며, 위에서 설명한 대로 `pipwin`을 이용해 설치하는 것이 좋습니다.
* `speech_recognition` 모듈은 Google 웹 서비스에 의존하여 음성 인식을 수행합니다. 오프라인 인식을 원한다면 다른 STT 라이브러리를 도입하거나 구현을 수정해야 합니다.
* Google Gemini API 사용량에는 요금이 부과될 수 있으므로 사용 전 과금 정책을 확인하세요.

향후 디스코드 봇으로 이식할 때는 현재 모듈 구조를 그대로 가져와 디스코드 봇에서 `voice_input`, `ai`, `tts` 모듈을 재사용하면 됩니다.