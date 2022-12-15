from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from main import process_pdf_files
# from pdf2Image import convert_upload
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'Upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ZIP_FOLDER'] = 'Archive'
app.config['EXCEL_PATH'] = 'excel_data'
app.config['EXCEL_TEMPLATE'] = 'excel_template'

@app.route('/', methods= ['GET'])
def main_code():
    if request.method == 'GET':

        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
        print('File Removed from UPLOAD FOLDER')
        return render_template('upload.html')
    else:
        return '404 Error in Website '

@app.route('/upload',methods = ['GET','POST'])
def upload_file():
    if request.method =='POST':
        files = request.files.getlist("file[]")
        print(request.files)
        for file in files:
            filename = secure_filename(os.path.basename(file.filename))
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        """All Files Uploaded Now Call Main Program"""
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('show_pdf_table.html', len=len(files), result=files)
    return render_template('upload.html')

@app.route('/pdf2excel',methods = ['GET','POST'])
def pdf_2_excel():

    if request.method =='GET':
        """All Files Uploaded Now Call Main Program"""

        files = os.listdir(app.config['UPLOAD_FOLDER'])

        process_pdf_files(
            input_folder=app.config['UPLOAD_FOLDER'],
            excel_path=app.config['EXCEL_PATH'],
            archive_path=app.config['ZIP_FOLDER'],
            excel_template=app.config['EXCEL_TEMPLATE']
        )

        return render_template('pdf2excel.html')

    return render_template('404 Error in the code')

@app.route('/download',methods=['GET'])
def download_file():
    try:

        return send_file(
                        'Archive/download.zip',
                         attachment_filename='download.zip',
                         cache_timeout=0,
                         as_attachment=True
                         )

    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    app.run(debug = True)