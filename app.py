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



def check_files(directory, components):
    import os
    import ast
    import pkg_resources
    # 定义字典，用于保存找到的开源组件及其版本号
    used_components = {}

    # 遍历指定目录下的所有java代码文件
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".java"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as f:
                    code = f.read()
                # 将代码解析为抽象语法树
                tree = ast.parse(code)
                # 遍历查找所有的导入语句
                for node in ast.iter_child_nodes(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            # 检查导入的模块名是否包含指定的开源组件名称
                            for component in components:
                                if component in alias.name:
                                    used_components[component] = None

                    elif isinstance(node, ast.ImportFrom):
                        # 检查导入的模块名是否包含指定的开源组件名称
                        for component in components:
                            if component in node.module:
                                used_components[component] = None
                        # 检查导入的子模块名是否包含指定的开源组件名称
                        for alias in node.names:
                            for component in components:
                                if component in alias.name:
                                    used_components[component] = None

    # 遍历所有已安装的包，查找使用的开源组件并获取它们的版本号
    for package in pkg_resources.working_set:
        for component, version in used_components.items():
            if component in package.project_name.lower():
                used_components[component] = package.version

    # 返回找到的开源组件及其版本号
    return used_components
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
    components = ['fastjson', 'commons', 'spring', 'hibernate', 'log4j', 'tomcat', 'junit', 'selenium', 'kafka','redis']#开源组件列表
    path = request.form.get('path')#检索的目录
    res = check_files(path,components)
    return res