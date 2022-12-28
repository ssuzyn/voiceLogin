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
                //mediaRecorder.exportWAV(createDownloadLink)
            }

            mediaRecorder.onstop = e => {
                console.log("data available after MediaRecorder.stop() called.")

                const clipName =  new Date().toISOString();

                const clipContainer = document.createElement('article')
                const clipLabel = document.createElement('p')
                const audio = document.createElement('audio')
                const deleteButton = document.createElement('button')
                const uploadButton = document.createElement('button')


                clipContainer.classList.add('clip')
                audio.setAttribute('controls', '')
                deleteButton.innerHTML = "삭제"
                uploadButton.innerHTML = "업로드"
                clipLabel.innerHTML = clipName

                clipContainer.appendChild(audio)
                clipContainer.appendChild(clipLabel)
                clipContainer.appendChild(deleteButton)
                clipContainer.appendChild(uploadButton)
                soundClips.appendChild(clipContainer)

                audio.controls = true
                const blob = new Blob(chunks, {
                    'type': 'audio/ogg codecs=opus'
                })
                console.log(new Uint8Array(blob))
                chunks = []
                const audioURL = URL.createObjectURL(blob)
                audio.src = audioURL
                console.log("recorder stopped")
                console.log(audio.src)

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
function createDownloadLink(blob) {

    var url = URL.createObjectURL(blob);
    var au = document.createElement('audio');
    var li = document.createElement('li');
    var link = document.createElement('a');

    //name of .wav file to use during upload and download (without extendion)
    var filename = new Date().toISOString();

    //add controls to the <audio> element
    au.controls = true;
    au.src = url;

    //save to disk link
    link.href = url;
    link.download = filename+".wav"; //download forces the browser to donwload the file using the  filename
    link.innerHTML = "Save to disk";

    //add the new audio element to li
    li.appendChild(au);

    //add the filename to the li
    li.appendChild(document.createTextNode(filename+".wav "))

    //add the save to disk link to li
    li.appendChild(link);

    //upload link
    var upload = document.createElement('a');
    upload.href="#";
    upload.innerHTML = "Upload";
    upload.addEventListener("click", function(event){
          var xhr=new XMLHttpRequest();
          xhr.onload=function(e) {
              if(this.readyState === 4) {
                  console.log("Server returned: ",e.target.responseText);
              }
          };
          var fd=new FormData();
          fd.append("audio_data",blob, filename);
          xhr.open("POST","/",true);
          xhr.send(fd);
    })
    li.appendChild(document.createTextNode (" "))//add a space in between
    li.appendChild(upload)//add the upload link to li

    //add the li element to the ol
    recordingsList.appendChild(li);
}