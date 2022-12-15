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
        number = find_text(df, 'Number')
        po_data = df[number[0] + 1:number[0] + 4]['TEXT'].values
        invoice_no = po_data[0]
        return invoice_no
    except Exception as e:
        print(str(e))
        pass
    return invoice_no

def get_invoice_date(df):
    invoice_date ='NULL'
    try:
        number = find_text(df, 'Number')
        po_data = df[number[0] + 1:number[0] + 4]['TEXT'].values
        invoice_date = po_data[2]
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
        table_start = find_text(df, '______________________________________________...')
        table_end = find_text(df, '______________________________________________...')
        table_data = df[table_start[1] + 1:table_end[-1]]

        for index, row in table_data.iterrows():

            #     if row['X1'] < 39:
            #         msg = dict()
            #         msg['item'] = row['TEXT']
            #         msg['part'] = ''
            if (10 < row['X1'] < 31):
                msg = dict()
                msg['part'] = ''

            if ('part' in msg) and (31 < row['X1'] < 120):
                #         print(row['TEXT'])
                msg['part'] = row['TEXT']
                msg['desc'] = ''

            if ('desc' in msg) and (120 < row['X1'] < 234):
                #         print(row['TEXT'])
                msg['desc'] = msg['desc'] + " " + row['TEXT']
                msg['qty'] = ''

            if ('qty' in msg) and (280 < row['X1'] < 295):
                #         print(row['TEXT'])
                msg['qty'] = row['TEXT']
                msg['unit'] = 0

            if ('unit' in msg) and (390 < row['X1'] < 423):
                #         print(row['TEXT'])
                msg['unit'] = row['TEXT']
                msg['total'] = 0

            if ('total' in msg) and (480 < row['X1'] < 516):
                #         print(row['TEXT'])
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
    write_excel_sheet(prev_filename, result, 'SB Steels')



if __name__ == '__main__':
    print('This kumar')
    filename = '../pdf_data/SB/SB Steel -   0091241464.pdf'
    df = convert_to_df(filename)
    excel_filepath = r'../excel_data'
    # convert_pdf_to_csv(filename, r'../csv_data/backup/eew_71.csv')
    start_process(df, excel_filepath)





