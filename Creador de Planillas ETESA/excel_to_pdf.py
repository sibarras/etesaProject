import win32com.client as converter
import os

PATH = os.path.abspath(__file__).rstrip(__file__.split('\\')[-1])
PATH = os.path.join(PATH, 'Excel Books', 'results')

def excel_to_pdf(wb_name:str, PATH=PATH):
    wb_PATH = PATH + wb_name + '.xlsx'
    pdf_PATH = PATH + wb_name + '.pdf'

    excel = converter.Dispatch("Excel.Application")
    excel.Visible = False

    try:
        wb = excel.Workbooks.Open(wb_PATH)
        wb.WorkSheets([1,2]).Select()
        wb.ActiveSheet.ExportAsFixedFormat(0, pdf_PATH)
    except Exception as e:
        print('[ERROR]: ', e)
    finally:
        wb.Close()
        excel.Quit()
