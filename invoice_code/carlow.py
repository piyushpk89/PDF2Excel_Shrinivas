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
        pos_date = find_text(df, 'page')
        po_data = df[pos_date[0] + 1:pos_date[0] + 3]['TEXT'].values
        invoice_date = po_data[0]
        invoice_no = po_data[1]
        return invoice_no
    except Exception as e:
        print(str(e))
        pass
    return invoice_no

def get_invoice_date(df):
    invoice_date ='NULL'
    try:
        pos_date = find_text(df, 'page')
        po_data = df[pos_date[0] + 1:pos_date[0] + 3]['TEXT'].values
        invoice_date = po_data[0]
        # invoice_no = po_data[1]
        return invoice_date
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
    msg = dict()
    try:
        table_start = find_text(df, 'Total')
        print(table_start)
        table_end = find_text(df, 'Code')
        if not len(table_end) > 1:
            table_data = df[table_start[0]:]

        else:
            table_data = df[table_start[0] + 2:table_end[-1]]

        from pprint import pprint
        msg = dict()
        for index, row in table_data.iterrows():

            #     if row['X1'] < 39:
            #         msg = dict()
            #         msg['item'] = row['TEXT']
            #         msg['part'] = ''
            if (45 < row['X1'] < 71):
                print(row['TEXT'])
                msg = dict()
                msg['qty'] = row['TEXT']
                msg['desc'] = ''
                msg['part'] = 'NA'

            elif ('desc' in msg) and (75 < row['X1'] < 270):
                msg['desc'] = msg['desc'] + " " + row['TEXT']
                msg['unit'] = ''

            elif ('unit' in msg) and (370 < row['X1'] < 400):
                msg['unit'] = row['TEXT']
                msg['total'] = 0

            elif ('total' in msg) and (490 < row['X1'] < 519):
                msg['total'] = row['TEXT']
                try:
                    msg['part'], msg['desc'] = msg['desc'].split('-')
                except Exception as e:
                    print(str(e))
                pprint(msg)
                result.append(msg)
                msg = dict()

    except Exception as e:
        traceback.print_exc()


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
    write_excel_sheet(prev_filename, result, 'Carlow')



if __name__ == '__main__':
    print('This kumar')
    filename = '../multipdf/Carlow Engineering - SIN11569.pdf'
    df = convert_to_df(filename)
    excel_filepath = r'../excel_data'
    # convert_pdf_to_csv(filename, r'../csv_data/backup/eew_71.csv')
    start_process(df, excel_filepath)





