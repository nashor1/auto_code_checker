import os
import re
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/upload'

def allowed_file(filename):
    allow_filename = {'txt','py','json','js','java','md','php','html'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allow_filename

def has_license(path):
    xieyi_name = r"(?i)(MIT|Apache|GPL|BSD)"
    for root, dirs, files in os.walk(path):
        for file in files:
            filename = os.path.join(root, file)
            if not os.path.isfile(filename):
                continue
            with open(filename, "r") as f:
                content = f.read()
                if re.search(xieyi_name, content):
                    return True
    return False

@app.route('/')
def index():
    return render_template('upload.html', upload_path=app.config['UPLOAD_FOLDER'])

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "请选择要上传的文件"
    file = request.files['file']
    if file.filename == '':
        return "请选择要上传的文件"
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return "文件上传成功"
    else:
        return "文件格式不正确"

@app.route('/check', methods=['POST'])
def check():
    path = request.form.get('path')
    if has_license(path):
        return "存在开源协议"
    else:
        return "不存在开源协议"
