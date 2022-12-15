import traceback
from pprint import pprint

import os
from invoice_utils.invoice_utils import find_text, find_next_word
from invoice_utils.pdf2df import convert_to_df
from invoice_utils.invoice_utils import write_excel_sheet


def get_invoice_no(df):
    invoice_no = 'NULL'
    try:
        pos = find_text(df, 'Invoice')
        invoice_no = df[pos[0] + 1:pos[0] + 2]['TEXT'].values[0]
        return invoice_no
    except Exception as e:
        print(str(e))
        pass
    return invoice_no

def get_invoice_date(df):
    invoice_date ='NULL'
    try:
        pos_date = find_text(df, 'date')[0]
        invoice_date = df[pos_date + 1:pos_date + 2]['TEXT'].values[0]
    except Exception as e:
        print(str(e))
        pass
    return invoice_date

def get_table_data(df):

    result = list()
    page_no = df['page_no'].unique()
    try:
        for page in page_no:
            mydf = df[df['page_no'] == page].reset_index(drop=True)
            get_result(mydf, result)
    except Exception as e:
        traceback.print_exc()

    return result

def get_result(df, result):
    table_start = find_next_word(df, 'nett', 'price')
    table_end = find_text(df, 'comment')
    if not len(table_end):
        table_data = df[table_start[0]:]
    else:
        table_data = df[table_start[0]:table_end[0]]
    msg = dict()
    for index, row in table_data.iterrows():
        #     print(row['TEXT'])

        if row['X1'] < 20:
            msg = dict()
            msg['part'] = row['TEXT']
            msg['desc'] = ''

        if ('part' in msg) and (200 < row['X1'] < 450):
            msg['desc'] = msg['desc'] + " " + row['TEXT']
            msg['qty'] = ''

        if 'qty' in msg and 500 < row['X1'] < 560 and (msg['qty'] == ''):
            msg['qty'] = row['TEXT']
            msg['unit'] = 0

        if 'unit' in msg and 580 < row['X1'] < 640:
            msg['unit'] = row['TEXT']
            msg['disc'] = 0
            msg['total'] = 0

        if 'disc' in msg and 680 < row['X1'] < 730:
            msg['disc'] = row['TEXT']
            print(row['TEXT'])
            msg['total'] = 0

        if 'total' in msg and 720 < row['X1'] < 800:
            msg['total'] = row['TEXT']
            pprint(msg)
            result.append(msg)
            msg = dict()


def start_process(df, excel_filepath):
    result = dict()
    invoice_no = get_invoice_no(df)
    invoice_date = get_invoice_date(df)
    items = get_table_data(df)
    result['invoice_no'] = invoice_no
    result['invoice_date'] = invoice_date
    result['items'] = items
    pprint(result)
    print('Excel File List :', excel_filepath)
    latest_file = os.listdir(excel_filepath)[0]
    prev_filename = os.path.join(excel_filepath, latest_file)
    write_excel_sheet(prev_filename, result, 'BPX')


if __name__ == '__main__':
    print('This kumar')
    filename = '../pdf_data/BPX/BPX -  I0655786 - CP216-2.pdf'
    df = convert_to_df(filename)
    # import pandas as pd
    # df = pd.read_csv('../csv_data/BPX.csv')
    # # get_table_data(df)
    excel_template = r'../excel_data/output_template.xlsx'
    output_path = r'../output_excel/bpx.xlsx'
    excel_filepath = r'../excel_data'
    start_process(df, excel_filepath)





