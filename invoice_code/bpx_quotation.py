import traceback
from pprint import pprint
import sys
sys.path.append('../')
import os
from invoice_utils.invoice_utils import find_text, find_next_word
from invoice_utils.pdf2df import convert_to_df
from invoice_utils.invoice_utils import write_excel_sheet


def get_invoice_no(df):
    quotation_no = 'NULL'
    try:
        pos = find_text(df, 'Quotation')
        quotation_no = df[pos[0] + 1:pos[0] + 2]['TEXT'].values[0]

        return quotation_no
    except Exception as e:
        print(str(e))
        pass
    return quotation_no

def get_invoice_date(df):
    date ='NULL'
    try:
        pos_date = find_text(df, 'date')[0]
        date = df[pos_date + 1:pos_date + 2]['TEXT'].values[0]
    except Exception as e:
        print(str(e))
        pass
    return date

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
    table_start = find_next_word(df, 'Description', 'Price')
    table_data = df[table_start[0]:]
    msg = dict()
    for index, row in table_data.iterrows():
        #     print(row['TEXT'])
        if row['X1'] < 40:
            if len(msg.keys()) > 4:
                result.append(msg)
                msg = dict()
            msg['qty'] = row['TEXT']
            msg['part'] = ""

        if ('part' in msg) and (50 < row['X1'] < 80):
            msg['part'] = row['TEXT']
            msg['desc'] = ''

        if ('desc' in msg) and (250 < row['X1'] < 450):
            if len(msg['desc']) < 3:
                msg['desc'] = row['TEXT']
                msg['unit'] = 0
            else:
                msg['desc'] = msg['desc'] + " " + row['TEXT']

        if 'unit' in msg and (600 < row['X1'] < 650):
            msg['unit'] = row['TEXT']
            msg['disc'] = 0
            msg['total'] = 0

        if 'disc' in msg and 690 < row['X1'] < 700:
            msg['disc'] = row['TEXT']
            #         print(row['TEXT'])
            msg['total'] = 0

        if 'total' in msg and 730 < row['X1'] < 770:
            msg['total'] = row['TEXT']

    if len(msg.keys()) > 4:
        result.append(msg)

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
    filename = '../pdf_issue/bpx_1.pdf'
    df = convert_to_df(filename)
    # import pandas as pd
    # df = pd.read_csv('../csv_data/BPX.csv')
    # # get_table_data(df)
    excel_template = r'../excel_data/output_template.xlsx'
    output_path = r'../output_excel/bpx.xlsx'
    excel_filepath = r'../excel_data'
    start_process(df, excel_filepath)





