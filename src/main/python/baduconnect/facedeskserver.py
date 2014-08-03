'''
Created on 2014

@author: aadebuger
'''
from flask import Flask
from flask import request
from flask import Flask, request, redirect, url_for
from flask import send_from_directory
from werkzeug import SharedDataMiddleware
from werkzeug import secure_filename
import os
import sys
import json
app = Flask(__name__)

UPLOAD_FOLDER = '/Users/aadebuger/Documents/faces'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

serialid=0
def getNewfilename(filename):
          global serialid
          ext=os.path.splitext(filename)[1] 
          newfilename = "%d.jpg"%(serialid)
          serialid=serialid+1
          return newfilename
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/rank', methods=['GET'])
def rangList():
    list = os.listdir(UPLOAD_FOLDER ) 
    return json.dumps(list)
    
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        try:
                print request.files
                file1 = request.files['file']
                if file and allowed_file(file1.filename):
                    filename = secure_filename(file1.filename)
                    print 'filename=',filename
                    newfilename = getNewfilename(filename)
                    print 'newfilename=',newfilename;
                    file1.save(os.path.join(app.config['UPLOAD_FOLDER'], newfilename))
                    print 'ok'
                    return redirect('/static/listr.html')
#            return redirect(url_for('uploaded_file',
#                                            filename=newfilename))
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
        if len(sys.argv)>=3:
            print 'sys',sys.argv[2]
            localpath=sys.argv[2]
        else:
            localpath='../facedesk'
        if 1:
           app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
                '/static': localpath
            })
           
        if len(sys.argv)>=2:
            UPLOAD_FOLDER= sys.argv[1]
            app.config['UPLOAD_FOLDER'] = sys.argv[1]
        app.run(host="0.0.0.0",port=5000,debug=True)