'''
Created on 2014

@author: aadebuger
'''
from flask import Flask
from flask import request
from flask import Flask, request, redirect, url_for
from flask import send_from_directory

from werkzeug import secure_filename
import os
app = Flask(__name__)

UPLOAD_FOLDER = '/Users/aadebuger/Documents/faces'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
           
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
                file1 = request.files['file']
                if file and allowed_file(file1.filename):
                    filename = secure_filename(file1.filename)
                    print 'filename=',filename
                    file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    print 'ok'
                    return redirect(url_for('uploaded_file',
                                            filename=filename))
        except Exception,e:
            print 'Exception'
            print e
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
if __name__ == '__main__':
        app.run(host="0.0.0.0",port=5000,debug=True)