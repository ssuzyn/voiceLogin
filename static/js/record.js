const record = document.getElementById("record")
const stop = document.getElementById("stop")
const soundClips = document.getElementById("sound-clips")
const chkHearMic = document.getElementById("chk-hear-mic")

//음원정보를 담은 노드를 생성하거나 음원을 실행 또는 디코딩
const audioCtx = new (window.AudioContext || window.webkitAudioContext)() // 오디오 컨텍스트 정의

const analyser = audioCtx.createAnalyser()

function makeSound(stream) { //내 컴퓨터의 마이크나 다른 소스를 통해 발생한 오디오 스트림의 정보를 보여줌
    const source = audioCtx.createMediaStreamSource(stream)
    source.connect(analyser)
    analyser.connect(audioCtx.destination)
}

if (navigator.mediaDevices) { //마이크 사용 권한 획득
    console.log('getUserMedia supported.')

    const constraints = {
        audio: true
    }
    let chunks = []

    navigator.mediaDevices.getUserMedia(constraints)
        .then(stream => {

            const mediaRecorder = new MediaRecorder(stream)

            chkHearMic.onchange = e => {
                if (e.target.checked == true) {
                    audioCtx.resume()
                    makeSound(stream)
                } else {
                    audioCtx.suspend()
                }
            }

            record.onclick = () => {
                mediaRecorder.start()
                console.log(mediaRecorder.state)
                console.log("recorder started")
                record.style.background = "red"
                record.style.color = "black"
            }

            stop.onclick = () => {
                mediaRecorder.stop()
                console.log(mediaRecorder.state)
                console.log("recorder stopped")
                record.style.background = ""
                record.style.color = ""
            }

            mediaRecorder.onstop = e => {
                console.log("data available after MediaRecorder.stop() called.")

                const clipName = prompt("오디오 파일 제목을 입력하세요.", new Date())

                const clipContainer = document.createElement('article')
                const clipLabel = document.createElement('p')
                const audio = document.createElement('audio')
                const deleteButton = document.createElement('button')

                clipContainer.classList.add('clip')
                audio.setAttribute('controls', '')
                deleteButton.innerHTML = "삭제"
                clipLabel.innerHTML = clipName

                clipContainer.appendChild(audio)
                clipContainer.appendChild(clipLabel)
                clipContainer.appendChild(deleteButton)
                soundClips.appendChild(clipContainer)

                audio.controls = true
                const blob = new Blob(chunks, {
                    'type': 'audio/ogg codecs=opus'
                })
                chunks = []
                const audioURL = URL.createObjectURL(blob)
                audio.src = audioURL
                console.log("recorder stopped")

                deleteButton.onclick = e => {
                    evtTgt = e.target
                    evtTgt.parentNode.parentNode.removeChild(evtTgt.parentNode)
                }
            }

            mediaRecorder.ondataavailable = e => {
                chunks.push(e.data)
            }
        })
        .catch(err => {
            console.log('The following error occurred: ' + err)
        })
}