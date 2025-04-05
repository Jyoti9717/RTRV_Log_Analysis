import os
from werkzeug.utils import secure_filename
from datetime import datetime


def output_file(file_name):
    output_path = "static/download_file"
    return output_path+'/'+file_name[:-4]+'.csv'

def fil_read(args):
    with open(args,encoding ='cp437') as Load_file:
        file_content = Load_file.read()
        return file_content.split('\n')

def change_filename(filename):
    new_name=secure_filename(datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")+'_'+filename)
    return new_name

def get_uploaded_file(filename):
    file_path = os.path.join('static\\uploaded_files',filename)
    return file_path
