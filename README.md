## 샴네트워크 모델을 활용한 음성 로그인

녹음된 음성을 파형 이미지로 변환한 후 샴네트워크 모델로 학습 및 추론

### 1. 녹음

- 회원가입 : static/js/signup.js
- 로그인 : static/js/login.js
  정확한 학습을 위해 회원가입시 3번의 녹음이 필요
---

### 2. wav파일 -> 이미지 변환

<server.py>
- 회원가입 : signup_upload()
- 로그인 : login_upload()

<siamese/voice.py>

녹음된 wav파일을 MFCC로 변환시켜 반환
변환된 이미지는 회원가입한 아이디를 폴더명으로 하여 저장된다
저장 경로: static/uploads/{아이디}

---

### 3. 학습

<siamese/train.py>

회원가입 성공시 실행
완료된 학습 모델은 siamese/model/test.pt로 저장

---

### 4. 추론

<siamese/inference.py> -> run()

로그인을 위한 녹음 후 실행

이미지 변환을 거친 파일을 static/login/{아이디} 경로로 저장

학습 모델 test.pt를 바탕으로 test(로그인)와 train(회원가입) 추론

기준: 현재 로그인 하려는 id와 추론된 id의 동일 여부

- 추론 성공: login success
- 추론 실패: login fail
