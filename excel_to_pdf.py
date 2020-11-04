import win32com.client as converter

def excel_to_pdf(wb_name:str, PATH='C:\\Users\\Samuel\\Desktop\\Projects\\etesaProject\\Excel Books\\results\\'):
    wb_PATH = PATH + wb_name + '.xlsx'
    pdf_PATH = PATH + wb_name + '.pdf'

    excel = converter.Dispatch("Excel.Application")
    excel.Visible = False

    try:
        print('Start conversion to PDF')
        wb = excel.Workbooks.Open(wb_PATH)
        wb.WorkSheets([1,2]).Select()
        wb.ActiveSheet.ExportAsFixedFormat(0, pdf_PATH)
    except Exception as e:
        print('[ERROR]: ', e)
    finally:
        wb.Close()
        excel.Quit()

excel_to_pdf('prueba')