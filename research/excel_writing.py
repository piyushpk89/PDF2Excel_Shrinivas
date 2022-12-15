# import the win32 module
import win32com.client

# create an xl object
xl = win32com.client.Dispatch("Excel.Application")
# create a workbook object
wrkBk = xl.Workbooks.Add()
# from the workbook grab the active sheet as your worksheet object
wrkSht = wrkBk.ActiveSheet;
# renaming the worksheet, this is just for detail!
wrkSht.Name = 'mysheet'

