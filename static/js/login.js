// 엘리먼트 취득
//const $audioEl = document.querySelector("audio");
const submit = document.getElementById("submit");
const login = document.getElementById("login");
const pwd = document.getElementById("pwd");
const id = document.getElementById("id");

// 녹음중 상태 변수
let isRecording = false;

// MediaRecorder 변수 생성
let mediaRecorder = null;

// 녹음 데이터 저장 배열
const audioArray = [];

let blob;

pwd.onclick = async function (event) {
  if (!isRecording) {
    // 마이크 mediaStream 생성: Promise를 반환하므로 async/await 사용
    const mediaStream = await navigator.mediaDevices.getUserMedia({
      audio: true,
    });

    // MediaRecorder 생성
    mediaRecorder = new MediaRecorder(mediaStream);

    // 이벤트핸들러: 녹음 데이터 취득 처리
    mediaRecorder.ondataavailable = (event) => {
      audioArray.push(event.data); // 오디오 데이터가 취득될 때마다 배열에 담아둔다.
      Object.keys(event.data).forEach((key) => {
        console.log(key);
        console.log(audioArray[key]);
      });
    };

    // 이벤트핸들러: 녹음 종료 처리 & 재생하기
    mediaRecorder.onstop = (event) => {
      // 녹음이 종료되면, 배열에 담긴 오디오 데이터(Blob)들을 합친다: 코덱도 설정해준다.
      blob = new Blob(audioArray, { type: "audio/ogg codecs=opus" });
      audioArray.splice(0); // 기존 오디오 데이터들은 모두 비워 초기화한다.
    };

    // 녹음 시작
    mediaRecorder.start();
    console.log("recording start");
    pwd.style.backgroundColor = "red";
    isRecording = true;
  } else {
    // 녹음 종료
    mediaRecorder.stop();
    console.log("recording stop");
    pwd.style.backgroundColor = "lightGray";
    isRecording = false;
    submit.diabled = true;
  }
};

submit.onclick = async function (event) {
  console.log("Audio being exported.");
  var filename = id.value + ".wav";
  // console.log(filename)
  console.log(blob);
  let fd = new FormData();
  fd.append("audio_data", blob, filename);
  fd.append("id", id.value);
  console.log(fd);

  fetch("http://127.0.0.1:5000/login/upload", { method: "POST", body: fd })
    .then((res) => {
      if (res.redirected) {
        window.location.href = res.url;
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

login.onclick = async function (event) {
  window.location.href = "http://127.0.0.1:5000/login/success";
};
