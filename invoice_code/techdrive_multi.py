import traceback
from pprint import pprint

import os
import sys
sys.path.append('../')
from invoice_utils.invoice_utils import find_text, find_next_word
from invoice_utils.pdf2df import convert_to_df
from invoice_utils.invoice_utils import write_excel_sheet


def rearrange(df):
    for i in range(1, len(df)):
        temp = df.loc[i, 'Y1'] - df.loc[i - 1, 'Y1']
        if -5 < temp < 10:
            df.loc[i, 'Y1'] = df.loc[i - 1, 'Y1']

    return df.sort_values(by=['page_no', 'Y1', 'X1']).reset_index(drop=True)

def get_invoice_no(df):
    invoice_no = 'NULL'
    try:
        pos = find_text(df, 'Invoice')
        invoice_no = df[pos[2] - 1:pos[2]]['TEXT'].values[0]
        print(invoice_no)
    except Exception as e:
        print(str(e))
        pass
    return invoice_no

def get_invoice_date(df):
    invoice_date ='NULL'
    try:
        pos = find_text(df, 'Date')
        invoice_date = df[pos[1] + 1:pos[1] + 2]['TEXT'].values[0]
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
    table_start = find_text(df, "Net")
    table_end = find_text(df, 'Commodity')
    print(table_start, table_end)
    table_data = df[table_start[0]:table_end[0]]
    from pprint import pprint
    msg = dict()

    for index, row in table_data.iterrows():
        if (10 < row['X1'] < 106):
            print(row['TEXT'])
            msg['part'] = row['TEXT']
            msg['qty'] = row['TEXT']

        elif ((159 < row['X1'] < 165) and ('qty' in msg)):
            print(row['TEXT'])
            msg['qty'] = row['TEXT']
            msg['desc'] = ""

        elif ((190 < row['X1'] < 308) and ('desc' in msg)):
            print(row['TEXT'])
            msg['desc'] = msg['desc'] + " " + row['TEXT']
            msg['total'] = ''

        elif (500 < row['X1'] < 544) and ('total' in msg):
            msg['total'] = row['TEXT']
            pprint(msg)
            msg['unit']  = str(float(msg['total'])/int(msg['qty']))
            result.append(msg)
            msg = dict()




def start_process(df, excel_filepath):
    result = dict()
    df = df.sort_values(['page_no', 'Y1', 'X1']).reset_index(drop=True)
    mydf = df[df.page_no == 1]
    invoice_no = get_invoice_no(mydf)
    invoice_date = get_invoice_date(mydf)
    df = rearrange(df)
    items = get_table_data(df)
    result['invoice_no'] = invoice_no
    result['invoice_date'] = invoice_date
    result['items'] = items
    pprint(result)
    print('Excel File List :', excel_filepath)
    latest_file = os.listdir(excel_filepath)[0]
    prev_filename = os.path.join(excel_filepath, latest_file)
    write_excel_sheet(prev_filename, result, 'Techdrive')


if __name__ == '__main__':
    print('This kumar')
    filename = '../multipdf/Technidrive - 58181.pdf'
    df = convert_to_df(filename)
    # import pandas as pd
    # df = pd.read_csv('../csv_data/BPX.csv')
    # # get_table_data(df)
    excel_template = r'../excel_data/output_template.xlsx'
    output_path = r'../output_excel/bpx.xlsx'
    excel_filepath = r'../excel_data'
    start_process(df, excel_filepath)





