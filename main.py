"""







Created by author : Piyush Kumar
Contact Details : 9588280153
Whats app no: 8985563435
Email : piyush.kumar.0i0@gmail.com



IF you need to create more project let me know






"""

import os

import sys
from time import sleep
import shutil
from tqdm import tqdm

sys.path.append('/invoice_code')
from invoice_code import bpx, eew, mitsubishi, demense_multi, \
    IFM, JandJ, kilkenny, radionics, \
    rittal, SB, techdrive_single, carlow, techdrive_multi, mitsubishi_v1, bpx_quotation

from pdf_utils.pdf2df import convert_to_df
from invoice_utils.invoice_utils import find_text


def removeList(dirPath):
    data_list = os.listdir(dirPath)
    for data in data_list:
        os.remove(os.path.join(dirPath,data))

def zip_file(srcDir, dstOutput):
    dst = dstOutput +'/download'
    src = srcDir
    removeList(dstOutput)
    import shutil
    path_to_archive = shutil.make_archive(dst, 'zip', src)
    print(path_to_archive)
    # removeList(srcDir)
    print('All Data is Archived Now !!!!!!!! =>>>')
    return path_to_archive

def check_name(df ,vendor_name, case=False):
    pos = find_text(df, vendor_name, case=case)
    if len(pos):
        return True
    else:
        return False


def create_new_excel(excel_template, excel_path):
    removeList(excel_path)
    print("Excel Removed from : ", excel_path)
    sheet = os.listdir(excel_template)[0]
    shutil.copy(os.path.join(excel_template, sheet), excel_path)


def process_pdf_files(input_folder, excel_path, archive_path, excel_template):
    create_new_excel(excel_template, excel_path)
    fileList = os.listdir(input_folder)
    with tqdm(total=100, desc="Extracting PDF Data to Excel") as pbar:
        for item in fileList:
            try:
                pdf_filename = os.path.join(input_folder, item)
                print("Calling This PDF Filename ", pdf_filename)
                df = convert_to_df(pdf_filename)

                if check_name(df, 'BPX', case=True):
                    print("Calling function : BPX")
                    if check_name(df,'Invoice',case=True):
                        bpx.start_process(df,excel_path)
                    elif check_name(df, "Quotation", case=True):
                        bpx_quotation.start_process(df, excel_path)

                elif check_name(df, 'demesne'):
                    print("Calling Demensne")
                    demense_multi.start_process(df,excel_path)

                elif check_name(df,'eew'):
                    eew.start_process(df,excel_path)

                elif check_name(df,'mitsubishi'):
                    mitsubishi_v1.start_process(df,excel_path)

                elif check_name(df ,"ifm"):
                    IFM.start_process(df, excel_path)

                elif check_name(df, 'J&J'):
                    JandJ.start_process(df, excel_path)

                elif check_name(df, 'info@kws.ie'):
                    kilkenny.start_process(df, excel_path)

                elif check_name(df , "Radionics"):
                    radionics.start_process(df , excel_path)

                elif check_name(df , "Rittal"):
                    rittal.start_process(df ,excel_path)

                elif check_name(df ,"sbsteel"):
                    SB.start_process(df , excel_path)

                elif check_name(df, "Technidrive"):
                    page_no = df['page_no'].unique()
                    if len(page_no) > 1:
                        techdrive_multi.start_process(df,excel_path)
                    else:
                        techdrive_single.start_process(df ,excel_path)


                elif check_name(df , "CARLOW", case=True):
                    carlow.start_process(df , excel_path)

                data=float(100.0/len(fileList))
                if (pbar.last_print_n+data) > 100:
                    data = 100-pbar.last_print_n

                pbar.update(data)
            except Exception as e:
                print('Either PDF is Image or code Issue', item)
                with open('file_issue.txt', 'a') as fp:
                    fp.write(item)
                    fp.write('\n')
                shutil.copy(os.path.join(input_folder, item),"error_pdf" )


    zipFile = zip_file(excel_path, archive_path)
    return True


if __name__ == '__main__':
    # pdf_filename = r'pdf_data/EEW/EEW  - ICI204571 - CP313.pdf'
    # # filename = '../pdf_data/Demesne/Demesne - 1001000 - CP312.pdf'
    # df = convert_to_df(pdf_filename)
    # excel_filepath = r'../excel_data'
    # convert_pdf_to_csv(filename, r'../csv_data/demesne_v2.csv')
    excel_path = 'excel_data'

    # input_folder = 'pdf_data/BPX'
    input_folder = 'input_pdf'
    archive = 'Archive'

    excel_template = 'excel_template'

    # fileList = os.listdir(input_folder)
    # input_folder = 'error_pdf'
    process_pdf_files(input_folder, excel_path, archive, excel_template)
    # create_new_excel(excel_template, excel_path)