from win32com import client

app = client.gencache.EnsureDispatch('Word.Application')
app.ActiveDocument.Active