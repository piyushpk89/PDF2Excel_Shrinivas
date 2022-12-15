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
        pos = find_text(df, 'Invoice')
        invoice_no = df[pos[1] - 1:pos[1]]['TEXT'].values[0]

        return invoice_no
    except Exception as e:
        print(str(e))
        pass
    return invoice_no

def get_invoice_date(df):
    invoice_date ='NULL'
    try:
        pos = find_text(df, 'Date')
        invoice_date = df[pos[0] + 1:pos[0] + 2]['TEXT'].values[0]
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
        table_start = find_next_word(df, 'Net', 'VAT')
        table_end = find_text(df, 'Delivery')
        table_data = df[table_start[0]:table_end[0]]

        for index, row in table_data.iterrows():

            if (30 < row['X1'] < 52):
                #         print(row['TEXT'])
                msg = dict()
                msg['qty'] = row['TEXT']
                msg['part'] = ''

            if ('part' in msg) and (93 < row['X1'] < 199):
                msg['part'] = row['TEXT']
                msg['desc'] = ''

            if ('desc' in msg) and (200 < row['X1'] < 358):
                msg['desc'] = msg['desc'] + " " + row['TEXT']
                msg['unit'] = "0"
                msg['total'] = "0"

            if ('unit' in msg) and (420 < row['X1'] < 453):
                msg['unit'] = row['TEXT']

            if ('total' in msg) and (476 < row['X1'] < 507):
                msg['total'] = row['TEXT']
                pprint(msg)
                result.append(msg)
                msg = dict()


    except Exception as e:
        traceback.print_exc()

    return result


def start_process(df, excel_filepath):
    result = dict()
    df = df.sort_values(['Y1', 'X1']).reset_index(drop=True)
    invoice_no = get_invoice_no(df)
    invoice_date = get_invoice_date(df)
    items = get_table_data(df)
    result['invoice_no'] = invoice_no
    result['invoice_date'] = invoice_date
    result['items'] = items
    pprint(result)
    latest_file = os.listdir(excel_filepath)[0]
    prev_filename = os.path.join(excel_filepath, latest_file)
    write_excel_sheet(prev_filename, result, 'Technidrive')



if __name__ == '__main__':
    print('This kumar')
    filename = '../pdf_data/Technidrive/Technidrive - 50891 - MP279.pdf'
    df = convert_to_df(filename)
    excel_filepath = r'../excel_data'
    # convert_pdf_to_csv(filename, r'../csv_data/backup/eew_71.csv')
    start_process(df, excel_filepath)





