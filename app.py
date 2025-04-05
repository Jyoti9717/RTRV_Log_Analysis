from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime,date
import os
# from Algo import *
from module_functions import *
from eng_log import *

UPLOAD_FOLDER = "static/uploaded_files"
ALLOWED_EXTENSION = {'txt'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION


@app.route('/execute',methods=['POST'])
def upload_file():
    try:
        if request.method == 'POST':
            selected_date = request.form.get('selected_date')
            selected_hours = request.form.get('selected_hours')
            selected_minutes = request.form.get('selected_minutes')
            selected_time = selected_hours + ':' + selected_minutes
            if 'file' not in request.files:
                return jsonify("no file part ")
            file = request.files['file']
            if file.filename == '':
                return jsonify("Please Select A File")
            if 'txt' not in file.filename:
                return jsonify("only .text file allowed")
            if file.filename and allowed_file(file.filename):
                filename = change_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                uploaded_file= get_uploaded_file(filename)
                tbl = eng_log(uploaded_file, selected_date,selected_time)
                tbl.to_csv(output_file(filename), index=False)
        return render_template('index.html')
    except Exception:
        return jsonify("Sorry! Content Not Found In Uploaded Text File.")

if __name__ == "__main__":
    app.run(debug=True)

