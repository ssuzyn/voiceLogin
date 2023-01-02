from flask import Flask, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
from werkzeug.utils import secure_filename
import os
import voice

mysql = MySQL()
app = Flask(__name__)


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'annie1004'
app.config['MYSQL_DATABASE_DB'] = 'voice'
mysql.init_app(app)

@app.route("/", methods=['POST', 'GET'])
def main():
    return render_template("main.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    return render_template("login.html")

@app.route("/signup", methods=['POST', 'GET'])
def signup():
    return render_template("signup.html")

@app.route("/upload/success")
def upload_success():
    return render_template('check.html')

@app.route("/upload/fail")
def upload_fail():
    return render_template('main.html')

@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if(request.method=='POST'):
        data = request.files['audio_data']
        id = request.form['id']
        print("현재 디렉토리 위치 : ", os.getcwd())
        #print(data.read())
        data.save('static/uploads/' + secure_filename(data.filename))
        files = os.listdir("static/uploads")
        pwd = voice.transform(data.filename, id)
        return redirect(url_for('upload_success'))
    else:
        return redirect(url_for('upload_fail'))

if __name__=="__main__":
  app.run(debug=True)