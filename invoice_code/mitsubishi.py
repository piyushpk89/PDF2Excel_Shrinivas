import traceback
from pprint import pprint
import os
import sys
sys.path.append('../')
from invoice_utils.invoice_utils import find_text
from invoice_utils.pdf2df import convert_to_df
from invoice_utils.invoice_utils import write_excel_sheet


def get_invoice_no(df):
    invoice_no = 'NULL'
    try:
        pos = find_text(df, 'Invoice')
        invoice_no = df[pos[0]+3:pos[0]+4]['TEXT'].values[0]
        return invoice_no
    except Exception as e:
        print(str(e))
        pass
    return invoice_no

def get_invoice_date(df):
    invoice_date ='NULL'
    try:
        pos_date = find_text(df, 'Date')
        invoice_date = df[pos_date[0] + 2:pos_date[0] + 3]['TEXT'].values[0]
        # invoice_date = date
        return invoice_date
    except Exception as e:
        print(str(e))
        pass
    return invoice_date

def get_table_data(df):

    msg = dict()
    result = list()

    try:
        table_start = find_text(df, 'Item')
        table_end = find_text(df, '______________________________________________')
        if len(table_end) < 3:
            table_end = find_text(df, 'commodity')

        table_data = df[table_start[0]:table_end[-1] + 1]
        for index, row in table_data.iterrows():

            if (40 < row['X1'] < 87) and (row['TEXT'].isdigit()):
                #         print(row['TEXT'])
                msg = dict()
                msg['item'] = row['TEXT']
                msg['disc'] = 0
                msg['desc_not'] = True
                print(row['TEXT'])

            if ('item' in msg) and (110 < row['X1'] < 142):
                msg['part'] = row['TEXT']
                print(row['TEXT'])
                msg['desc'] = ''

            if 'part' in msg and (173 < row['X1'] < 400) and msg['desc_not']:
                msg['desc'] = msg['desc'] + " " + row['TEXT']
                print(row['TEXT'])

            if row['TEXT'] == 'PC' and not 'qty' in msg:
                print(table_data.iloc[index - 2]['TEXT'])
                msg['qty'] = table_data.iloc[index - 2]['TEXT']
                msg['desc_not'] = False
                print(row['TEXT'])


            if row['TEXT'].__contains__('Discount'):
                msg['disc'] = table_data.iloc[index]['TEXT'].replace('-', '')
                print(row['TEXT'])

            if row['TEXT'].__contains__("Commodity"):
                msg['total'] = table_data.iloc[index - 2]['TEXT']
                msg['unit'] = str(float(msg['total'].replace(',','')) / int(msg['qty']))

                print(msg)

                result.append(msg)
                msg= dict()

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
    write_excel_sheet(prev_filename, result, 'Mitsubishi')



if __name__ == '__main__':
    print('This kumar')
    filename = '../pdf_data/Mitsubishi/Mitsubishi_3.pdf'
    df = convert_to_df(filename)
    excel_filepath = r'../excel_data'
    # convert_pdf_to_csv(filename, r'../csv_data/eew_71.csv')
    start_process(df, excel_filepath)





