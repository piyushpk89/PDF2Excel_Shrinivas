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
        pos = find_text(df, 'Number')
        invoice_no = df[pos[0] + 1:pos[0] + 2]['TEXT'].values[0]
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
        table_start = find_text(df, 'Unit')
        table_end = find_next_word(df, 'VAT', 'Analysis')
        table_data = df[table_start[0]:table_end[0]]
        msg = dict()
        result = list()
        for index, row in table_data.iterrows():
            if row['X1'] < 30:
                #         print(row['TEXT'])
                msg = dict()
                msg['part'] = row['TEXT']
                msg['desc'] = ''


            elif ('desc' in msg) and (90 < row['X1'] < 300):
                #         print(row['TEXT'])
                msg['desc'] = msg['desc'] + " " + row['TEXT']
                msg['qty'] = ''

            elif ('qty' in msg) and (340 < row['X1'] < 374):
                #         print(row['TEXT'])
                msg['qty'] = row['TEXT']
                msg['unit'] = ''

            if ('unit' in msg) and (400 < row['X1'] < 438):
                #         print(row['TEXT'])
                msg['unit'] = row['TEXT']
                msg['disc'] = 0
                msg['total'] = 0

            if 'disc' in msg and 470 < row['X1'] < 500:
                msg['disc'] = row['TEXT']
                msg['total'] = 0

            if 'total' in msg and 520 < row['X1'] < 560:
                msg['total'] = row['TEXT']
                pprint(msg)
                result.append(msg)
                msg = dict()

    except Exception as e:
        traceback.print_exc()

    return result


def rearrange(df):
    for i in range(1, len(df)):
        temp = df.loc[i, 'Y1'] - df.loc[i - 1, 'Y1']
        if -5 < temp < 10:
            df.loc[i, 'Y1'] = df.loc[i - 1, 'Y1']

    return df.sort_values(by=['Y1', 'X1']).reset_index(drop=True)

def start_process(df, excel_filepath):
    result = dict()
    df = df.sort_values(by=['Y1', 'X1']).reset_index(drop=True)
    df = rearrange(df)
    invoice_no = get_invoice_no(df)
    invoice_date = get_invoice_date(df)
    items = get_table_data(df)
    result['invoice_no'] = invoice_no
    result['invoice_date'] = invoice_date
    result['items'] = items
    pprint(result)
    latest_file = os.listdir(excel_filepath)[0]
    prev_filename = os.path.join(excel_filepath, latest_file)
    write_excel_sheet(prev_filename, result, 'Kilkenny')


if __name__ == '__main__':
    print('This kumar')
    filename = '../pdf_data/Kilkenny/Kilkenny Welding Supplies Limited_Invoice_PL016142_211020120306567.pdf'
    df = convert_to_df(filename)
    excel_filepath = r'../excel_data'
    # convert_pdf_to_csv(filename, r'../csv_data/backup/eew_71.csv')
    start_process(df, excel_filepath)





