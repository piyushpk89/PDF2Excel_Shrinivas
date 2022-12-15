import os.path

import fitz
import pandas as pd

from pdf_utils.pdf2df import convert_pdf_to_csv

if __name__ == '__main__':
    filename = 'pdf_data/Carlow/Carlow Engineering - SIN120039.pdf'
    csv_path = 'csv_data'
    dirname = filename.split('/')[1]
    file = os.path.basename(filename)
    file = file.replace('.pdf','.csv')
    csv_path = csv_path+'/'+dirname+'/'+file
    print(csv_path)
    # print(os.path.basename(filename))
    # print(os.path.dirname(filename))
    # print(os.path.)
    # print(filename.split('/'))
    # print(os.path.)


    convert_pdf_to_csv(filename, csv_path)
