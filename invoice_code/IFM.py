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
        pos = find_next_word(df, 'Invoice', 'no.')
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
        date = df[pos_date + 1:pos_date + 2]['TEXT'].values[0]
        invoice_date = date
        # invoice_no = po_data[1]
        return invoice_date
    except Exception as e:
        print(str(e))
        pass
    return invoice_date


def rearrange(df):
    for i in range(1, len(df)):
        temp = df.loc[i, 'Y1'] - df.loc[i - 1, 'Y1']
        if -5 < temp < 10:
            df.loc[i, 'Y1'] = df.loc[i - 1, 'Y1']

    return df.sort_values(by=['Y1', 'X1']).reset_index(drop=True)


def get_table_data(df):
    result= list()
    page_no = df['page_no'].unique()
    for page in page_no:
        mydf = df[df['page_no'] == page].reset_index(drop=True)
        get_result(mydf, result)

    return result

def get_result(df, result):

    from pprint import pprint
    msg = dict()
    df = rearrange(df)

    # print(table_end)
    try:
        table_start = find_text(df, '00')
        table_end = find_text(df, 'Country')
        table_data = df[table_start[0]: table_end[-1]]
        table_data = df[table_start[0]:table_end[-1]]
        for index, row in table_data.iterrows():

            if (50 < row['X1'] < 76):
                if 'part' in msg:
                    result.append(msg)
                    pprint(msg)
                msg = dict()
                msg['item'] = row['TEXT']
                msg['part'] = ''
                msg['qty'] = ''
                msg['desc'] = ''

            if ('part' in msg) and (204 < row['X1'] < 300) and (msg['part'] == ''):
                msg['part'] = row['TEXT']

            elif ('desc' in msg) and (204 < row['X1'] < 270):
                msg['desc'] = msg['desc'] + " " + row['TEXT']

            elif ('qty' in msg) and (380 < row['X1'] < 397):
                msg['qty'] = row['TEXT']
                msg['unit'] = 0

            elif ('unit' in msg) and (420 < row['X1'] < 482):
                msg['unit'] = row['TEXT']
                msg['total'] = 0

            elif ('total' in msg) and (500 < row['X1'] < 530):
                msg['total'] = row['TEXT']

        if 'part' in msg:
            result.append(msg)
            pprint(msg)

    except Exception as e:
        pass


def start_process(df, excel_filepath):
    result = dict()

    df_sort= df.sort_values(by=['page_no','Y1','X1']).reset_index(drop=True)
    df = rearrange(df_sort)

    invoice_no = get_invoice_no(df)
    invoice_date = get_invoice_date(df)

    items = get_table_data(df)

    result['invoice_no'] = invoice_no
    result['invoice_date'] = invoice_date
    result['items'] = items

    pprint(result)
    latest_file = os.listdir(excel_filepath)[0]
    prev_filename = os.path.join(excel_filepath, latest_file)
    write_excel_sheet(prev_filename, result, 'IFM')



if __name__ == '__main__':
    print('This kumar')
    # filename = '../multipdf/IFM - 29371311.pdf'
    # filename = '../pdf_data/IFM/IFM - 28850755 - MP334.pdf'
    filename = '../multipdf/IFM - 29371311.pdf'
    df = convert_to_df(filename)
    excel_filepath = r'../excel_data'
    # convert_pdf_to_csv(filename, r'../csv_data/backup/eew_71.csv')
    start_process(df, excel_filepath)





