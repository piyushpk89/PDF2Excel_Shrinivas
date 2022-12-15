import os

filelist =os.listdir('../pdf_data')
print(filelist)

for item in filelist:
    folder = os.path.join('../csv_data', item)
    if not os.path.exists(folder):
        os.makedirs(folder)
