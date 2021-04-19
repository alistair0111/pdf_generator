from flask import Flask,render_template
from flask import after_this_request
from flask import *
from i2p import i2pconverter, i2pconverterAutoCrop, pdfMerger
import glob, os
import io
import string
import random
from multiprocessing import Process
from datetime import datetime
import time
app = Flask(__name__)


UPLOAD_FOLDER = ""
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def welcome():
    return render_template('welcome.html')


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route('/normalPDF')
def index():
    return render_template('normal.html')


@app.route('/autoCropPDF')
def autoCropPDF():
    return render_template('autoCrop.html')


@app.route('/mergePDF')
def mergePDF():
    return render_template('mergePDF.html')
    
# @app.route('/', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':
#         if 'files[]' not in request.files:
#             return redirect(request.url)

#         files = request.files.getlist('files[]')

#         for file in files:
#             if file and allowed_file(file.filename):
#                 filename = secure_filename(file.filename)
#                 file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#         flash('File(s) successfully uploaded')
#         return redirect('/')

@app.route('/converted',methods = ['GET', 'POST'])
def convert():
    if request.method == 'POST':

        files = request.files.getlist('img')
        N = 3
        folderName = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
        folderName += "-"
        now = datetime.now()
        folderName += now.strftime("%d-%m-%Y--%H-%M-%S")

        global UPLOAD_FOLDER
        UPLOAD_FOLDER = os.path.join(folderName)

        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        for file in files:
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(UPLOAD_FOLDER, filename))
    i2pconverter(files, UPLOAD_FOLDER)
    return render_template('converted.html')


@app.route('/convertAutoCrop',methods = ['GET', 'POST'])
def convertAutoCrop():
    if request.method == 'POST':

        files = request.files.getlist('img')
        N = 3
        folderName = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
        folderName += "-"
        now = datetime.now()
        folderName += now.strftime("%d-%m-%Y--%H-%M-%S")

        global UPLOAD_FOLDER
        UPLOAD_FOLDER = os.path.join(folderName)

        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        for file in files:
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(UPLOAD_FOLDER, filename))
    i2pconverterAutoCrop(files, UPLOAD_FOLDER)
    return render_template('converted.html')


@app.route('/convertMergePDF',methods = ['GET', 'POST'])
def convertMergePDF():
    if request.method == 'POST':

        files = request.files.getlist('img')
        N = 3
        folderName = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k = N))
        folderName += "-"
        now = datetime.now()
        folderName += now.strftime("%d-%m-%Y--%H-%M-%S")

        global UPLOAD_FOLDER
        UPLOAD_FOLDER = os.path.join(folderName)

        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        for file in files:
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(UPLOAD_FOLDER, filename))
    pdfMerger(files, UPLOAD_FOLDER)
    return render_template('converted.html')

@app.route('/downloadPDF', methods=['GET'])
def downloadPDF():
    global UPLOAD_FOLDER
    filename = UPLOAD_FOLDER+".pdf"
    try:
        filelist = [ f for f in os.listdir(UPLOAD_FOLDER) ]
        for f in filelist:
            os.remove(os.path.join(UPLOAD_FOLDER, f))
    except Exception as e:
        pass
    try:
        os.rmdir(UPLOAD_FOLDER)
    except Exception as e:
        print(e)
    print("HOLA ",filename)

    try:
        with open(filename, 'rb') as fo:
            return_data = io.BytesIO()
            return_data.write(fo.read())
        return_data.seek(0)
        os.remove(filename)
    except Exception as e:
        print(e)

    # print("Above os.remove()")
    
    try: 
        return send_file(return_data, mimetype='application/pdf', as_attachment=True, cache_timeout=0, attachment_filename=filename)
    except Exception as e:
        return redirect(url_for('dashboard'))

    # background_remove(filename)

    # return send_file(filename, mimetype='application/pdf', as_attachment=True, cache_timeout=0)


def background_remove(path):
    task = Process(target=rm(path))
    task.start()


def rm(path):
    os.remove(path)

# def job():
#     allPDFS = [os.remove(file) for file in os.listdir(os.getcwd()) if file.endswith('.pdf')]
    
# schedule.every(5).minutes.do(job)

if __name__ == '__main__':
    app.run(debug = True)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
