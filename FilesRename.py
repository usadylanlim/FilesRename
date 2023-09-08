import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 设置上传文件夹
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 主页
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        folder_path = request.form['folder_path']
        letters = request.form['letters']
        start_number = int(request.form['start_number'])
        
        if not os.path.exists(folder_path):
            return "文件夹不存在，请检查路径。"
        
        # 获取文件夹下所有文件
        files = os.listdir(folder_path)
        files.sort()
        
        for i, file in enumerate(files, start=start_number):
            extension = os.path.splitext(file)[1]
            new_name = letters + "{:0{width}d}".format(i, width=len(str(start_number))) + extension
            new_path = os.path.join(folder_path, new_name)
            
            # 检查目标文件是否存在，如果存在，添加数字来避免冲突
            counter = 1
            while os.path.exists(new_path):
                new_name = letters + "{:0{width}d}".format(i, width=len(str(start_number))) + f"_{counter}" + extension
                new_path = os.path.join(folder_path, new_name)
                counter += 1
            
            old_path = os.path.join(folder_path, file)
            os.rename(old_path, new_path)
        
        return "文件重命名完成。"
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
