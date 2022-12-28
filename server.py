from flask import Flask
from flask import request
from flask import render_template
import os

app = Flask(__name__, static_folder='./static/')

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        f = open('./1.wav', 'wb')
        f.write(request.get_data("audio_data"))
        f.close()
        if os.path.isfile('./1.wav'):
            print("./1.wav exists")

        return render_template('index.html', request="POST")   
    else:
        return render_template("index.html")

if __name__=="__main__":
  app.run(debug=True)