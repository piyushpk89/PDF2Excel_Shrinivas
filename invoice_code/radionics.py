import traceback
from pprint import pprint
import os

import sys
sys.path.append("../")

from invoice_utils.invoice_utils import find_text, find_next_word
from invoice_utils.pdf2df import convert_to_df, convert_pdf_to_csv
from invoice_utils.invoice_utils import write_excel_sheet


def get_invoice_no(df):
    invoice_no = 'NULL'
    try:
        pos = find_next_word(df, 'Invoice', 'No.')
        invoice_no = df[pos[0] + 2:pos[0] + 3]['TEXT'].values[0]

        return invoice_no
    except Exception as e:
        print(str(e))
        pass
    return invoice_no

def get_invoice_date(df):
    invoice_date ='NULL'
    try:
        pos_date = find_text(df, 'date')[0]
        date = df[pos_date + 3:pos_date + 4]['TEXT'].values[0]
        invoice_date = date
        # invoice_no = po_data[1]
        return invoice_date
    except Exception as e:
        print(str(e))
        pass
    return invoice_date

def get_table_data(df):
    msg = dict()
    result = list()
    try:
        table_start = find_next_word(df, 'qty', 'sales')
        table_end = find_text(df, 'Standard')
        table_data = df[table_start[0]:table_end[0]]

        for index, row in table_data.iterrows():

            if row['X1'] < 39:
                msg = dict()
                msg['item'] = row['TEXT']
                msg['part'] = ''

            if ('part' in msg) and (50 < row['X1'] < 87):
                msg['part'] = row['TEXT']
                msg['desc'] = ''

            if ('desc' in msg) and (100 < row['X1'] < 250):
                msg['desc'] = msg['desc'] +" "+ row['TEXT']
                msg['qty'] = ''

            if ('qty' in msg) and (280 < row['X1'] < 357):
                if not row['TEXT'].__contains__('EA'):
                    msg['qty'] = row['TEXT']
                    msg['unit'] = 0

            if ('unit' in msg) and (450 < row['X1'] < 479):
                msg['unit'] = row['TEXT']
                msg['total'] = 0

            if ('total' in msg) and (500 < row['X1'] < 530):
                msg['total'] = row['TEXT']
                pprint(msg)
                result.append(msg)
                msg = dict()


    except Exception as e:
        traceback.print_exc()

    return result


def start_process(df, excel_filepath):
    result = dict()
    invoice_no = get_invoice_no(df)
    invoice_date = get_invoice_date(df)
    items = get_table_data(df)
    result['invoice_no'] = invoice_no
    result['invoice_date'] = invoice_date
    result['items'] = items
    pprint(result)
    latest_file = os.listdir(excel_filepath)[0]
    prev_filename = os.path.join(excel_filepath, latest_file)
    write_excel_sheet(prev_filename, result, 'Radionics')



if __name__ == '__main__':
    print('This kumar')
    # filename = '../pdf_data/Radionics/Radionics_v1.pdf'
    filename = '../pdf_issue/radionics_1.pdf'
    df = convert_to_df(filename)
    excel_filepath = r'../excel_data'
    # convert_pdf_to_csv(filename, r'../csv_data/backup/eew_71.csv')
    start_process(df, excel_filepath)





