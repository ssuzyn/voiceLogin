from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os, warnings
import voice, dbconn

app = Flask(__name__)
CORS(app)
warnings.filterwarnings(action='ignore')

@app.route("/", methods=['POST', 'GET'])
def main():
    return render_template("main.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    return render_template("login.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    return render_template("signup.html")

@app.route("/upload/success", methods=['GET'])
def upload_success():
    return render_template('check.html')

@app.route("/upload", methods=['POST'])
def upload():
    if(request.method=='POST'):
        data = request.files['audio_data']
        id = request.form['id']
        #print(data.read())
        data.save('static/uploads/' + secure_filename(data.filename))
        files = os.listdir("static/uploads")
        pwd = voice.transform(data.filename, id)
        print(pwd)
        print("현재 디렉토리 위치 : ", os.getcwd())
        #dbconn.database().signup(id, pwd)
        return redirect(url_for('upload_success'))

if __name__=="__main__":
  app.run(debug=True)