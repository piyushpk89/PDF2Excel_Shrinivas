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
        invoice_no = df[pos[1] + 3:pos[1] + 4]['TEXT'].values[0]
        return invoice_no
    except Exception as e:
        print(str(e))
        pass
    return invoice_no

def get_invoice_date(df):
    invoice_date ='NULL'
    try:
        pos = find_text(df, 'date')
        invoice_date = df[pos[0] + 2:pos[0] + 3]['TEXT'].values[0]
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
        table_start = find_text(df, 'Quantity')
        print(table_start[1])
        table_end = find_text(df, 'Item', case=True)
        if table_end.__len__() < 2:
            table_end = find_text(df, 'items', case=True)
        print(table_end)
        table_data = df[table_start[1]:table_end[-1]]

        for index, row in table_data.iterrows():

            if (40 < row['X1'] < 52):
                #         print(row['TEXT'])
                if ('part' in msg):
                    result.append(msg)
                    pprint(msg)

                msg = dict()
                msg['item'] = row['TEXT']
                msg['part'] = table_data.loc[index + 1]['TEXT']
                msg['desc'] = ''

            if row['TEXT'].__contains__('disc'):
                msg['disc'] = table_data.loc[index + 1]['TEXT']

            if ('part' in msg) and (row['TEXT'].__contains__('EA') or row['TEXT'].__contains__('PU')) and (
                    'qty' not in msg):
                msg['qty'] = table_data.loc[index - 1]['TEXT']

            elif ('part' in msg) and (70 < row['X1'] < 230):
                msg['desc'] = msg['desc'] + " " + row['TEXT']

            elif ('qty' in msg) and (385 < row['X1'] < 422) and ('unit' not in msg):
                msg['unit'] = row['TEXT']

            elif ('unit' in msg) and (510 < row['X1'] < 565) and ('total' not in msg):
                msg['total'] = row['TEXT']

        result.append(msg)


    except Exception as e:
        traceback.print_exc()

    return result


def start_process(df, excel_filepath):
    result = dict()
    df = df[df['page_no'] == 1].reset_index(drop=True)
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
    write_excel_sheet(prev_filename, result, 'Rittal')



if __name__ == '__main__':
    print('This kumar')
    # filename = '../pdf_data/Rittal/Rittal - 4220014716 - CP267.pdf'
    filename = '../multipdf/RITTAL Invoice 4220025684.PDF'
    df = convert_to_df(filename)
    excel_filepath = r'../excel_data'
    # convert_pdf_to_csv(filename, r'../csv_data/backup/eew_71.csv')
    start_process(df, excel_filepath)





