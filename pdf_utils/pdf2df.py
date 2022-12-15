import fitz
import pandas as pd

def convert_to_df(filename):
    try:
        doc = fitz.open(filename)
        print(doc.metadata)
        flag = True
        message={}
        result = list()
        # message = []
        for page in doc.pages():
            text_dic = page.getText("words")
            for item in text_dic:
                message = {}
                # pprint(item)
                X1,Y1,X2,Y2,word, block_no, line_no, word_no = item
                message['TEXT'] = word
                message['X1'] =int(X1)
                message['Y1'] =int(Y1)
                message['X2'] =int(X2)
                message['Y2'] =int(Y2)
                message['block_no'] =int(block_no)
                message['line_no'] =int(line_no)
                message['page_no'] = int(page.number)+1
                result.append(message)

            df = pd.DataFrame(result)
        return df
    except Exception as e:
        print(str(e))


def convert_pdf_to_csv(pdf_path, csv_path):
    # df.to_csv(csv_path)
    try:
        df = convert_to_df(pdf_path)
        df.to_csv(csv_path, index=False)
        return True
    except Exception as e:
        print(str(e))
        return False
