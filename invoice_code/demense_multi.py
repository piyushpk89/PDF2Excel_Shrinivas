import traceback
from pprint import pprint
import os
import sys
sys.path.append('../')
from invoice_utils.invoice_utils import find_text, find_next_word
from invoice_utils.pdf2df import convert_to_df
from invoice_utils.invoice_utils import write_excel_sheet


def get_invoice_no(df):
    invoice_no = 'NULL'
    try:
        pos = find_next_word(df, 'Invoice', 'Number')
        invoice_no = df[pos[0] + 2:pos[0] + 3]['TEXT'].values[0]
        return invoice_no
    except Exception as e:
        print(str(e))
        pass
    return invoice_no

def get_invoice_date(df):
    invoice_date ='NULL'
    try:
        pos = find_next_word(df, 'Invoice', 'Date')
        invoice_date = df.iloc[pos[0] + 2:pos[0] + 3]['TEXT'].values[0]

        return invoice_date
    except Exception as e:
        print(str(e))
        pass
    return invoice_date


def rearrange(df):
    for i in range(1, len(df)):
        temp = df.loc[i, 'Y1'] - df.loc[i - 1, 'Y1']
        if -5 < temp < 5:
            df.loc[i, 'Y1'] = df.loc[i - 1, 'Y1']

    return df.sort_values(by=['page_no', 'Y1', 'X1']).reset_index(drop=True)


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
    table_start = find_next_word(df, 'Unit', 'Price')
    table_end = find_next_word(df, 'Vat', 'Analysis')
    if not len(table_end):
        last_pos = df.iloc[[-1]].index.to_list()
        print(last_pos)
        table_data = df[table_start[0]:]

    else:
        table_data = df[table_start[0]:table_end[0]]

    msg = dict()

    for index, row in table_data.iterrows():
        if row['X1'] < 60 and row['TEXT'].isdigit():
            msg = dict()
            msg['qty'] = row['TEXT']
            msg['part'] = ''

        if ('qty' in msg) and (60 < row['X1'] < 90):
            msg['part'] = row['TEXT']
            msg['desc'] = ''

        if ('desc' in msg) and (180 < row['X1'] < 360):
            msg['desc'] = msg['desc'] + " " + row['TEXT']
            msg['unit'] = ''

        if ('unit' in msg) and (400 < row['X1'] < 460):
            msg['unit'] = row['TEXT']
            msg['disc'] = 0
            msg['total'] = 0

        if 'disc' in msg and 470 < row['X1'] < 500:
            msg['disc'] = row['TEXT']
            msg['total'] = 0

        if 'total' in msg and 520 < row['X1'] < 560:
            msg['total'] = row['TEXT']
            result.append(msg)
            msg = dict()


def start_process(df, excel_filepath):
    result = dict()
    df_sort = df.sort_values(by=['page_no','Y1', 'X1']).reset_index(drop=True)
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

    write_excel_sheet(prev_filename, result, 'Demesne')



if __name__ == '__main__':
    print('This kumar')
    # filename = '../pdf_data/Demesne/Demesne - 1001000 - CP312.pdf'
    filename = '../new_pdf/deme_error.pdf'
    df = convert_to_df(filename)
    excel_filepath = r'../excel_data'
    # convert_pdf_to_csv(filename, r'../csv_data/demesne_v2.csv')
    start_process(df, excel_filepath)





