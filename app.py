import AIBOT
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.static_folder = 'static'

UPLOAD_FOLDER = 'knowledge_base'  # 上传文件存储的路径
ALLOWED_EXTENSIONS = {'md', 'pdf'}  # 允许上传的文件扩展名
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.debug=True
app.secret_key=os.urandom(24)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(AIBOT.get_zhipuai_response(userText))


# 检查文件扩展名是否合法
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 上传文件并重定向用户到上传后的文件URL
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 检查请求中是否包含文件部分
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # 如果用户没有选择文件，浏览器也会提交一个没有文件名的空文件
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file', filename=filename))
    return


if __name__ == "__main__":
    app.run()