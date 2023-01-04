from flask import Flask, jsonify, request, render_template, redirect, url_for
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

@app.route("/signup/success", methods=['GET'])
def upload_success():
    return render_template('check.html')

@app.route("/upload", methods=['POST'])
def upload():
    if(request.method=='POST'):
        data = request.files['audio_data']
        id = request.form['id']
        cnt = request.form['cnt']
        #print(data.read())
        path = './static/uploads/' + id + '/'
        if not os.path.isdir(path) :
            os.makedirs(path)
        
        data.save(path + secure_filename(data.filename))
        files = os.listdir("static/uploads")
        pwd = voice.transform(data.filename, id, cnt)
        print(pwd)
        print("현재 디렉토리 위치 : ", os.getcwd())
        #dbconn.database().signup(id, pwd)
        return jsonify({'host': '127.0.0.1', 'port': '5000'})

if __name__=="__main__":
  app.run(debug=True)